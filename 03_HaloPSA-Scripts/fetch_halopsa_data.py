import requests
import config

def fetch_open_ticket_and_project_count(client_id):
    """Fetches both the open ticket count and open project count for a specific client from HaloPSA API, along with ticket details."""
    headers = {
        "Authorization": f"Bearer {config.settings['oauth_token']}"
    }
    
    # Parameters for fetching open tickets
    ticket_params = {
        "includeclosed": "0",
        "client_ref": client_id
    }
    
    # Fetch open ticket count and details
    ticket_response = requests.get(config.settings['halopsa_api_url'], headers=headers, params=ticket_params)
    open_tickets = []
    if ticket_response.status_code == 200:
        ticket_data = ticket_response.json()
        open_ticket_count = ticket_data.get('record_count', 0)
        
        # Extract required ticket details
        for ticket in ticket_data.get('tickets', []):  # Assuming 'tickets' is the key containing ticket info
            ticket_info = {
                "id": ticket.get("id"),
                "summary": ticket.get("summary"),
                "user_name": ticket.get("user_name"),
                "dateoccurred": ticket.get("dateoccurred")
            }
            open_tickets.append(ticket_info)
    else:
        print(f"Failed to fetch open tickets: {ticket_response.status_code} - {ticket_response.text}")
        open_ticket_count = None

    # Parameters for fetching open projects
    project_params = {
        "includeclosed": "0",
        "client_ref": client_id
    }

    # Fetch open project count
    project_response = requests.get(config.settings['halopsa_api_url'], headers=headers, params=project_params)
    if project_response.status_code == 200:
        project_data = project_response.json()
        open_project_count = project_data.get('record_count', 0)
    else:
        print(f"Failed to fetch open projects: {project_response.status_code} - {project_response.text}")
        open_project_count = None

    return open_ticket_count, open_project_count, open_tickets
