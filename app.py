import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from matplotlib import colors as mcolors
import datetime
import json

from get_data import get_data
from constants import POPULATIONS

colours = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf',
           'blue', 'purple', 'pink', 'cyan', '#FF1493', 'navy', '#aaffc3', '#228B22', '#aa6e28', '#FFA07A',
           ] + list(mcolors.CSS4_COLORS.keys())

COUNTRY_LIST = ['world',
                'uk',
                'us',
                'italy',
                'spain',
                'germany',
                'iran',
                'france',
                'australia',
                'albania',
                'algeria',
                'andorra',
                'argentina',
                'armenia',
                'austria',
                'bahrain',
                'belgium',
                'bosnia and herzegovina',
                'brazil',
                'brunei',
                'bulgaria',
                'burkina faso',
                'canada',
                'chile',
                'china',
                'colombia',
                'costa rica',
                'croatia',
                'cyprus',
                'czechia',
                'denmark',
                'dominican republic',
                'ecuador',
                'egypt',
                'estonia',
                'finland',
                'greece',
                'hungary',
                'iceland',
                'india',
                'indonesia',
                'iraq',
                'ireland',
                'israel',
                'japan',
                'jordan',
                'kuwait',
                'latvia',
                'lebanon',
                'lithuania',
                'luxembourg',
                'malaysia',
                'malta',
                'mexico',
                'moldova',
                'morocco',
                'netherlands',
                'new zealand',
                'north macedonia',
                'norway',
                'pakistan',
                'panama',
                'peru',
                'philippines',
                'poland',
                'portugal',
                'qatar',
                'romania',
                'russia',
                'south-korea',
                'san marino',
                'saudi arabia',
                'serbia',
                'singapore',
                'slovakia',
                'slovenia',
                'south africa',
                'sri lanka',
                'sweden',
                'switzerland',
                'taiwan',
                'thailand',
                'tunisia',
                'turkey',
                'united arab emirates',
                'ukraine',
                'uruguay',
                'vietnam',]
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

app.layout = html.Div(style={'backgroundColor': colors['background'], 'font-family': 'sans-serif'},
                      id='output-layout', children=[
    html.H2(
        children='COVID-19 Cases and Deaths',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'margin-top': '17px'
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
                   style={'textAlign': 'center', 'color': colors['text'],
                          "margin-left": "5px", "margin-right": "15px"}),
            html.Div(style={'margin-top': '10px'}),
            html.Div([
                dcc.Checklist(
                    id=c_name,
                    options=[{'label': c_name.title() if c_name not in ['us', 'uk'] else c_name.upper(),
                              'value': c_name}],
                    value=[c_name] if c_name in ('us', 'uk', 'italy') else [],
                    style={"margin-left": "15px", 'textAlign': 'left'},
                    inputStyle={"margin-right": "5px"})
                for i, c_name in enumerate(COUNTRY_LIST)]),
        ], style={'width': '17%', 'display': 'inline-block', 'vertical-align': 'top',
                  'background-color': 'lightgrey', 'horizontal-align': 'left', 'textAlign': 'center'}),
        html.Div(style={'width': '5%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                html.I("Fit exponential from: ",
                       style={'textAlign': 'center', 'color': colors['text'], "margin-left": "15px",}),
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
                html.I("Predict until: ",
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
                      "margin-bottom": "15px",}),
            dcc.Checklist(
                id='show-exponential-check',
                options=[{'label': "Show exponential fits?", 'value': 'exponential'}],
                value=['exponential'],
                style={'textAlign': 'center', "margin-bottom": "0px"},
                inputStyle={"margin-right": "5px"}
            ),
            dcc.Checklist(
                id='normalise-check',
                options=[{'label': "Normalise by population?", 'value': 'normalise'}],
                value=[],
                style={'textAlign': 'center', "margin-bottom": "20px"},
                inputStyle={"margin-right": "5px"}
            ),
            dcc.Loading(id="loading-icon", children=[html.Div(id="loading-output-1")], type="default"),
            dcc.Tabs([
                 dcc.Tab(label='linear', children=[
                    html.H3(children='Total Cases' , style={'textAlign': 'center', 'color': colors['text'],
                                                           'margin-top': '30px'}),
                    dcc.Graph(id='infections-linear'),
                    html.H3(children='Total Deaths', style={'textAlign': 'center', 'color': colors['text']}),
                    dcc.Graph(id='deaths-linear'),
                    html.Div(id='active-cases-linear-container', style={'display': 'block'}, children=[
                        html.H3(children='Active Cases', style={'textAlign': 'center', 'color': colors['text']}),
                        dcc.Graph(id='active-linear'),
                    ]),
                    html.Div(id='daily-cases-linear-container', children=[
                        html.H3(children='Daily New Cases', style={'textAlign': 'center', 'color': colors['text']}),
                        dcc.RadioItems(
                            id='daily-linear-bar-scatter-radio',
                            options=[{'label': i, 'value': i} for i in ['Bar', 'Scatter']],
                            value='Bar',
                            labelStyle={'display': 'inline-block', "margin-right": "10px"},
                            inputStyle={"margin-right": "4px"}
                        ),
                        dcc.Graph(id='daily-linear'),
                    ]),
                ]),
                dcc.Tab(label='log', children=[
                    html.H3(children='Total Cases', style={'textAlign': 'center', 'color': colors['text'],
                                                           'margin-top': '30px'}),
                    dcc.Graph(id='infections-log'),
                    html.H3(children='Total Deaths', style={'textAlign': 'center', 'color': colors['text']}),
                    dcc.Graph(id='deaths-log'),
                    html.Div(id='active-cases-log-container', style={'display': 'block'}, children=[
                        html.H3(children='Active Cases', style={'textAlign': 'center', 'color': colors['text']}),
                        dcc.Graph(id='active-log'),
                    ]),
                    html.Div(id='daily-cases-log-container', children=[
                        html.H3(children='Daily New Cases', style={'textAlign': 'center', 'color': colors['text']}),
                        dcc.RadioItems(
                            id='daily-log-bar-scatter-radio',
                            options=[{'label': i, 'value': i} for i in ['Bar', 'Scatter']],
                            value='Bar',
                            labelStyle={'display': 'inline-block', "margin-right": "10px"},
                            inputStyle={"margin-right": "4px"}
                        ),
                        dcc.Graph(id='daily-log'),
                    ]),
                ]),
            ]),
            html.H3(children='New Cases vs Total Cases',
                    style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Graph(id='new-vs-total-cases'),
            html.I("Some countries do not have available data for the number of Active Cases. ",
                   style={'textAlign': 'center', 'color': colors['text']}),
            html.I("The models assume exponential growth - social distancing, quarantining, herd immunity, "
                   "and other factors will slow down the predicted trajectories. ",
                   style={'textAlign': 'center', 'color': colors['text']}),
            # html.I("The last plot is a nice way to check if we are beating COVID-19. Countries that fall "
            #        "below the general linear line on the log-log plot are reducing their growth rate of COVID-19. ",
            #        style={'textAlign': 'center', 'color': colors['text']}),
        ], style={'width': '75%', 'display': 'inline-block', 'vertical-align': 'top', 'horizontal-align': 'center',
                  'textAlign': 'center', "margin-left": "0px"}),
        html.Hr(),
        html.Div(id='hidden-stored-data', style={'display': 'none'}),
        html.Footer(["Author: ",
                     html.A('Daniel Muthukrishna', href='https://twitter.com/DanMuthukrishna'), ". ",
                     html.A('Source code', href='https://github.com/daniel-muthukrishna/covid19'), ". ",
                     "Data is taken from ",
                     html.A("Worldometer", href='https://www.worldometers.info/coronavirus/'), " if available or otherwise ",
                     html.A("John Hopkins University (JHU) CSSE", href="https://github.com/ExpDev07/coronavirus-tracker-api"), "."],
                    style={'textAlign': 'center', 'color': colors['text']}),
    ], style={'horizontal-align': 'center', 'textAlign': 'center'}),
])


@app.callback([Output('infections-linear', 'figure'),
               Output('infections-log', 'figure'),
               Output('deaths-linear', 'figure'),
               Output('deaths-log', 'figure'),
               Output('active-linear', 'figure'),
               Output('active-log', 'figure'),
               Output('daily-linear', 'figure'),
               Output('daily-log', 'figure'),
               Output('new-vs-total-cases', 'figure'),
               Output('hidden-stored-data', 'children'),
               Output("loading-icon", "children"),],
              [Input('button-plot', 'n_clicks'),
               Input('start-date', 'date'),
               Input('end-date', 'date'),
               Input('show-exponential-check', 'value'),
               Input('normalise-check', 'value'),
               Input('daily-linear-bar-scatter-radio', 'value'),
               Input('daily-log-bar-scatter-radio', 'value')],
              [State('hidden-stored-data', 'children')] +
              [State(c_name, 'value') for c_name in COUNTRY_LIST])
def update_plots(n_clicks, start_date, end_date, show_exponential, normalise_by_pop,
                 daily_linear_radio, daily_log_radio, saved_json_data, *args):
    print(n_clicks, start_date, end_date, args)
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    country_names = []
    for country in args:
        country_names.extend(country)

    if saved_json_data is None:
        country_data = {}
    else:
        country_data = json.loads(saved_json_data)

    for i, country in enumerate(country_names):
        if country not in country_data.keys():
            data = get_data(country)
            country_data[country] = data

    out = []
    for title in ['Cases', 'Deaths', 'Currently Infected', 'Daily New Cases']:
        if normalise_by_pop:
            axis_title = f"{title} (% of population)"
        else:
            axis_title = title
        fig_linear = []
        fig_log = []

        layout_linear = {
            'yaxis': {'title': axis_title, 'type': 'linear', 'showgrid': True},
            'showlegend': True,
            'margin': {'l': 50, 'b': 100, 't': 0, 'r': 0},
        }
        layout_log = {
            'yaxis': {'title': axis_title, 'type': 'log', 'showgrid': True},
            'showlegend': True,
            'margin': {'l': 50, 'b': 100, 't': 0, 'r': 0},
        }

        for fig in [fig_linear, fig_log]:
            if show_exponential:
                fig.append(go.Scatter(x=[datetime.date(2020, 2, 20)],
                                      y=[0],
                                      mode='lines',
                                      line={'color': 'black', 'dash': 'dash'},
                                      showlegend=True,
                                      name=fr'Best exponential fits',
                                      yaxis='y1',
                                      legendgroup='group2', ))
                label = fr'COUNTRY : best fit (doubling time)'
            else:
                label = fr'COUNTRY'
            fig.append(go.Scatter(x=[datetime.date(2020, 2, 20)],
                                  y=[0],
                                  mode='lines+markers',
                                  line={'color': 'black'},
                                  showlegend=True,
                                  name=label,
                                  yaxis='y1',
                                  legendgroup='group2', ))

        for i, c in enumerate(country_names):
            if country_data[c] is None:
                print("Cannot retrieve data from country:", c)
                continue
            if title == 'Daily New Cases':
                dates = country_data[c]['Cases']['dates'][1:]
                xdata = np.arange(len(dates))
                ydata = np.diff(np.array(country_data[c]['Cases']['data']).astype('float'))
            elif title not in country_data[c]:
                continue
            else:
                dates = country_data[c][title]['dates']
                xdata = np.arange(len(dates))
                ydata = country_data[c][title]['data']
                ydata = np.array(ydata).astype('float')

            if normalise_by_pop:
                ydata = ydata/POPULATIONS[c] * 100

            date_objects = []
            for date in dates:
                date_objects.append(datetime.datetime.strptime(date, '%Y-%m-%d').date())
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
            lin_yfit = np.exp(logA) * np.exp(b * model_xdata)

            if show_exponential:
                if np.log(2) / b >= 1000:
                    double_time = 'no growth'
                else:
                    double_time = fr'{np.log(2) / b:.1f} days to double'
                label = fr'{c.upper():<10s}: {np.exp(b):.2f}^t ({double_time})'
            else:
                label = fr'{c.upper():<10s}'

            for fig in [fig_linear, fig_log]:
                daily_radio = daily_linear_radio if fig == fig_linear else daily_log_radio
                if title in ['Daily New Cases'] and daily_radio == 'Bar':
                    fig.append(go.Bar(x=date_objects,
                                      y=ydata,
                                      showlegend=True,
                                      name=label,
                                      marker={'color': colours[i]},
                                      yaxis='y1',
                                      legendgroup='group1'))
                else:
                    fig.append(go.Scatter(x=date_objects,
                                          y=ydata,
                                          mode='lines+markers',
                                          marker={'color': colours[i]},
                                          line={'color': colours[i]},
                                          showlegend=True,
                                          name=label,
                                          yaxis='y1',
                                          legendgroup='group1', ))
                if show_exponential and daily_radio != 'Bar':
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

    # Plot 'New Cases vs Total Cases'
    fig_new_vs_total = []
    for i, c in enumerate(country_names):
        l = 3  # Number of days to look back
        xdata = np.array(country_data[c]['Cases']['data']).astype('float')[1:-(l+1)]
        ydata = np.diff(np.array(country_data[c]['Cases']['data']).astype('float'))

        # Compute new cases over the past l days
        ydata = np.sum([np.array(ydata[i:i + l]) for i in range(len(ydata)) if i < (len(ydata) - l - 1)], axis=1)

        mask = xdata > 100
        xdata = xdata[mask]
        ydata = ydata[mask]

        if normalise_by_pop:
            xdata = xdata / POPULATIONS[c] * 100
            ydata = ydata / POPULATIONS[c] * 100

        fig_new_vs_total.append(go.Scatter(x=xdata,
                                           y=ydata,
                                           mode='lines+markers',
                                           marker={'color': colours[i]},
                                           line={'color': colours[i]},
                                           showlegend=True,
                                           name=fr'{c.upper():<10s}',
                                           yaxis='y1',
                                           legendgroup='group1', ))
    if normalise_by_pop:
        yaxis_title = 'New Cases (% of population) in the past 3 days'
        xaxis_title = 'Total Cases (% of population)'
    else:
        yaxis_title = 'New Cases (in the past 3 days)'
        xaxis_title = 'Total Cases'
    layout_new_vs_total = {
        'yaxis': {'title': yaxis_title, 'type': 'log', 'showgrid': True},
        'xaxis': {'title': xaxis_title, 'type': 'log', 'showgrid': True},
        'showlegend': True,
        'margin': {'l': 50, 'b': 100, 't': 0, 'r': 0},
    }
    out.append({'data': fig_new_vs_total, 'layout': layout_new_vs_total})

    out.append(json.dumps(country_data))
    out.append(None)

    return out


# Dash CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

if __name__ == '__main__':
    app.run_server(debug=True)
