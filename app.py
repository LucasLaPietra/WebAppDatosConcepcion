import dash
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from datetime import datetime as dt
import plotly.express as px
import flask
import pandas as pd
import utils
import re

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.BOOTSTRAP], server=server)
app.title = 'Visualizacion datos contratos publicos'

df = pd.read_csv('https://github.com/LucasLaPietra/WebScraperDatosConcepcion/blob/main/webscraping-app/contratos'
                 '/contratos-complete.csv?raw=true')

maxYear = df['Año'].max()
minYear = df['Año'].min()
maxFirstYearMonth = df[(df['Año'] == minYear)]['Mes'].max()
minFirstYearMonth = df[(df['Año'] == minYear)]['Mes'].min()
maxActualYearMonth = df[(df['Año'] == maxYear)]['Mes'].max()
minActualYearMonth = df[(df['Año'] == maxYear)]['Mes'].min()

topNavBar = dbc.Navbar(
    children=[
        html.Div(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col([
                        html.H1(children='Visualizacion de datos de contratos publicos de Concepcion del Uruguay'),
                        html.H5(children='Datos Concepcion')
                    ])
                ],
                align="center", className='nav-bar'
            )
        )
    ],
    color="primary",
    dark=True,
    sticky="top"
)

title = dbc.Container(
    children=[
        dbc.Row([html.H4("Actualmente la municipalidad de concepcion del uruguay informa en su sitio",
                         className='centered-subtitle'),
                 ], justify="center"
                )
    ]
)

revenueTab = dbc.Container(children=[
    dbc.Row(
        dbc.Col([
            html.H5("En esta seccion pueden conocerse los gastos del municipio en un periodo determinado"),
        ], width=12, className='tab-title'
        ), justify="center"
    ),
    dbc.Row(
        [dbc.Col([
            dcc.DatePickerRange(
                id='dateRangeRevenue',
                min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                start_date=dt(maxYear, minActualYearMonth, 1).date(),
                end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                display_format='D/M/Y',
                calendar_orientation='horizontal'),
        ], width=6, className='date-row'
        ),
        ], justify="center"
    ),
    dbc.Row(
        [
            dbc.Col([
                dbc.Card([
                    html.Img(src=app.get_asset_url("file-lines-solid.svg"), className='revenue-icon'),
                    html.H4("Total de ordenes de compra por:"),
                    html.H3(id='totalRevenue'),
                ])
            ], className='revenue-column'
            ),
            dbc.Col([
                dbc.Card([
                    html.Img(src=app.get_asset_url("clipboard-solid.svg"), className='revenue-icon'),
                    html.H4("Cantidad de proveedores:"),
                    html.H3(id='totalProviders'),
                ])
            ], className='revenue-column'
            ),
            dbc.Col([
                dbc.Card([
                    html.Img(src=app.get_asset_url("dolly-solid.svg"), className='revenue-icon'),
                    html.H4("Cantidad de ordenes de compra:"),
                    html.H3(id='totalBuyOrders'),
                ])
            ], className='revenue-column'
            )]
        , justify="center"
    ),
])

providersPaymentTab = html.Div(children=[
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H5(
                        "En esta seccion puede conocerse el dinero percibido por diferentes proveedores en un rubro",
                    ),
                ], className='tab-title'
            ),

        ], justify="center"
    ),
    dbc.Row(
        [dbc.Col([
            dcc.DatePickerRange(
                id='dateRangeProvidersPayment',
                min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                start_date=dt(maxYear, minActualYearMonth, 1).date(),
                end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                display_format='D/M/Y',
                calendar_orientation='horizontal'),
        ], width=6, className='date-row'
        ),
        ], justify="center"
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                    html.P('Rubro:'),
                    dcc.Dropdown(
                        id='providersPaymentDropDown',
                        options=[{'label': "Ninguno", 'value': "None"}],
                        value="None",
                        multi=False,
                        clearable=False,
                        className='drop-down'
                    ),
                    html.P('Orientacion:'),
                    dcc.Dropdown(
                        id='providersPaymentOrientationDropDown',
                        options=[{'label': "Horizontal", 'value': "Horizontal"},
                                 {'label': "Vertical", 'value': "Vertical"}],
                        value="Horizontal",
                        multi=False,
                        clearable=False,
                        className='drop-down'
                    ),
                    html.P('Ordenar por:'),
                    dcc.Dropdown(
                        id='providersPaymentOrderDropDown',
                        options=[{'label': "Nombre", 'value': "Nombre Fantasia"},
                                 {'label': "Importe", 'value': "Importe"}],
                        value="Importe",
                        multi=False,
                        clearable=False,
                        className='drop-down'
                    ),
                ], className='drop-down-col'
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='providersPaymentGraph')
                ]), width=10
            ),
        ]
        , justify="center", align="center"
    ),
])

figExpensesEvolution = px.line(df, x="Nombre Fantasia", y="Importe", labels={
    "Nombre Fantasia": "proveedor",
    "Importe": "Dinero percibido",
})
figExpensesEvolution.data[0].line.color = "Red"

expensesEvolutionTab = html.Div(children=[
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H5(
                        "En esta seccion puede conocerse la evolución del gasto en el tiempo",
                    ),
                ], className='dropdown-tab-title', width=8
            ),
            dbc.Col(
                [
                    dcc.Dropdown(
                        id='expensesEvolutionDropDown',
                        multi=True,
                    ),
                ], className='drop-down'
            )

        ], justify="center", className='title-row'
    ),
    dbc.Row(
        [dbc.Col([
            dcc.DatePickerRange(
                id='dateRangeExpensesEvolution',
                min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                start_date=dt(maxYear, minActualYearMonth, 1).date(),
                end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                display_format='D/M/Y',
                calendar_orientation='horizontal'),
        ], width=6, className='date-row'
        ),
        ], justify="center"
    ),
    dbc.Row(
        [
            html.Div([
                dcc.Graph(id="expensesEvolutionGraph")
            ])
        ]
        , justify="center"
    ),
])

providersRankingTab = dbc.Container(children=[
    dbc.Row(
        dbc.Col([
            html.H5("Ranking de proveedores de acuerdo al gasto total"),
        ], width=12, className='tab-title'
        ), justify="center"
    ),
    dbc.Row(
        [dbc.Col([
            dcc.DatePickerRange(
                id='dateRangeProvidersRanking',
                min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                start_date=dt(maxYear, minActualYearMonth, 1).date(),
                end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                display_format='D/M/Y',
                calendar_orientation='horizontal'),
        ], width=6, className='date-row'
        ),
        ], justify="center"
    ),
    dbc.Row(justify="center", className='centered-table', id='providersRankingTable'),
])

providersSearchTab = dbc.Container(children=[
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H5(
                        "En esta seccion puede buscarse un proveedor de acuerdo a una palabra clave",
                    ),
                ], className='dropdown-tab-title', width=8
            ),
            dbc.Col(
                [
                    dbc.Input(placeholder="Ingrese nombre o razon social del proveedor",
                              type="text",
                              id="providersSearchInput",
                              value="")
                ], className='drop-down'
            )

        ], justify="center", className='title-row'
    ),
    dbc.Row(
        [dbc.Col([
            dcc.DatePickerRange(
                id='dateRangeProvidersSearch',
                min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                start_date=dt(maxYear, minActualYearMonth, 1).date(),
                end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                display_format='D/M/Y',
                calendar_orientation='horizontal'),
        ], width=6, className='date-row'
        ),
        ], justify="center"
    ),
    dbc.Row(justify="center", className='centered-table', id='providersSearchTable'),
])

body = html.Div(
    [
        html.Hr(),
        dbc.Row(dbc.Col(revenueTab)),
        html.Hr(),
        dbc.Row(dbc.Col(providersPaymentTab)),
        html.Hr(),
        dbc.Row(dbc.Col(providersRankingTab)),
        html.Hr(),
        dbc.Row(dbc.Col(expensesEvolutionTab)),
        html.Hr(),
        dbc.Row(dbc.Col(providersSearchTab)),
    ]
)

app.layout = html.Div(children=[
    topNavBar,
    title,
    body])


@app.callback(
    [Output('totalRevenue', 'children'), Output('totalProviders', 'children'), Output('totalBuyOrders', 'children')],
    [Input('dateRangeRevenue', 'start_date'), Input('dateRangeRevenue', 'end_date')]
)
def update_figure(initial_date, final_date):
    initial_date = dt.strptime(re.split('T| ', initial_date)[0], '%Y-%m-%d')
    final_date = dt.strptime(re.split('T| ', final_date)[0], '%Y-%m-%d')
    filtered_df = utils.filter_by_date(df, initial_date, final_date)
    revenue_data = utils.revenue_data(filtered_df)
    return revenue_data[0], revenue_data[1], revenue_data[2]


@app.callback([Output('providersPaymentGraph', 'figure'), Output('providersPaymentDropDown', 'options')],
              [Input('dateRangeProvidersPayment', 'start_date'), Input('dateRangeProvidersPayment', 'end_date'),
               Input('providersPaymentDropDown', 'value'), Input('providersPaymentOrientationDropDown', 'value'),
               Input('providersPaymentOrderDropDown', 'value')]
              )
def update_figure(initial_date, final_date, category, orientation, order):
    initial_date = dt.strptime(re.split('T| ', initial_date)[0], '%Y-%m-%d')
    final_date = dt.strptime(re.split('T| ', final_date)[0], '%Y-%m-%d')
    filtered_df = utils.filter_by_date(df, initial_date, final_date)
    df_providers_payment = utils.make_providers_payment_df(filtered_df, order)
    categories = set(df_providers_payment['Rubro'])
    dict_filter = [{'label': i.capitalize(), 'value': i} for i in categories]
    dict_filter.append({'label': "Ninguno", 'value': "None"})
    df_filtered_by_category = utils.filter_by_category(df_providers_payment, category)
    if orientation == 'Horizontal':
        fig_providers_payment = px.bar(df_filtered_by_category, x="Importe", y="Nombre Fantasia", labels={
            "Nombre Fantasia": "proveedor",
            "Importe": "Dinero percibido",
        }, color_continuous_scale="Peach", color="Importe", orientation='h')
    else:
        fig_providers_payment = px.bar(df_filtered_by_category, x="Nombre Fantasia", y="Importe", labels={
            "Nombre Fantasia": "proveedor",
            "Importe": "Dinero percibido",
        }, color_continuous_scale="Peach", color="Importe", orientation='v')
    return fig_providers_payment, dict_filter


@app.callback([Output('expensesEvolutionGraph', 'figure'), Output('expensesEvolutionDropDown', 'options')],
              [Input('dateRangeExpensesEvolution', 'start_date'), Input('dateRangeExpensesEvolution', 'end_date'),
               Input('expensesEvolutionDropDown', 'value')]
              )
def update_figure(initial_date, final_date, selected_categories):
    initial_date = dt.strptime(re.split('T| ', initial_date)[0], '%Y-%m-%d')
    final_date = dt.strptime(re.split('T| ', final_date)[0], '%Y-%m-%d')
    filtered_df = utils.filter_by_date(df, initial_date, final_date)
    categories = set(filtered_df['Rubro'])
    dict_filter = [{'label': i.capitalize(), 'value': i} for i in categories]
    if (selected_categories is None) or (len(selected_categories) == 0):
        df_new = utils.make_expenses_evolution_df(filtered_df, False)
        fig_expenses_evolution = px.line(df_new, x="date", y="Importe", labels={
            "date": "Fecha",
            "Importe": "Dinero",
        })
        fig_expenses_evolution.data[0].line.color = "Red"
    else:
        df_new = utils.make_expenses_evolution_df(filtered_df, True)
        df_categories_filtered = df_new[df_new['Rubro'].isin(selected_categories)]
        fig_expenses_evolution = px.line(df_categories_filtered, x="date", y="Importe", color="Rubro", labels={
            "date": "Fecha",
            "Importe": "Dinero",
        })
    return fig_expenses_evolution, dict_filter


@app.callback(Output('providersRankingTable', 'children'),
              [Input('dateRangeProvidersRanking', 'start_date'), Input('dateRangeProvidersRanking', 'end_date')]
              )
def update_figure(initial_date, final_date):
    initial_date = dt.strptime(re.split('T| ', initial_date)[0], '%Y-%m-%d')
    final_date = dt.strptime(re.split('T| ', final_date)[0], '%Y-%m-%d')
    filtered_df = utils.filter_by_date(df, initial_date, final_date)
    table_df = utils.create_ranking_table_df(filtered_df)
    table = dbc.Table.from_dataframe(
        table_df,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True)
    return table


@app.callback(Output('providersSearchTable', 'children'),
              [
                  Input('dateRangeProvidersRanking', 'start_date'),
                  Input('dateRangeProvidersRanking', 'end_date'),
                  Input("providersSearchInput", "value")
              ]
              )
def update_figure(initial_date, final_date, search_input):
    initial_date = dt.strptime(re.split('T| ', initial_date)[0], '%Y-%m-%d')
    final_date = dt.strptime(re.split('T| ', final_date)[0], '%Y-%m-%d')
    filtered_df = utils.filter_by_date(df, initial_date, final_date)
    table_df = utils.create_search_table_df(filtered_df, search_input)
    table = dbc.Table.from_dataframe(
        table_df,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True)
    return table


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
