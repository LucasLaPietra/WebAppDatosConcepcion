def revenue_data(df):
    total_revenue = "$" + str(round(df["Importe"].sum(), 2))
    total_providers = len(df["Razon social"].value_counts())
    total_buy_orders = df["Cantidad de contratados"].sum()
    return [total_revenue, total_providers, total_buy_orders]
