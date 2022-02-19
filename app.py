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

dfProvidersPayment = df.groupby(['Nombre Fantasia'], as_index=False)['Importe'].sum()
figProvidersPayment = px.bar(dfProvidersPayment, x="Nombre Fantasia", y="Importe", labels={
    "Nombre Fantasia": "proveedor",
    "Importe": "Dinero percibido",
}, color_continuous_scale="Peach", color="Importe")

providersPaymentTab = html.Div(children=[
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H5(
                        "En esta seccion puede conocerse el dinero percibido por diferentes proveedores en un rubro",
                    ),
                ], className='dropdown-tab-title', width=8
            ),
            dbc.Col(
                [
                    dbc.DropdownMenu(
                        label="Rubro",
                        children=[
                            dbc.DropdownMenuItem("Rubro 1"),
                            dbc.DropdownMenuItem("Rubro 2"),
                            dbc.DropdownMenuItem("Rubro 3"),
                        ]
                    )
                ], className='drop-down'
            )

        ], justify="center", className='title-row'
    ),
    dbc.Row(
        [dbc.Col([
            dcc.DatePickerRange(
                id='dateRangeProvidersPayment',
                min_date_allowed=dt(2020, 5, 1),
                max_date_allowed=dt(2020, 5, 31),
                start_date=dt(2020, 5, 1).date(),
                end_date=dt(2020, 5, 31).date(),
                display_format='D/M/Y',
                calendar_orientation='horizontal'),
        ], width=6, className='date-row'
        ),
        ], justify="center"
    ),
    dbc.Row(
        [
            html.Div([
                dcc.Graph(figure=figProvidersPayment)
            ])
        ]
        , justify="center"
    ),
])

figExpensesEvolution = px.line(dfProvidersPayment, x="Nombre Fantasia", y="Importe", labels={
    "Nombre Fantasia": "proveedor",
    "Importe": "Dinero percibido",
})
figExpensesEvolution.data[0].line.color = "Red"

expensesEvolutionTab = html.Div(children=[
    dbc.Row(
        dbc.Col([
            html.H5("En esta seccion puede conocerse la evolución del gasto en el tiempo"),
        ], width=12, className='tab-title'
        ), justify="center"
    ),
    dbc.Row(
        [dbc.Col([
            dcc.DatePickerRange(
                id='dateRangeExpensesEvolution',
                min_date_allowed=dt(2020, 5, 1),
                max_date_allowed=dt(2020, 5, 31),
                start_date=dt(2020, 5, 1).date(),
                end_date=dt(2020, 5, 31).date(),
                display_format='D/M/Y',
                calendar_orientation='horizontal'),
        ], width=6, className='date-row'
        ),
        ], justify="center"
    ),
    dbc.Row(
        [
            html.Div([
                dcc.Graph(figure=figExpensesEvolution)
            ])
        ]
        , justify="center"
    ),
])

table_header = [
    html.Thead(html.Tr([html.Th("Proveedor"), html.Th("Cuit"), html.Th("Importe Total")]))
]

row1 = html.Tr([html.Td("Proveedor 1"), html.Td("00-00000000-0"), html.Td("$1000")])
row2 = html.Tr([html.Td("Proveedor 2"), html.Td("00-00000000-0"), html.Td("$1000")])
row3 = html.Tr([html.Td("Proveedor 3"), html.Td("00-00000000-0"), html.Td("$1000")])
row4 = html.Tr([html.Td("Proveedor 4"), html.Td("00-00000000-0"), html.Td("$1000")])

table_body = [html.Tbody([row1, row2, row3, row4])]

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
                min_date_allowed=dt(2020, 5, 1),
                max_date_allowed=dt(2020, 5, 31),
                start_date=dt(2020, 5, 1).date(),
                end_date=dt(2020, 5, 31).date(),
                display_format='D/M/Y',
                calendar_orientation='horizontal'),
        ], width=6, className='date-row'
        ),
        ], justify="center"
    ),
    dbc.Row(
        [
            dbc.Table(
                # using the same table as in the above example
                table_header + table_body,
                bordered=True,
                hover=True,
                responsive=True,
                striped=True,
            )
        ]
        , justify="center", className='centered-table'
    ),
])

body = html.Div(
    [
        html.Hr(),
        dbc.Row(dbc.Col(revenueTab)),
        html.Hr(),
        dbc.Row(dbc.Col(providersPaymentTab)),
        html.Hr(),
        dbc.Row(dbc.Col(expensesEvolutionTab)),
        html.Hr(),
        dbc.Row(dbc.Col(providersRankingTab)),
    ]
)

app.layout = html.Div(children=[
    topNavBar,
    title,
    body])


@app.callback([Output('totalRevenue', 'children'), Output('totalProviders', 'children'), Output('totalBuyOrders', 'children')],
              [Input('dateRangeRevenue', 'start_date'), Input('dateRangeRevenue', 'end_date')]
              )
def update_figure(initial_date, final_date):
    initial_date = dt.strptime(re.split('T| ', initial_date)[0], '%Y-%m-%d')
    final_date = dt.strptime(re.split('T| ', final_date)[0], '%Y-%m-%d')
    filtered_df = utils.filter_by_date(df, initial_date, final_date)
    revenue_data = utils.revenue_data(filtered_df)
    return revenue_data[0], revenue_data[1], revenue_data[2]


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)