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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
                server=server)
app.title = 'Visualizacion datos contratos publicos'

df = pd.read_csv('https://github.com/LucasLaPietra/WebScraperDatosConcepcion/blob/main/webscraping-app/contratos'
                 '/contratos-complete.csv?raw=true')

maxYear = df['Año'].max()
minYear = df['Año'].min()
maxFirstYearMonth = df[(df['Año'] == minYear)]['Mes'].max()
minFirstYearMonth = df[(df['Año'] == minYear)]['Mes'].min()
maxActualYearMonth = df[(df['Año'] == maxYear)]['Mes'].max()
minActualYearMonth = df[(df['Año'] == maxYear)]['Mes'].min()

topNavBar = html.Div(
    dbc.Row(
        [
            dbc.Col([
                dbc.Row(
                    [
                        html.H1(children='Visualización de datos'),
                        html.H1(children='de CONTRATOS PÚBLICOS'),
                        html.H3(children='de la Municipalidad de Concepción del Uruguay'),
                    ],
                    className='top-bar-top-row text-white'
                ),
                dbc.Row(
                    [
                        dbc.Col([
                            html.H1(children='DATOS'),
                            html.H3(children='CONCEPCIÓN'),
                        ], width=3, className='top-bar-bottom-row-column')

                    ],
                    className='top-bar-bottom-row text-white', justify="end"
                )

            ])
        ],
        align="center", className='top-bar'
    )
)

title = dbc.Container(
    children=[
        dbc.Row([html.H4("Actualmente la Municipalidad de Concepción del Uruguay informa en su sitio los siguentes "
                         "datos",
                         className='centered-subtitle'),
                 ], justify="center"
                )
    ], className="h-100 p-5 bg-light border rounded-3"
)

revenueTab = dbc.Container(children=[
    dbc.Row(
        [
            dbc.Col([
                html.H2('GASTOS DEL MUNICIPIO'),
                html.H5("En esta sección pueden conocerse los gastos del municipio en un período determinado"),
            ], className='tab-title'
            ),
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dcc.DatePickerRange(
                            id='dateRangeRevenue',
                            min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                            max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                            start_date=dt(maxYear, minActualYearMonth, 1).date(),
                            end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                            display_format='D/M/Y',
                            calendar_orientation='horizontal'),
                        width='auto', align='center')
                    ,
                    dbc.Col(
                        dbc.Button(html.I(className="bi bi-arrow-right"), color="primary",
                                   id='revenueDateButton'),
                        width='auto', align='center'
                    )

                ],
                    justify="end", className='date-row'
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            html.Span([html.I(className="bi bi-cloud-download"), "  Descargar Datos"]),
                            color="primary",
                            id='revenueDownloadButton'),
                        width='auto'),
                    justify="end"
                ),

                dcc.Download(id="revenueDownload"),
                dbc.Tooltip(
                    "Descargar datos sobre gastos del municipio en .csv",
                    target="revenueDownloadButton",
                ),

            ], className='date-col'
            )],
        justify="center"
    ),
    dbc.Spinner(size="lg",
                children=[
                    dbc.Row(
                        [
                            dbc.Col([
                                dbc.Card([
                                    html.H5("Total de órdenes de compra por:"),
                                    html.Img(src=app.get_asset_url("file-lines-solid.svg"), className='revenue-icon')
                                ], color="secondary", inverse=True, className='top-card'),
                                dbc.Card([
                                    html.H3(id='totalRevenue'),
                                ], color="secondary", inverse=True, className='bottom-card')
                            ], className='revenue-column', align="center", width='auto'
                            ),
                            dbc.Col([
                                dbc.Card([
                                    html.H5("Cantidad de proveedores:"),
                                    html.Img(src=app.get_asset_url("clipboard-solid.svg"), className='revenue-icon'),
                                ], color="secondary", inverse=True, className='top-card'),
                                dbc.Card([
                                    html.H3(id='totalProviders'),
                                ], color="secondary", inverse=True, className='bottom-card')
                            ], className='revenue-column', align="center", width='auto'
                            ),
                            dbc.Col([
                                dbc.Card([
                                    html.H5("Cantidad de órdenes de compra:"),
                                    html.Img(src=app.get_asset_url("dolly-solid.svg"), className='revenue-icon')
                                ], color="secondary", inverse=True, className='top-card'),
                                dbc.Card([
                                    html.H3(id='totalBuyOrders'),
                                ], color="secondary", inverse=True, className='bottom-card')
                            ], className='revenue-column', align="center", width='auto'
                            )]
                        , justify="center"
                    ), ])
], className="h-100 p-5 text-white bg-dark rounded-3")

providersPaymentTab = dbc.Container(children=[
    dbc.Row(
        [
            dbc.Col([
                html.H2('TOTAL DE CONTRATACIONES MEDIDO EN PESOS'),
                html.H5("En esta sección puede conocerse el dinero percibido por diferentes proveedores en un rubro"),
            ], className='tab-title'
            ),
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dcc.DatePickerRange(
                            id='dateRangeProvidersPayment',
                            min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                            max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                            start_date=dt(maxYear, minActualYearMonth, 1).date(),
                            end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                            display_format='D/M/Y',
                            calendar_orientation='horizontal'),
                        width='auto', align='center')
                    ,
                    dbc.Col(
                        dbc.Button(html.I(className="bi bi-arrow-right"), color="primary",
                                   id='providersPaymentDateButton'),
                        width='auto', align='center'
                    )

                ],
                    justify="end", className='date-row'
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            html.Span([html.I(className="bi bi-cloud-download"), "  Descargar Datos"]),
                            color="primary",
                            id='providersPaymentDownloadButton'),
                        width='auto'),
                    justify="end"
                ),

                dcc.Download(id="providersPaymentDownload"),
                dbc.Tooltip(
                    "Descargar datos sobre total de contrataciones en .csv",
                    target="providersPaymentDownloadButton",
                ),

            ], className='date-col'
            )],
        justify="center"
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
                    html.P('Cantidad de proveedores a mostrar:'),
                    dcc.Slider(min=1, max=20, step=1, value=20, id='providersPaymentSlider',
                               tooltip={"placement": "bottom", "always_visible": False})
                ], className='drop-down-col', width=4
            ),
        ]),
    dbc.Spinner(size="lg",
                children=[
                    dbc.Row([
                        dbc.Col(
                            html.Div([
                                dcc.Graph(id='providersPaymentGraph')
                            ]), width=10
                        ),
                    ], justify="center", align="center"
                    ), ])
], className="h-100 p-5 bg-light border rounded-3")

figExpensesEvolution = px.line(df, x="Nombre Fantasia", y="Importe", labels={
    "Nombre Fantasia": "proveedor",
    "Importe": "Dinero percibido",
})
figExpensesEvolution.data[0].line.color = "Red"

expensesEvolutionTab = dbc.Container(children=[
    dbc.Row(
        [
            dbc.Col([
                html.H2('EVOLUCION DEL GASTO POR RUBRO'),
                html.H5("En esta sección puede conocerse la evolución del gasto en el tiempo, seleccionando y"
                        " comparando entre uno o más rubros"),
            ], className='tab-title'
            ),
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dcc.DatePickerRange(
                            id='dateRangeExpensesEvolution',
                            min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                            max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                            start_date=dt(maxYear, minActualYearMonth, 1).date(),
                            end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                            display_format='D/M/Y',
                            calendar_orientation='horizontal'),
                        width='auto', align='center')
                    ,
                    dbc.Col(
                        dbc.Button(html.I(className="bi bi-arrow-right"), color="primary",
                                   id='expensesEvolutionDateButton'),
                        width='auto', align='center'
                    )

                ],
                    justify="end", className='date-row'
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            html.Span([html.I(className="bi bi-cloud-download"), "  Descargar Datos"]),
                            color="primary",
                            id='expensesEvolutionDownloadButton'),
                        width='auto'),
                    justify="end"
                ),

                dcc.Download(id="expensesEvolutionDownload"),
                dbc.Tooltip(
                    "Descargar datos sobre evolución del gasto en .csv",
                    target="expensesEvolutionDownloadButton",
                ),

            ], className='date-col'
            )],
        justify="center"
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                    html.P('Rubros a comparar:', id='expensesEvolutionDropDownTitle'),
                    dcc.Dropdown(
                        id='expensesEvolutionDropDown',
                        multi=True,
                        className='drop-down'
                    ),
                    dbc.Tooltip(
                        "Si no tiene rubros seleccionados se mostrara la evolucion general, pero puede seleccionar"
                        "uno o mas rubros para compararlos",
                        target="expensesEvolutionDropDownTitle",
                    ),
                ], className='drop-down-col'
            ),
        ]
    ),
    dbc.Spinner(size="lg",
                children=[
                    dbc.Row([
                        dbc.Col([
                            html.Div(dcc.Graph(id="expensesEvolutionGraph"))
                        ], width=10),
                    ]
                        , justify="center", align="center"
                    ), ])
], className="h-100 p-5 bg-light border rounded-3")

providersRankingTab = dbc.Container(children=[
    dbc.Row(
        [
            dbc.Col([
                html.H2('RANKING DE PROVEEDORES DE ACUERDO AL GASTO TOTAL'),
            ], className='tab-title'
            ),
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dcc.DatePickerRange(
                            id='dateRangeProvidersRanking',
                            min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                            max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                            start_date=dt(maxYear, minActualYearMonth, 1).date(),
                            end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                            display_format='D/M/Y',
                            calendar_orientation='horizontal'),
                        width='auto', align='center')
                    ,
                    dbc.Col(
                        dbc.Button(html.I(className="bi bi-arrow-right"), color="primary",
                                   id='providersRankingDateButton'),
                        width='auto', align='center'
                    )

                ],
                    justify="end", className='date-row'
                ),
            ], className='date-col'
            )],
        justify="center"
    ),
    dbc.Spinner(size="lg",
                children=[
                    dbc.Row(
                        justify="center", className='centered-table', id='providersRankingTable'
                    ), ])
], className="h-100 p-5 bg-light border rounded-3")

providersSearchTab = dbc.Container(children=[
    dbc.Row(
        [
            dbc.Col([
                html.H2('LISTADO DE PROVEEDORES'),
                html.H5("En esta sección puede buscarse un proveedor de acuerdo a una palabra clave"),
            ], className='tab-title'
            ),
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dcc.DatePickerRange(
                            id='dateRangeProvidersSearch',
                            min_date_allowed=dt(minYear, minFirstYearMonth, 1),
                            max_date_allowed=dt(maxYear, maxActualYearMonth, 31),
                            start_date=dt(maxYear, minActualYearMonth, 1).date(),
                            end_date=dt(maxYear, maxActualYearMonth, 31).date(),
                            display_format='D/M/Y',
                            calendar_orientation='horizontal'),
                        width='auto', align='center')
                    ,
                    dbc.Col(
                        dbc.Button(html.I(className="bi bi-arrow-right"), color="primary",
                                   id='providersSearchDateButton'),
                        width='auto', align='center'
                    )

                ],
                    justify="end", className='date-row'
                ),
            ], className='date-col'
            )],
        justify="center"
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Input(placeholder="Ingrese nombre o razón social del proveedor",
                              type="text",
                              id="providersSearchInput",
                              value="")
                ], className='drop-down', width=4
            )
        ], justify="center", className='title-row'
    ),
    dbc.Spinner(size="lg",
                children=[
                    dbc.Row(justify="center", className='centered-table', id='providersSearchTable'), ])
], className="h-100 p-5 bg-light border rounded-3")

footer = dbc.Row(
    dbc.Col(
        [
            html.Img(src=app.get_asset_url('logo.png'), className='footer-logo'),
            html.H3(['UN PROYECTO DE ', html.B('DATOS CONCEPCIÓN')], className='footer-title'),
            html.H5('Argentina - Latam', className='footer-subtitle'),
            html.H5(['Aplicación desarrollada por ',
                     html.A('Lucas La Pietra',
                            href='https://www.linkedin.com/in/lucas-la-pietra-0b1ab6194/')
                     ], className='footer-subtitle'),
            dbc.Row([
                dbc.Col(
                    html.A(html.Img(src=app.get_asset_url("facebook.svg"), className='footer-social-icon'),
                           href='https://m.facebook.com/datosconcepcion22/'),
                    width=1),
                dbc.Col(html.A(html.Img(src=app.get_asset_url("twitter.svg"), className='footer-social-icon'),
                               href='https://twitter.com/DataConcepcion?t=eLjVH-ZLjYTt8DXltbuHqQ&s=08 '),
                        width=1),
                dbc.Col(
                    html.A(html.Img(src=app.get_asset_url("instagram.svg"), className='footer-social-icon'),
                           href='https://instagram.com/datos.concepcion?utm_medium=copy_link'),
                    width=1),
                dbc.Col(
                    html.A(html.Img(src=app.get_asset_url("github.svg"), className='footer-social-icon'),
                           href='https://github.com/LucasLaPietra/WebScraperDatosConcepcion'),
                    width=1),
                dbc.Col(
                    html.A(html.Img(src=app.get_asset_url("mail.svg"), className='footer-social-icon'),
                           href='mailto: datosconcepcion22@gmail.com'),
                    width=1)
            ], className='footer-social-row', justify="center")
        ]
    ), className='bg-dark footer-row text-white', justify="center"
)

body = html.Div(
    [
        dbc.Row(dbc.Col(revenueTab), className="app-container"),
        dbc.Row(dbc.Col(providersPaymentTab), className="app-container"),
        dbc.Row(dbc.Col(providersRankingTab), className="app-container"),
        dbc.Row(dbc.Col(expensesEvolutionTab), className="app-container"),
        dbc.Row(dbc.Col(providersSearchTab), className="app-container")
    ]
)

app.layout = html.Div(children=[
    topNavBar,
    title,
    body,
    footer
])


@app.callback(
    [Output('totalRevenue', 'children'), Output('totalProviders', 'children'), Output('totalBuyOrders', 'children'),
     Output("revenueDownload", "data")],
    [Input('dateRangeRevenue', 'start_date'), Input('dateRangeRevenue', 'end_date'),
     Input('revenueDownloadButton', 'n_clicks'), Input('revenueDateButton', 'n_clicks')]
)
def update_figure(initial_date, final_date, button, date_button):
    ctx = dash.callback_context
    initial_date = dt.strptime(re.split('T| ', initial_date)[0], '%Y-%m-%d')
    final_date = dt.strptime(re.split('T| ', final_date)[0], '%Y-%m-%d')
    filtered_df = utils.filter_by_date(df, initial_date, final_date)
    revenue_data = utils.revenue_data(filtered_df)
    if ctx.triggered[0]['prop_id'] == 'revenueDownloadButton.n_clicks':
        df_to_download = pd.DataFrame({'Metrica':
                                           ['Total de ordenes de compra por',
                                            'Cantidad de proveedores',
                                            'Cantidad de ordenes de compra'],
                                       'Valor': revenue_data})
        return "$" + str('{0:,}'.format(revenue_data[0])), '{0:,}'.format(revenue_data[1]), '{0:,}'.format(
            revenue_data[2]), dcc.send_data_frame(df_to_download.to_csv, "data.csv")
    else:
        if (ctx.triggered[0]['prop_id'] != 'dateRangeRevenue.start_date') and \
                (ctx.triggered[0]['prop_id'] != 'dateRangeRevenue.end_date'):
            return "$" + str('{0:,}'.format(revenue_data[0])), '{0:,}'.format(revenue_data[1]), '{0:,}'.format(
                revenue_data[2]), dash.no_update
        else:
            dash.no_update, dash.no_update, dash.no_update, dash.no_update


@app.callback([Output('providersPaymentGraph', 'figure'), Output('providersPaymentDropDown', 'options'),
               Output("providersPaymentDownload", "data"), Output("providersPaymentSlider", "max")],
              [Input('dateRangeProvidersPayment', 'start_date'), Input('dateRangeProvidersPayment', 'end_date'),
               Input('providersPaymentDropDown', 'value'), Input('providersPaymentSlider', 'value'),
               Input('providersPaymentDownloadButton', 'n_clicks'), Input('providersPaymentDateButton', 'n_clicks')]
              )
def update_figure(initial_date, final_date, category, slider, button, date_button):
    ctx = dash.callback_context
    initial_date = dt.strptime(re.split('T| ', initial_date)[0], '%Y-%m-%d')
    final_date = dt.strptime(re.split('T| ', final_date)[0], '%Y-%m-%d')
    filtered_df = utils.filter_by_date(df, initial_date, final_date)
    df_providers_payment = utils.make_providers_payment_df(filtered_df)
    categories = set(df_providers_payment['Rubro'])
    dict_filter = [{'label': i.capitalize(), 'value': i} for i in categories]
    dict_filter.append({'label': "Ninguno", 'value': "None"})
    df_filtered_by_category = utils.filter_by_category(df_providers_payment, category)
    df_limited = df_filtered_by_category.nlargest(slider, 'Importe')
    fig_providers_payment = px.bar(df_limited, x="Importe", y="Nombre Fantasia", labels={
        "Nombre Fantasia": "proveedor",
        "Importe": "Dinero percibido",
    }, color_continuous_scale="Viridis", color="Importe", orientation='h')

    if ctx.triggered[0]['prop_id'] == 'providersPaymentDownloadButton.n_clicks':
        return fig_providers_payment, dict_filter, dcc.send_data_frame(df_limited.to_csv, "data.csv"), \
               len(df_filtered_by_category)
    else:
        if (ctx.triggered[0]['prop_id'] != 'dateRangeProvidersPayment.start_date') and \
                (ctx.triggered[0]['prop_id'] != 'dateRangeProvidersPayment.end_date'):
            return fig_providers_payment, dict_filter, dash.no_update, len(df_filtered_by_category)
        else:
            return dash.no_update, dict_filter, dash.no_update, len(df_filtered_by_category)


@app.callback([Output('expensesEvolutionGraph', 'figure'), Output('expensesEvolutionDropDown', 'options'),
               Output("expensesEvolutionDownload", "data")],
              [Input('dateRangeExpensesEvolution', 'start_date'), Input('dateRangeExpensesEvolution', 'end_date'),
               Input('expensesEvolutionDropDown', 'value'), Input('expensesEvolutionDownloadButton', 'n_clicks'),
               Input('expensesEvolutionDateButton', 'n_clicks')]
              )
def update_figure(initial_date, final_date, selected_categories, button, date_button):
    ctx = dash.callback_context
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
    else:
        df_categories_filtered = filtered_df[filtered_df['Rubro'].isin(selected_categories)]
        df_new = utils.make_expenses_evolution_df(df_categories_filtered, True)
        fig_expenses_evolution = px.line(df_new, x="date", y="Importe", color="Rubro", labels={
            "date": "Fecha",
            "Importe": "Dinero",
        })
    if ctx.triggered[0]['prop_id'] == 'expensesEvolutionDownloadButton.n_clicks':
        return fig_expenses_evolution, dict_filter, dcc.send_data_frame(df_new.to_csv, "data.csv")
    else:
        if (ctx.triggered[0]['prop_id'] != 'dateRangeExpensesEvolution.start_date') and \
                (ctx.triggered[0]['prop_id'] != 'dateRangeExpensesEvolution.end_date'):
            return fig_expenses_evolution, dict_filter, dash.no_update
        else:
            return dash.no_update, dict_filter, dash.no_update


@app.callback(Output('providersRankingTable', 'children'),
              [Input('dateRangeProvidersRanking', 'start_date'), Input('dateRangeProvidersRanking', 'end_date'),
               Input('providersRankingDateButton', 'n_clicks')]
              )
def update_figure(initial_date, final_date, date_button):
    ctx = dash.callback_context
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
    if (ctx.triggered[0]['prop_id'] != 'dateRangeProvidersRanking.start_date') and \
            (ctx.triggered[0]['prop_id'] != 'dateRangeProvidersRanking.end_date'):
        return table
    else:
        return dash.no_update


@app.callback(Output('providersSearchTable', 'children'),
              [
                  Input('dateRangeProvidersSearch', 'start_date'),
                  Input('dateRangeProvidersSearch', 'end_date'),
                  Input("providersSearchInput", "value"),
                  Input('providersSearchDateButton', 'n_clicks')
              ]
              )
def update_figure(initial_date, final_date, search_input, date_button):
    ctx = dash.callback_context
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
    if (ctx.triggered[0]['prop_id'] != 'dateRangeProvidersSearch.start_date') and \
            (ctx.triggered[0]['prop_id'] != 'dateRangeProvidersSearch.end_date'):
        return table
    else:
        return dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
