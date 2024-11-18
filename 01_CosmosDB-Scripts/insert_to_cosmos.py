from datetime import datetime
from connect_to_cosmos import connect_to_cosmos
import config
from azure.cosmos.exceptions import CosmosResourceNotFoundError, CosmosResourceExistsError

def insert_revenue_data(customer_id, revenue_amount):
    container = connect_to_cosmos(config.settings['container_id'])
    if not container:
        print("Failed to connect to the Cosmos DB container.")
        return

    # Generate a unique ID for the new revenue entry
    data_id = f"{customer_id}_{datetime.now().strftime('%Y%m%d')}"

    # Create the new revenue entry
    new_data = {
        'id': data_id,
        'client_id': customer_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'revenue': revenue_amount,
        'currency': 'CHF'
    }

    # Step 1: Query all existing entries for the same client_id
    existing_items = list(container.query_items(
        query="SELECT * FROM c WHERE c.client_id = @client_id",
        parameters=[{"name": "@client_id", "value": customer_id}],
        enable_cross_partition_query=True
    ))

    # Step 2: Delete all existing entries for the client_id
    for item in existing_items:
        try:
            container.delete_item(item=item['id'], partition_key=customer_id)
            print(f"Deleted outdated revenue entry: {item['id']} for customer {customer_id}")
        except CosmosResourceNotFoundError:
            print(f"Item {item['id']} was not found during deletion. Skipping.")

    # Step 3: Insert the new revenue record
    try:
        container.create_item(body=new_data)
        print(f"Inserted latest revenue data for customer {customer_id}: {revenue_amount} CHF")
    except CosmosResourceExistsError:
        print(f"Conflict: Revenue data with id {data_id} already exists.")


# Insert HaloPSA data (open tickets and projects)
def insert_halopsa_data(client_id, open_ticket_count, open_project_count):
    container = connect_to_cosmos(config.settings['container_id_halopsa'])
    if not container:
        print("Failed to connect to the Cosmos DB container.")
        return

    # Generate a unique ID for the data entry
    data_id = f"{client_id}_{datetime.now().strftime('%Y%m%d')}"

    # Create the new data entry
    new_data = {
        'id': data_id,
        'client_id': client_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'open_ticket_count': open_ticket_count,
        'open_project_count': open_project_count
    }

    # Check if an entry with the same ID already exists
    existing_items = list(container.query_items(
        query="SELECT * FROM c WHERE c.id = @id",
        parameters=[{"name": "@id", "value": data_id}],
        enable_cross_partition_query=True
    ))

    if existing_items:
        existing_data = existing_items[0]
        if existing_data['open_ticket_count'] == open_ticket_count and existing_data['open_project_count'] == open_project_count:
            print("Same data line is already in the DB; no action taken.")
        else:
            container.replace_item(item=existing_data, body=new_data)
            print(f"Updated data for client {client_id} with open tickets: {open_ticket_count}, open projects: {open_project_count}")
    else:
        container.create_item(body=new_data)
        print(f"Inserted data for client {client_id} with open tickets: {open_ticket_count}, open projects: {open_project_count}")


# Insert individual ticket details into HaloPSA Cosmos DB container
def insert_ticket_data(client_id, ticket_id, summary, user_name, date_occurred):
    container = connect_to_cosmos(config.settings['container_id_halopsa'])
    if not container:
        print("Failed to connect to the Cosmos DB container for HaloPSA tickets.")
        return

    # Generate a unique ID for each ticket based on client and ticket ID
    ticket_data_id = f"{client_id}_{ticket_id}"

    # Define the ticket entry
    ticket_data = {
        'id': ticket_data_id,
        'client_id': client_id,
        'ticket_id': ticket_id,
        'summary': summary,
        'user_name': user_name,
        'date_occurred': date_occurred,
        'date_logged': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Check if an entry with the same ticket ID already exists
    existing_items = list(container.query_items(
        query="SELECT * FROM c WHERE c.id = @id",
        parameters=[{"name": "@id", "value": ticket_data_id}],
        enable_cross_partition_query=True
    ))

    if existing_items:
        print(f"Ticket {ticket_id} for client {client_id} is already logged in the DB; no action taken.")
    else:
        container.create_item(body=ticket_data)
        print(f"Inserted ticket {ticket_id} for client {client_id} into the database.")
        

def sync_tickets_with_db(client_id, open_tickets):
    """
    Syncs the latest ticket data with the database by removing outdated tickets 
    and updating or inserting new ones.
    """
    container = connect_to_cosmos(config.settings['container_id_halopsa'])
    if not container:
        print("Failed to connect to the Cosmos DB container for HaloPSA tickets.")
        return

    # Step 1: Get all ticket IDs currently in the database for the client
    existing_tickets = list(container.query_items(
        query="SELECT c.id FROM c WHERE c.client_id = @client_id AND IS_DEFINED(c.ticket_id)",
        parameters=[{"name": "@client_id", "value": client_id}],
        enable_cross_partition_query=True
    ))

    # Extract the ticket IDs from the database
    existing_ticket_ids = {ticket['id'] for ticket in existing_tickets}

    # Step 2: Extract the ticket IDs from the latest API response
    new_ticket_ids = set()
    for ticket in open_tickets:
        ticket_id = f"{client_id}_{ticket['id']}"
        new_ticket_ids.add(ticket_id)
        
        # Prepare ticket data for insertion/updating
        ticket_data = {
            'id': ticket_id,
            'client_id': client_id,
            'ticket_id': ticket['id'],
            'summary': ticket.get('summary'),
            'user_name': ticket.get('user_name'),
            'dateoccurred': ticket.get('dateoccurred'),
            'date_logged': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Check if the ticket already exists in the database
        existing_items = list(container.query_items(
            query="SELECT * FROM c WHERE c.id = @id",
            parameters=[{"name": "@id", "value": ticket_id}],
            enable_cross_partition_query=True
        ))

        if existing_items:
            print(f"Ticket {ticket['id']} for client {client_id} is already in the DB; no action taken.")
        else:
            # Insert new ticket data if no matching entry exists
            container.create_item(body=ticket_data)
            print(f"Inserted ticket {ticket['id']} for client {client_id} into the database.")

    # Step 3: Find tickets that need to be deleted (exist in DB but not in the latest API response)
    tickets_to_delete = existing_ticket_ids - new_ticket_ids
    for ticket_id in tickets_to_delete:
        container.delete_item(item=ticket_id, partition_key=client_id)
        print(f"Deleted outdated ticket {ticket_id} for client {client_id} from the database.")
