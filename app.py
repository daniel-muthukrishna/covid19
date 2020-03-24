import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from urllib.request import urlopen
import numpy as np
from matplotlib import colors as mcolors
import datetime
import json
import copy

from get_data import get_data

colours = ['green', 'orange', 'blue', 'purple', 'pink', 'brown', 'cyan', 'red',
           'olive', '#FF1493', 'navy', '#aaffc3', 'lightcoral', '#228B22', '#aa6e28', '#FFA07A',
           ] + list(mcolors.CSS4_COLORS.keys())
monthsdict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

base_url = 'https://www.worldometers.info/coronavirus/country/'

popular_countries_data = {}
for i, country in enumerate(['australia', 'uk', 'us', 'italy', 'china']):
    print(country)
    url = base_url + country
    f = urlopen(url)
    webpage = f.read()
    dates, names, data = get_data(webpage)
    popular_countries_data[country] = {'dates': dates, 'titles': names, 'data': data}

app = dash.Dash(__name__)
server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

app.layout = html.Div(style={'backgroundColor': colors['background'], 'font-family': 'sans-serif'},
                      id='output-layout', children=[
    html.H1(
        children='COVID-19 Cases and Deaths',
        style={
            'textAlign': 'center',
            'color': colors['text'],
        }
    ),
    html.Hr(),
    html.Div([
        html.Div([
            html.Button(
                children='Plot',
                id='button-plot',
                type='submit',
                style={"margin": "15px", 'background-color': '#008CBA', 'color': 'white', 'width': '80%',
                       'height': '30px', 'font-size': '20px', 'border': 'None', 'border-radius': '10px'}
            ),
            html.I("Select countries of interest, then click the Plot button above.",
                   style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Checklist(
                id='australia',
                options=[{'label': "Australia", 'value': 'australia'}],
                value=['australia'],
                style={"margin-left": "15px", 'textAlign': 'left', 'margin-top': '10px'}
            ),
            dcc.Checklist(
                id='uk',
                options=[{'label': "UK", 'value': 'uk'}],
                value=['uk'],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='us',
                options=[{'label': "US", 'value': 'us'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='italy',
                options=[{'label': "Italy", 'value': 'italy'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='spain',
                options=[{'label': "Spain", 'value': 'spain'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='germany',
                options=[{'label': "Germany", 'value': 'germany'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='iran',
                options=[{'label': "Iran", 'value': 'iran'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='france',
                options=[{'label': "France", 'value': 'france'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='ireland',
                options=[{'label': "Ireland", 'value': 'ireland'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='china',
                options=[{'label': "China", 'value': 'china'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='south-korea',
                options=[{'label': "South Korea", 'value': 'south-korea'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='switzerland',
                options=[{'label': "Switzerland", 'value': 'switzerland'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='netherlands',
                options=[{'label': "Netherlands", 'value': 'netherlands'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='austria',
                options=[{'label': "Austria", 'value': 'austria'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='belgium',
                options=[{'label': "Belgium", 'value': 'belgium'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='norway',
                options=[{'label': "Norway", 'value': 'norway'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='sweden',
                options=[{'label': "Sweden", 'value': 'sweden'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='portugal',
                options=[{'label': "Portugal", 'value': 'portugal'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='brazil',
                options=[{'label': "Brazil", 'value': 'brazil'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='canada',
                options=[{'label': "Canada", 'value': 'canada'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='denmark',
                options=[{'label': "Denmark", 'value': 'denmark'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='malaysia',
                options=[{'label': "Malaysia", 'value': 'malaysia'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='poland',
                options=[{'label': "Poland", 'value': 'poland'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='greece',
                options=[{'label': "Greece", 'value': 'greece'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='indonesia',
                options=[{'label': "Indonesia", 'value': 'indonesia'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='philippines',
                options=[{'label': "Philippines", 'value': 'philippines'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='china-hong-kong-sar',
                options=[{'label': "Hong Kong", 'value': 'china-hong-kong-sar'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='iraq',
                options=[{'label': "Iraq", 'value': 'iraq'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left'}
            ),
            dcc.Checklist(
                id='algeria',
                options=[{'label': "Algeria", 'value': 'algeria'}],
                value=[],
                style={"margin-left": "15px", 'textAlign': 'left', 'margin-bottom': '500px'}
            ),
        ], style={'width': '17%', 'display': 'inline-block', 'vertical-align': 'top',
                  'background-color': 'lightgrey', 'horizontal-align': 'left', 'textAlign': 'center'}),
        html.Div(style={'width': '5%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                html.I("Fit exponential from:",
                       style={'textAlign': 'center', 'color': colors['text'], "margin-left": "15px", }),
                dcc.DatePickerSingle(
                    id='start-date',
                    min_date_allowed=datetime.date(2020, 1, 22),
                    max_date_allowed=datetime.date(2022, 1, 1),
                    initial_visible_month=datetime.date.today() - datetime.timedelta(days=7),
                    date=datetime.date.today() - datetime.timedelta(days=7),
                    style={'textAlign': 'center'}
                ),
            ], style={'display': 'inline-block', 'horizontal-align': 'center', 'textAlign': 'center'}),
            html.Div([
                html.I("Predict until:",
                       style={'textAlign': 'center', 'color': colors['text'], "margin-left": "15px", }),
                dcc.DatePickerSingle(
                    id='end-date',
                    min_date_allowed=datetime.date(2020, 1, 22),
                    max_date_allowed=datetime.date(2022, 1, 1),
                    initial_visible_month=datetime.date.today(),
                    date=datetime.date.today(),
                    style={'textAlign': 'center'}
                ),
            ], style={'display': 'inline-block', 'horizontal-align': 'center', 'textAlign': 'center',
                      "margin-bottom": "20px",}),
            dcc.Tabs([
                 dcc.Tab(label='linear', children=[
                    html.H2(children='Total Cases' ,style={'textAlign': 'center','color': colors['text']}),
                    dcc.Graph(id='infections-linear'),
                    html.H2(children='Total Deaths',style={'textAlign': 'center','color': colors['text']}),
                    dcc.Graph(id='deaths-linear'),
                    ]),
                dcc.Tab(label='log', children=[
                    html.H2(children='Total Cases', style={'textAlign': 'center', 'color': colors['text']}),
                    dcc.Graph(id='infections-log'),
                    html.H2(children='Total Deaths', style={'textAlign': 'center', 'color': colors['text']}),
                    dcc.Graph(id='deaths-log'),
                ]),
            ]),
        ], style={'width': '75%', 'display': 'inline-block', 'vertical-align': 'top', 'horizontal-align': 'center',
                  'textAlign': 'center', "margin-left": "0px"}),
        html.Hr(),
        html.Div(id='hidden-stored-data', style={'display': 'none'}),
        html.Footer(["Author: Daniel Muthukrishna. Data is taken from ",
                     html.A('https://www.worldometers.info/coronavirus/.', href='https://www.worldometers.info/coronavirus/'),
                     " ", html.A('Source code', href='https://github.com/daniel-muthukrishna/covid19.')],
                    style={'textAlign': 'center', 'color': colors['text']}),
    ], style={'horizontal-align': 'center', 'textAlign': 'center'}),
])


@app.callback([Output('infections-linear', 'figure'),
               Output('infections-log', 'figure'),
               Output('deaths-linear', 'figure'),
               Output('deaths-log', 'figure')],
              [Input('button-plot', 'n_clicks'),
               Input('start-date', 'date'),
               Input('end-date', 'date')],
              [State('australia', 'value'),
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
def update_plots(n_clicks, start_date, end_date, *args):
    print(n_clicks, start_date, end_date, args)
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    country_names = []
    for country in args:
        country_names.extend(country)

    country_data = copy.copy(popular_countries_data)
    for i, country in enumerate(country_names):
        if country not in country_data.keys():
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
                      # 'titlefont': {'size': 17},
                      # 'tickfont': {'size': 14},
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
                      # 'titlefont': {'size': 17},
                      # 'tickfont': {'size': 14},
                      },
            # 'xaxis': {'title': 'Time (days since trigger)', 'showgrid': True,
            #           'titlefont': {'size': 17},
            #           'tickfont': {'size': 14},
            #           },
            'showlegend': True,
        }
        for fig in [fig_linear, fig_log]:
            fig.append(go.Scatter(x=[datetime.date.today()],
                                  y=[0],
                                  mode='lines',
                                  line={'color': 'black', 'dash': 'dash'},
                                  showlegend=True,
                                  name=fr'Best exponential fits',
                                  yaxis='y1',
                                  legendgroup='group2', ))
            fig.append(go.Scatter(x=[datetime.date(2020, 2, 20)],
                                  y=[0],
                                  mode='lines+markers',
                                  line={'color': 'black'},
                                  showlegend=True,
                                  name=fr'COUNTRY : best fit (double time)',
                                  yaxis='y1',
                                  legendgroup='group2', ))

        for i, c in enumerate(country_names):
            title_index = country_data[c]['titles'].index(title)
            dates = country_data[c]['dates']
            xdata = np.arange(len(dates))
            ydata = country_data[c]['data'][title_index]
            ydata = np.array(ydata).astype('float')

            date_objects = []
            for date in dates:
                month, day = date.split()
                date_objects.append(datetime.date(year=2020, month=monthsdict[month], day=int(day)))
            date_objects = np.asarray(date_objects)

            model_date_mask = (date_objects <= end_date) & (date_objects >= start_date)

            model_dates = []
            model_xdata = []
            date = start_date
            d_idx = min(xdata[model_date_mask])
            while date <= end_date:
                model_dates.append(date)
                model_xdata.append(d_idx)
                date += datetime.timedelta(days=1)
                d_idx += 1
            model_xdata = np.array(model_xdata)

            b, logA = np.polyfit(xdata[model_date_mask], np.log(ydata[model_date_mask]), 1)
            # log_yfit = b * xdata[model_date_mask] + logA
            lin_yfit = np.exp(logA) * np.exp(b * model_xdata)

            for fig in [fig_linear, fig_log]:
                fig.append(go.Scatter(x=date_objects,
                                      y=ydata,
                                      mode='lines+markers',
                                      marker={'color': colours[i]},
                                      line={'color': colours[i]},
                                      showlegend=True,
                                      name=fr'{c.upper():<10s}: {np.exp(b):.2f}^t ({np.log(2) / b:.1f} days to double)',
                                      yaxis='y1',
                                      legendgroup='group1', ))
                fig.append(go.Scatter(x=model_dates,
                                      y=lin_yfit,
                                      mode='lines',
                                      line={'color': colours[i], 'dash': 'dash'},
                                      showlegend=False,
                                      name=fr'Model {c.upper():<10s}',
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
