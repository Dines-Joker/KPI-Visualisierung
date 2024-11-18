import requests

def fetch_erpnext_data(customer_id, start_date, api_key, api_secret):
    headers = {
        "Authorization": f"token {api_key}:{api_secret}"
    }
    filters = f'filters=[["customer", "=", "{customer_id}"], ["posting_date", ">=", "{start_date}"]]'
    fields = 'fields=["name", "grand_total", "posting_date"]'
    
    url = f"https://erp.jokerit.cloud/api/resource/Sales%20Invoice?{filters}&{fields}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    invoices = response.json().get("data", [])
    print(f"Fetched {len(invoices)} invoices for customer {customer_id}")
    return invoices
