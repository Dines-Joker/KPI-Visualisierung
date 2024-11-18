import os
import sys


# Append the package directories to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../01_CosmosDB-Scripts')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../02_ERPNext-Scripts')))


# Import config & modules from the packages
import config 

from insert_to_cosmos import insert_revenue_data
from fetch_erpnext_data import fetch_erpnext_data
from calculate_revenue import calculate_revenue

def main():
    # Step 1: Fetch data from ERPNext
    invoices = fetch_erpnext_data(
        config.settings['erpnext_customer_id'],
        config.settings['erpnext_start_date'],
        config.settings['erpnext_api_key'],
        config.settings['erpnext_api_secret']
    )
    
    # Step 2: Calculate total revenue
    total_revenue = calculate_revenue(invoices)
    
    # Step 3: Insert data into Cosmos DB
    insert_revenue_data(config.settings['erpnext_customer_id'], total_revenue)

if __name__ == "__main__":
    main()
