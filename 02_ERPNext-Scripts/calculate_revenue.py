def calculate_revenue(invoices):
    total_revenue = sum(float(invoice.get("grand_total", 0)) for invoice in invoices)
    print(f"Calculated total revenue: CHF {total_revenue}")
    return round(total_revenue, 2)
