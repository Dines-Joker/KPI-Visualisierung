import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://dinesnimalthas.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'vC3qN45346JydHJ1ke9uOCHPdtSGRdHJ203bsCWyVNCbnTA7Uc7hUZU7pF1hoOhqNgjQneMk5J1PACDbr6f7xQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'KPI'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'ERPNext'),
    'container_id_halopsa': os.environ.get('COSMOS_CONTAINER', 'HaloPSA'),

    # Halopsa API configuration
    'halopsa_api_url': 'https://jokerit.halopsa.com/api/Tickets',
    'halopsa_client_id': '10306', 
    'oauth_token': 'VITPmYtYUGIh4j7ZvEzRw3FbL8jet5cZDl0m8mfPA4o', # OAuth Token has to be renewed every hour

    # ERPNext API configuration
    'erpnext_customer_id': "10306",
    'erpnext_start_date': "2024-01-01",
    'erpnext_api_key': "65f5314118f3305",
    'erpnext_api_secret': "a1edf25daa9376d",
    'erpnext_api_url': 'https://erp.jokerit.cloud/api/resource/Sales%20Invoice'
}
