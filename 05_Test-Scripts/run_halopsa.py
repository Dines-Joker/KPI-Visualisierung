import os
import sys

# Append the package directories to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../01_CosmosDB-Scripts')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../03_HaloPSA-Scripts')))

# Import modules
from insert_to_cosmos import insert_halopsa_data, sync_tickets_with_db
from fetch_halopsa_data import fetch_open_ticket_and_project_count

import config

def main():
    # Step 1: Fetch open ticket and project counts, along with detailed ticket information from HaloPSA
    open_ticket_count, open_project_count, open_tickets = fetch_open_ticket_and_project_count(config.settings['halopsa_client_id'])
    
    # Step 2: Insert both counts into Cosmos DB
    if open_ticket_count is not None and open_project_count is not None:
        insert_halopsa_data(config.settings['halopsa_client_id'], open_ticket_count, open_project_count)
    else:
        print("Failed to retrieve open ticket or project counts.")
    
    # Step 3: Sync tickets with the database (add new, update existing, delete outdated)
    sync_tickets_with_db(config.settings['halopsa_client_id'], open_tickets)

if __name__ == "__main__":
    main()
