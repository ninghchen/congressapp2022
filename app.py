from datetime import date
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dateutil import parser

state_NE = ['VT', 'NH', 'ME', 'MA', 'RI', 'CT', 'PA', 'MD', 'DE', 'DC', 'WV', 'VA', 'NY', 'NJ']
state_MW = ['ND', 'SD', 'NE', 'MN', 'IA', 'WI', 'IL', 'MI', 'IN', 'OH']
state_S = ['KY', 'TN', 'NC', 'MS', 'AL', 'GA', 'SC', 'FL', 'NM', 'OK', 'AR', 'TX', 'LA']
state_W = ['MT', 'WY', 'UT', 'CO', 'KS', 'MO', 'WA', 'OR', 'IDD', 'CA', 'NV', 'AZ']

states = state_NE + state_MW + state_S + state_W
states.sort()
states = ['US'] + states

def str2date(d):
    return parser.parse(d).date()

df_bread = pd.read_csv('Bread.csv')
df_bread['Month'] = df_bread['Month'].apply(str2date)
df_chicken = pd.read_csv('Chicken.csv')
df_chicken['Month'] = df_chicken['Month'].apply(str2date)
df_electricity = pd.read_csv('Electricity.csv')
df_electricity['Month'] = df_electricity['Month'].apply(str2date)
df_gas = pd.read_csv('Gas.csv')
df_gas['Month'] = df_gas['Month'].apply(str2date)
df_milk = pd.read_csv('Milk.csv')
df_milk['Month'] = df_milk['Month'].apply(str2date)
df_orange = pd.read_csv('Orange.csv')
df_orange['Month'] = df_orange['Month'].apply(str2date)

df_ir_bread = pd.read_csv('IR_bread.csv')
df_ir_chicken = pd.read_csv('IR_chicken.csv')
df_ir_electricity = pd.read_csv('IR_electricity.csv')
df_ir_gas = pd.read_csv('IR_gas.csv')
df_ir_milk = pd.read_csv('IR_milk.csv')
df_ir_orange = pd.read_csv('IR_orange.csv')
df_ir_bread['Month'] = df_ir_bread['Month'].apply(str2date)
df_ir_chicken['Month'] = df_ir_chicken['Month'].apply(str2date)
df_ir_electricity['Month'] = df_ir_electricity['Month'].apply(str2date)
df_ir_gas['Month'] = df_ir_gas['Month'].apply(str2date)
df_ir_milk['Month'] = df_ir_milk['Month'].apply(str2date)
df_ir_orange['Month'] = df_ir_orange['Month'].apply(str2date)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

def get_region(state):
    if state in state_NE:
        return 'NE'
    if state in state_MW:
        return 'MW'
    if state in state_S:
        return 'S'
    if state in state_W:
        return 'W'

    return 'US'

def get_title():
    return html.Div([
        dbc.Container([
            html.Div([
                html.Div(children="Inflation Rate", className="header-title"),
            ], className = 'title-container')
        ])
    ])

def get_state():
    options = [{'label':state, 'value':state} for state in states]
    return dbc.Select(
        id = 'state',
        options = options,
        value = 'US'
    )

def get_left():
    return html.Div([
        dbc.Container([
            dbc.Row(
                dbc.Button("Query", id = 'query', color="primary", className="md-1"),
            ),
            dbc.Row(html.Br()),
            dbc.Row(html.Hr()),
            dbc.Row(html.P('Select Month')),
            dbc.Row([
                dbc.Col(md = 2),
                dbc.Col(dcc.DatePickerSingle(
                id='start-date',
                min_date_allowed=date(2012, 1, 1),
                max_date_allowed=date(2022, 9, 1),
                initial_visible_month=date(2019, 12, 1),
                date=date(2019, 12, 1),
            ))
            ]),
            dbc.Row(html.Br()),
            dbc.Row([
                dbc.Col(html.Div(), md = 2),
                dbc.Col(html.P("VS"))]),
            dbc.Row(dcc.DatePickerSingle(
                id='end-date',
                min_date_allowed=date(2012, 1, 1),
                max_date_allowed=date(2022, 9, 1),
                initial_visible_month=date(2019, 12, 1),
                date=date(2022, 9, 1),
            )),
            dbc.Row(html.Br()),
            dbc.Row(html.Hr()),
            dbc.Row(html.P('Select State')),
            dbc.Row(get_state())
        ])
    ])

def get_bread(ir):
    return html.Div(
        dbc.Row([
            dbc.Col(html.Img(src = 'assets/bread2.jpeg'), md=4),
            dbc.Col(html.Div(), md = 1),
            dbc.Col(html.Label('%.1f'%ir), md = 2),
            dbc.Col(html.Label('%'), md = 1)
        ]), className = 'my-4'
    )

def get_chicken(ir):
    return html.Div(
        dbc.Row([
            dbc.Col(html.Img(src = 'assets/chicken.jpeg'), md=4),
            dbc.Col(html.Div(), md = 1),
            dbc.Col(html.Label('%.1f'%ir), md = 2),
            dbc.Col(html.Label('%'), md = 1)
        ]), className = 'my-4'
    )

def get_electricity(ir):
    return html.Div(
        dbc.Row([
            dbc.Col(html.Img(src = 'assets/electricity.jpeg'), md=4),
            dbc.Col(html.Div(), md = 1),
            dbc.Col(html.Label('%.1f'%ir), md = 2),
            dbc.Col(html.Label('%'), md = 1)
        ]), className = 'my-4'
    )

def get_gasoline(ir):
    return html.Div(
        dbc.Row([
            dbc.Col(html.Img(src = 'assets/gasoline.png'), md=4),
            dbc.Col(html.Div(), md = 1),
            dbc.Col(html.Label('%.1f'%ir), md = 2),
            dbc.Col(html.Label('%'), md = 1)
        ]), className = 'my-4'
    )

def get_milk(ir):
    return html.Div(
        dbc.Row([
            dbc.Col(html.Img(src = 'assets/milk.jpeg'), md=4),
            dbc.Col(html.Div(), md = 1),
            dbc.Col(html.Label('%.1f'%ir), md = 2),
            dbc.Col(html.Label('%'), md = 1)
        ]), className = 'my-4'
    )

def get_orange(ir):
    return html.Div(
        dbc.Row([
            dbc.Col(html.Img(src = 'assets/orange.jpeg'), md=4),
            dbc.Col(html.Div(), md = 1),
            dbc.Col(html.Label('%.1f'%ir), md = 2),
            dbc.Col(html.Label('%'), md = 1)
        ]), className = 'my-4'
    )

def get_items(ir_bread, ir_chicken, ir_electricity, ir_gas, ir_milk, ir_orange):
    return [
            dbc.Col(get_bread(ir_bread), md=4),
            dbc.Col(get_chicken(ir_chicken), md=4),
            dbc.Col(get_electricity(ir_electricity), md=4),
            dbc.Col(get_gasoline(ir_gas), md=4),
            dbc.Col(get_milk(ir_milk), md=4),
            dbc.Col(get_orange(ir_orange), md=4)
        ]

def get_right():
    return html.Div([
        dbc.Row(id = 'item-row'),
        dbc.Row(id = 'inflation-plot')
    ], id = 'right')

def get_content():
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(get_left(), md = 2),
                dbc.Col(get_right(), md = 10)
            ])
        ])
    ])

def get_value(df, date, region):
    #print(df[df['Month'] == date], region)
    #print(df[df['Month'] == date][region])
    date = date.replace(day=1)
    return df[df['Month'] == date][region].iloc[0]

def get_ir(c_current, c_base):
    return (c_current-c_base)/c_base*100

def get_inflation_plot(region):
    return html.Div([
        html.Label('Monthly Inflation Rate Plots', className = 'sub-title'),
        dcc.Graph(figure = get_inflation_fig(region))
    ])

def get_inflation_fig(region):
    fig = go.Figure()
    trace = go.Scatter(x=df_ir_bread['Month'], y=df_ir_bread[region], mode='lines+markers', name='Bread')
    fig.add_trace(trace)

    trace = go.Scatter(x=df_ir_chicken['Month'], y=df_ir_chicken[region], mode='lines+markers', name = 'Chicken')
    fig.add_trace(trace)

    trace = go.Scatter(x=df_ir_electricity['Month'], y=df_ir_electricity[region], mode='lines+markers', name = 'Electricity')
    fig.add_trace(trace)

    trace = go.Scatter(x=df_ir_gas['Month'], y=df_ir_gas[region], mode='lines+markers', name = 'Gasoline')
    fig.add_trace(trace)

    trace = go.Scatter(x=df_ir_milk['Month'], y=df_ir_milk[region], mode='lines+markers', name = 'Milk')
    fig.add_trace(trace)

    trace = go.Scatter(x=df_ir_orange['Month'], y=df_ir_orange[region], mode='lines+markers', name = 'Orange')
    fig.add_trace(trace)

    fig.update_layout(
        font_color='silver',
        xaxis_title = 'years',
        yaxis_title = 'inflation rate',
        margin=dict(
            l=0,

            r=0,

            b=100,

            t=0,

            pad=0
        ),
            paper_bgcolor='white',
            plot_bgcolor='white',
    )

    return fig

def get_info():
    return html.Div(
        dbc.Row([
            dbc.Col(md=11),
            dbc.Col(dbc.Button("?", id = 'info', outline=True, color="primary"), md=1),
            dbc.Offcanvas([
                html.H5('Goal', className = 'sub-title'),
                html.P(
                    "Enable users to recognize the inflation rate of specific necessary items in their daily life, help them adjust cost habits", className = 'paragraph'),
                html.H5('Data', className = 'sub-title'),
                html.Label('Data source', className = 'sub-title'),
                html.P('Downloaded from U.S. BUREAU OF LABOR STATISTICS, https://data.bls.gov/PDQWeb/ap', className = 'paragraph'),
                html.Label('Data description', className = 'sub-title'),
                html.P('U.S. BUREAU OF LABOR publishes item prices monthly. It splits US into five regions geographically and calculate average prices. North and East region contains "VT", "NH", "ME", "MA", "RI", "CT", "PA", "MD", "DE", "DC", "WV", "VA", "NY", "NJ"; Midwest region contains "ND", "SD", "NE", "MN", "IA", "WI", "IL", "MI", "IN", "OH"; South region contains "KY", "TN", "NC", "MS", "AL", "GA", "SC", "FL", "NM", "OK", "AR", "TX", "LA"; West region contains "MT", "WY", "UT", "CO","KS","MO", "WA", "OR", "IDD", "CA", "NV", "AZ"', className = 'paragraph'),
                html.Label('Data processing', className = 'sub-title'),
                html.Div(
                    dbc.Row([
                        dbc.Col(md=4),
                        dbc.Col(html.Img(src = 'assets/Inflation.png'), md=6)
                    ])
                ),
                html.P('The raw data downloaded are kind of unstructured which are organized by year and month with raw data info for each region in xlsx. In order to use the data directly in the app, the 30 raw data files were processed and generated 6 processed csv files in which each csv file for one item.', className = 'paragraph'),
                html.P('Some of the data points were missed in the raw data. They were replaced withe value of the previous month', className = 'paragraph'),
                html.Label('Inflation Rate (IR) Formula', className = 'sub-title'),
                html.P('IR = (cost_2 - cost_1)/cost_1*100', className = 'paragraph'),
                html.Label('App Layout', className = 'sub-title'),
                html.Div(
                    dbc.Row([
                        dbc.Col(md=2),
                        dbc.Col(html.Img(src = 'assets/Layout.png'), md=8)
                    ])
                ),
                html.H5('Reference', className='sub-title'),
                html.P(html.A('1. BLS', href='https://data.bls.gov/PDQWeb/ap'), className = 'paragraph'),
                html.P(html.A('2. Wiki', href = 'https://en.wikipedia.org/wiki/Consumer_price_index'), className = 'paragraph')
                ],
                id="offcanvas",
                title="SUMMARY",
                is_open=False,
                placement = 'end', # start (left, default), end (right), top, bottom
                scrollable=True,
                #close_button=False, # disable close button
                #backdrop="static", # disable closing by click outside canvas
                #keyboard=False # disable escape key
                class_name = 'w-75'
            ),
        ]
        )
    )

app.layout = html.Div([
    get_title(),
    get_info(),
    get_content()
    ])

@app.callback(
    Output("offcanvas", "is_open"),
    Input("info", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("item-row", "children"),
    Output('inflation-plot', 'children'),
    Input("query", "n_clicks"),
    State('start-date', 'date'),
    State('end-date', 'date'),
    State('state', 'value')
)
def update_item_row(n, s_date, e_date, state):
    if not n:
        raise PreventUpdate
    s_date = parser.parse(s_date).date()
    e_date = parser.parse(e_date).date()
    region = get_region(state)

    ir_bread = get_ir(get_value(df_bread, e_date, region), get_value(df_bread, s_date, region))
    ir_chicken = get_ir(get_value(df_chicken, e_date, region), get_value(df_chicken, s_date, region))
    ir_electricity = get_ir(get_value(df_electricity, e_date, region), get_value(df_electricity, s_date, region))
    ir_gas = get_ir(get_value(df_gas, e_date, region), get_value(df_gas, s_date, region))
    ir_milk = get_ir(get_value(df_milk, e_date, region), get_value(df_milk, s_date, region))
    ir_orange = get_ir(get_value(df_orange, e_date, region), get_value(df_orange, s_date, region))

    return get_items(ir_bread, ir_chicken, ir_electricity, ir_gas, ir_milk, ir_orange), get_inflation_plot(region)

if __name__ == '__main__':
    app.run_server(debug=True)
