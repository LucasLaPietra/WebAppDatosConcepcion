from datetime import datetime as dt
from dash import html


def filter_by_date(df, initial_date, final_date):
    initial_year = initial_date.year
    final_year = final_date.year
    initial_month = initial_date.month
    final_month = final_date.month
    df_filter_year = df[(df['Año'] >= initial_year) & (df['Año'] <= final_year)]
    if initial_year == final_year:
        df_filter_month = df_filter_year.loc[
            ((df_filter_year['Mes'] >= initial_month) & (df_filter_year['Mes'] <= final_month))]
    else:
        df_filter_month = df_filter_year.loc[
            ((df_filter_year['Mes'] >= initial_month) & (df_filter_year['Año'] == initial_year)) | (
                        (df_filter_year['Mes'] <= final_month) & (df_filter_year['Año'] == final_year)) | (
                        (df_filter_year['Año'] != final_year) & (df_filter_year['Año'] != initial_year))]
    return df_filter_month


def make_providers_payment_df(df):
    df_providers_payment = df.groupby(['Nombre Fantasia', 'Rubro'], as_index=False)['Importe'].sum()
    return df_providers_payment


def filter_by_category(df, category):
    if category == "None":
        return df
    else:
        return df[df['Rubro'] == category]


def make_expenses_evolution_df(df, filter_by_category):
    df['date'] = df['Año'].astype(str) + '/' + df['Mes'].astype(str).str.zfill(2)
    if filter_by_category:
        filtered_df = df.groupby(['date','Rubro'], as_index=False)['Importe'].sum()
    else:
        filtered_df = df.groupby(['date'], as_index=False)['Importe'].sum()
    return filtered_df.sort_values(by=['date'])


def revenue_data(df):
    total_revenue = round(df["Importe"].sum(), 2)
    total_providers = len(df["Razon social"].value_counts())
    total_buy_orders = df["Cantidad de contratados"].sum()
    return [total_revenue, total_providers, total_buy_orders]


def create_ranking_table_df(df):
    filtered_df = df.groupby(['Nombre Fantasia', 'CUIL proveedor'], as_index=False)['Importe'].sum()
    ordered_df = filtered_df.sort_values(by=['Importe'], ascending=False)
    ordered_df['Nombre Fantasia'] = ordered_df['Nombre Fantasia'].apply(lambda x: x.capitalize())
    ordered_df['Importe'] = ordered_df['Importe'].apply(lambda x: round(x, 2))
    return ordered_df


def create_search_table_df(df, search_input):
    input_upper = search_input.upper()
    filtered_df = df[df['Nombre Fantasia'].str.contains(input_upper) | df['Razon social'].str.contains(input_upper)]
    filtered_df['Nombre Fantasia'] = filtered_df['Nombre Fantasia'].apply(lambda x: x.capitalize())
    filtered_df['Razon social'] = filtered_df['Razon social'].apply(lambda x: x.capitalize())
    return filtered_df
