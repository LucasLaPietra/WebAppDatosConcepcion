import dash
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from datetime import datetime as dt
import plotly.express as px
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL], server=server)
app.title = 'Visualizacion datos contratos publicos'

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
                align="center"
            )
        )
    ],
    color="primary",
    dark=True,
    sticky="top"
)

body = dbc.Container(
    children=[
        dbc.Row(
            [dbc.Col([
                html.H5("Para conocer la informacion en un rango de fechas determinado, "
                        "utilice el filtro por fechas", className='centered-subtitle')], width=12)
            ], justify="center"
        ),
        dbc.Row(
            [dbc.Col([
                dcc.DatePickerRange(
                    id='daterange',
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
        [
            dbc.Col([
                html.H4("Total de ordenes de compra por:"),
                html.H3("$10000000"),
            ], className='revenue-column'
            ),
            dbc.Col([
                html.H4("Cantidad de proveedores:"),
                html.H3("500"),
            ], className='revenue-column'
            ),
            dbc.Col([
                html.H4("Cantidad de ordenes de compra"),
                html.H3("1000"),
            ], className='revenue-column'
            )]
        , justify="center"
    ),
])

df = px.data.gapminder().query("country=='Canada'")
figProvidersPayment = px.bar(df, x="year", y="lifeExp",labels={
                     "year": "tiempo",
                     "lifeExp": "gasto",
                 },)

providersPaymentTab = html.Div(children=[
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H5(
                        "En esta seccion puede conocerse el dinero percibido por diferentes proveedores en un rubro",
                        ),
                ],className='dropdown-tab-title', width=8
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
        [
            html.Div([
                dcc.Graph(figure=figProvidersPayment)
            ])
        ]
        , justify="center"
    ),
])


figExpensesEvolution = px.line(df, x="year", y="lifeExp",labels={
                     "year": "tiempo",
                     "lifeExp": "gasto",
                 },)

expensesEvolutionTab = html.Div(children=[
    dbc.Row(
        dbc.Col([
            html.H5("En esta seccion puede conocerse la evolución del gasto en el tiempo"),
        ], width=12, className='tab-title'
        ), justify="center"
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

row1 = html.Tr([html.Td("Proveedor 1"), html.Td("00-00000000-0"),  html.Td("$1000")])
row2 = html.Tr([html.Td("Proveedor 2"), html.Td("00-00000000-0"),  html.Td("$1000")])
row3 = html.Tr([html.Td("Proveedor 3"), html.Td("00-00000000-0"),  html.Td("$1000")])
row4 = html.Tr([html.Td("Proveedor 4"), html.Td("00-00000000-0"),  html.Td("$1000")])

table_body = [html.Tbody([row1, row2, row3, row4])]

providersRankingTab = dbc.Container(children=[
    dbc.Row(
        dbc.Col([
            html.H5("Ranking de proveedores de acuerdo al gasto total"),
        ], width=12, className='tab-title'
        ), justify="center"
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

tabs = dbc.Tabs(
    [
        dbc.Tab(revenueTab, label="Datos por totales"),
        dbc.Tab(providersPaymentTab, label="Pago a proveedores"),
        dbc.Tab(expensesEvolutionTab, label="Evolución de los gastos"),
        dbc.Tab(providersRankingTab, label="Ranking proveedores")
    ]
)

app.layout = html.Div(children=[
    topNavBar,
    body,
    tabs])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
