import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from urllib.request import urlopen
import numpy as np
from matplotlib import colors as mcolors


from backend import get_data

colours = ['green', 'orange', 'red', 'blue', 'purple', 'pink', 'brown', 'cyan',
           'olive', '#FF1493', 'navy', '#aaffc3', 'lightcoral', '#228B22', '#aa6e28', '#FFA07A',
           ] + list(mcolors.CSS4_COLORS.keys())

base_url = 'https://www.worldometers.info/coronavirus/country/'

app = dash.Dash(__name__)
server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}
N_CLICKS = 0

app.layout = html.Div(style={'backgroundColor': colors['background']}, id='output-layout', children=[
    html.H1(
        children='COVID-19 Cases and Deaths',
        style={
            'textAlign': 'center',
            'color': colors['text'],
        }
    ),

    # html.Div(children='', style={
    #     'textAlign': 'center',
    #     'color': colors['text'],
    #     'fontSize': 30
    # }),

    html.Hr(),

    html.Div([
        html.Div([
            html.Button(
                children='Plot',
                id='button-plot',
                type='submit',
                style={"margin": "15px", 'background-color': '#008CBA', 'color': 'white', 'width': '80%',
                       'height':'30px', 'font-size': '20px'}
            ),
            dcc.Checklist(
                id='australia',
                options=[{'label': "Australia", 'value': 'australia'}],
                value=['australia'],
                style={"margin-left": "15px",}
            ),
            dcc.Checklist(
                id='uk',
                options=[{'label': "UK", 'value': 'uk'}],
                value=['uk'],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='us',
                options=[{'label': "US", 'value': 'us'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='italy',
                options=[{'label': "Italy", 'value': 'italy'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='spain',
                options=[{'label': "Spain", 'value': 'spain'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='germany',
                options=[{'label': "germany", 'value': 'germany'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='iran',
                options=[{'label': "iran", 'value': 'iran'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='france',
                options=[{'label': "france", 'value': 'france'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='ireland',
                options=[{'label': "ireland", 'value': 'ireland'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='china',
                options=[{'label': "china", 'value': 'china'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='south-korea',
                options=[{'label': "south-korea", 'value': 'south-korea'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='switzerland',
                options=[{'label': "switzerland", 'value': 'switzerland'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='netherlands',
                options=[{'label': "netherlands", 'value': 'netherlands'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='austria',
                options=[{'label': "austria", 'value': 'austria'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='belgium',
                options=[{'label': "belgium", 'value': 'belgium'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='norway',
                options=[{'label': "norway", 'value': 'norway'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='sweden',
                options=[{'label': "sweden", 'value': 'sweden'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='portugal',
                options=[{'label': "portugal", 'value': 'portugal'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='brazil',
                options=[{'label': "brazil", 'value': 'brazil'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='canada',
                options=[{'label': "canada", 'value': 'canada'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='denmark',
                options=[{'label': "denmark", 'value': 'denmark'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='malaysia',
                options=[{'label': "malaysia", 'value': 'malaysia'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='poland',
                options=[{'label': "poland", 'value': 'poland'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='greece',
                options=[{'label': "greece", 'value': 'greece'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='indonesia',
                options=[{'label': "indonesia", 'value': 'indonesia'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='philippines',
                options=[{'label': "philippines", 'value': 'dphilippinesummy'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='china-hong-kong-sar',
                options=[{'label': "hong kong", 'value': 'dchina-hong-kong-sarummy'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='iraq',
                options=[{'label': "iraq", 'value': 'iraq'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='algeria',
                options=[{'label': "algeria", 'value': 'algeria'}],
                value=[],
                style={"margin-left": "15px", }
            ),

            html.I("Lookback time:", style={'textAlign': 'center', 'color': colors['text'], "margin-left": "15px",}),
            dcc.Input(
                id='lookback-time',
                placeholder='Lookback time for model (in days)',
                value='-10',
                style={
                    'width': '70%',
                    'height': '20px',
                    "lineHeight": "20px",
                    "margin-left": "15px",
                },
            ),
        ], style={'width': '15%', 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='linear', children=[
                        dcc.Graph(id='infections-linear'),
                        dcc.Graph(id='deaths-linear'),
                        ]),
                    dcc.Tab(label='log', children=[
                        dcc.Graph(id='infections-log'),
                        dcc.Graph(id='deaths-log'),
                    ]),
                ]),
            ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Hr(),
        html.Footer("Author: Daniel Muthukrishna. Data is taken from https://www.worldometers.info/coronavirus/",
                    style={'textAlign': 'center', 'color': colors['text']}),
    ]),
])


@app.callback([Output('infections-linear', 'figure'),
               Output('infections-log', 'figure'),
               Output('deaths-linear', 'figure'),
               Output('deaths-log', 'figure')],
              [Input('button-plot', 'n_clicks')],
              [State('lookback-time', 'value'),
               State('australia', 'value'),
               State('uk', 'value'),
               State('us', 'value'),
               State('italy', 'value'),
               State('spain', 'value'),
               State('germany', 'value'),
               State('iran', 'value'),
               State('france', 'value'),
               State('ireland', 'value'),
               State('china', 'value'),
               State('south-korea', 'value'),
               State('switzerland', 'value'),
               State('netherlands', 'value'),
               State('austria', 'value'),
               State('belgium', 'value'),
               State('norway', 'value'),
               State('sweden', 'value'),
               State('portugal', 'value'),
               State('brazil', 'value'),
               State('canada', 'value'),
               State('denmark', 'value'),
               State('malaysia', 'value'),
               State('poland', 'value'),
               State('greece', 'value'),
               State('indonesia', 'value'),
               State('philippines', 'value'),
               State('china-hong-kong-sar', 'value'),
               State('iraq', 'value'),
               State('algeria', 'value')])
def update_infections_plot(n_clicks, lookback_time, *args):
    print(n_clicks, lookback_time, args)
    country_names = []
    for country in args:
        country_names.extend(country)
    country_data = {}
    for i, country in enumerate(country_names):
        url = base_url + country

        f = urlopen(url)
        webpage = f.read()

        dates, names, data = get_data(webpage)

        country_data[country] = {'dates': dates, 'titles': names, 'data': data}

    out = []
    for title in ['Cases', 'Deaths']:
        fig_linear = []
        fig_log = []

        layout_linear = {
            # 'height': 375,
            # 'margin': {'l': 45, 'b': 30, 'r': 10, 't': 10},
            'yaxis': {'title': title, 'type': 'linear', 'showgrid': True,
                      'titlefont': {'size': 17},
                      'tickfont': {'size': 14},
                      },
            # 'xaxis': {'title': 'Time (days since trigger)', 'showgrid': True,
            #           'titlefont': {'size': 17},
            #           'tickfont': {'size': 14},
            #           },
            'showlegend': True,
        }
        layout_log = {
            # 'height': 375,
            # 'margin': {'l': 45, 'b': 30, 'r': 10, 't': 10},
            'yaxis': {'title': title, 'type': 'log', 'showgrid': True,
                      'titlefont': {'size': 17},
                      'tickfont': {'size': 14},
                      },
            # 'xaxis': {'title': 'Time (days since trigger)', 'showgrid': True,
            #           'titlefont': {'size': 17},
            #           'tickfont': {'size': 14},
            #           },
            'showlegend': True,
        }

        for i, c in enumerate(country_names):
            print(c)
            title_index = country_data[c]['titles'].index(title)
            dates = country_data[c]['dates']
            xdata = np.arange(len(dates))
            ydata = country_data[c]['data'][title_index]
            ydata = np.array(ydata).astype('float')

            sidx = int(lookback_time)
            b, logA = np.polyfit(xdata[sidx:], np.log(ydata[sidx:]), 1)
            log_yfit = b * xdata[sidx:] + logA
            lin_yfit = np.exp(logA) * np.exp(b * xdata[sidx:])

            fig_linear.append(go.Scatter(x=dates,
                                  y=ydata,
                                  mode='lines+markers',
                                  marker={'color': colours[i]},
                                  line={'color': colours[i]},
                                  showlegend=True,
                                  name=fr'{c.upper():<10s}: {np.exp(b):.2f}^t ({np.log(2) / b:.1f} days to double)',
                                  yaxis='y1',
                                  legendgroup='group1', ))
            fig_linear.append(go.Scatter(x=dates[sidx:],
                                  y=lin_yfit,
                                  mode='lines',
                                  line={'color': colours[i], 'dash': 'dash'},
                                  showlegend=False,
                                  yaxis='y1',
                                  legendgroup='group1', ))


            fig_log.append(go.Scatter(x=dates,
                                  y=ydata,
                                  mode='lines+markers',
                                  marker={'color': colours[i]},
                                  line={'color': colours[i]},
                                  showlegend=True,
                                  name=fr'{c.upper():<10s}: {np.exp(b):.2f}^t ({np.log(2) / b:.1f} days to double)',
                                  yaxis='y1',
                                  legendgroup='group1', ))
            fig_log.append(go.Scatter(x=dates[sidx:],
                                  y=lin_yfit,
                                  mode='lines',
                                  line={'color': colours[i], 'dash': 'dash'},
                                  showlegend=False,
                                  yaxis='y1',
                                  legendgroup='group1', ))
        out.append({'data': fig_linear, 'layout': layout_linear})
        out.append({'data': fig_log, 'layout': layout_log})

    return out


# Dash CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

if __name__ == '__main__':
    app.run_server(debug=True)
