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
import copy

from get_data import get_data
from constants import POPULATIONS, WORLDOMETER_NAME

colours = ['#1f77b4','#ff7f0e', '#2ca02c','#9467bd', '#8c564b', '#e377c2', '#d62728', '#7f7f7f', '#bcbd22', '#17becf',
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
                'hong kong',
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
                'mexico',
                'moldova',
                'morocco',
                'netherlands',
                'new zealand',
                'north macedonia',
                'norway',
                'pakistan',
                'palestine',
                'panama',
                'peru',
                'philippines',
                'poland',
                'portugal',
                'qatar',
                'romania',
                'russia',
                'san marino',
                'saudi arabia',
                'serbia',
                'singapore',
                'slovakia',
                'slovenia',
                'south africa',
                'south korea',
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
                ]

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])


app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-162069366-1"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'UA-162069366-1');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

app.layout = html.Div(style={'backgroundColor': colors['background'], 'font-family': 'sans-serif'},
                      id='output-layout', children=[

    html.Br(),
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
            html.H2(
                children='COVID-19 Cases and Deaths',
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'margin-top': '5px',
                    'margin-bottom': '15px',
                }
            ),
            html.P(["This App is superseded by the more comprehensive ", html.A('LowHighCovid ', href='https://lowhighcovid.herokuapp.com'),
                    "App. \nIt includes modelling and educational resources as well as data on vaccinations by country."],
                   style={'textAlign': 'center', 'color': colors['text'], "margin-bottom": "40px"}),
            html.Hr(),
            html.Div([
                html.I("Fit exponential from: ",
                       style={'textAlign': 'center', 'color': colors['text'], "margin-left": "15px",}),
                dcc.DatePickerSingle(
                    id='start-date',
                    min_date_allowed=datetime.date(2020, 1, 22),
                    max_date_allowed=datetime.date(2022, 1, 1),
                    initial_visible_month=datetime.date.today() - datetime.timedelta(days=7),
                    date=datetime.date.today() - datetime.timedelta(days=7),
                    display_format='D-MMM-YYYY',
                    style={'textAlign': 'center'}
                ),
            ], style={'display': 'inline-block', 'horizontal-align': 'center', 'textAlign': 'center',
                      'margin-top': '10px',}),
            html.Div([
                html.I("Predict until: ",
                       style={'textAlign': 'center', 'color': colors['text'], "margin-left": "15px", }),
                dcc.DatePickerSingle(
                    id='end-date',
                    min_date_allowed=datetime.date(2020, 1, 22),
                    max_date_allowed=datetime.date(2022, 1, 1),
                    initial_visible_month=datetime.date.today(),
                    date=datetime.date.today(),
                    display_format='D-MMM-YYYY',
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
                options=[{'label': "Plot as percentage of population?", 'value': 'normalise'}],
                value=[],
                style={'textAlign': 'center', "margin-bottom": "20px"},
                inputStyle={"margin-right": "5px"}
            ),
            dcc.Loading(id="loading-icon", children=[html.Div(id="loading-output-1")], type="default"),

            html.Hr(),
            html.H3(children='Total Cases', style={'textAlign': 'center', 'color': colors['text'],
                                                   'margin-top': '30px'}),

            html.Div(style={'display': 'inline-block', 'textAlign': 'left'}, children=[
                dcc.Checklist(
                    id='align-cases-check',
                    options=[{'label': "Align countries by the date when the number of confirmed cases was ",
                              'value': 'align'}],
                    value=[],
                    style={'textAlign': 'left', "margin-right": "4px", 'display': 'inline-block'},
                    inputStyle={"margin-right": "5px"}
                ),
                dcc.Input(
                    id="align-cases-input",
                    type="number",
                    placeholder='Number of cases',
                    value=1000,
                    min=0,
                    debounce=True,
                    style={'width': 80},
                ),
                html.Div(id='display_percentage_text_cases', style={'display': 'none'}, children=[
                    html.P("% of population")
                ]),
            ]),
            dcc.Graph(id='infections-plot'),
            html.H3(children='Total Deaths', style={'textAlign': 'center', 'color': colors['text'],
                                                    'margin-top': '10px'}),
            html.Div(style={'display': 'inline-block', 'textAlign': 'left'}, children=[
                dcc.Checklist(
                    id='align-deaths-check',
                    options=[{'label': "Align countries by the date when the number of confirmed deaths was ",
                              'value': 'align'}],
                    value=[],
                    style={'textAlign': 'left', "margin-right": "4px", 'display': 'inline-block'},
                    inputStyle={"margin-right": "5px"}
                ),
                dcc.Input(
                    id="align-deaths-input",
                    type="number",
                    placeholder='Number of deaths',
                    value=20,
                    min=0,
                    debounce=True,
                    style={'width': 80},
                ),
                html.Div(id='display_percentage_text_deaths', style={'display': 'none'}, children=[
                    html.P("% of population")
                ]),
            ]),
            dcc.Graph(id='deaths-plot'),
            html.Div(id='active-cases-container', style={'display': 'block'}, children=[
                html.H3(children='Active Cases', style={'textAlign': 'center', 'color': colors['text']}),
                html.Div(style={'display': 'inline-block', 'textAlign': 'left'}, children=[
                    dcc.Checklist(
                        id='align-active-cases-check',
                        options=[{'label': "Align countries by the date when the number of confirmed cases was ",
                                  'value': 'align'}],
                        value=[],
                        style={'textAlign': 'left', "margin-right": "4px", 'display': 'inline-block'},
                        inputStyle={"margin-right": "5px"}
                    ),
                    dcc.Input(
                        id="align-active-cases-input",
                        type="number",
                        placeholder='Number of cases',
                        value=1000,
                        min=0,
                        debounce=True,
                        style={'width': 80},
                    ),
                    html.Div(id='display_percentage_text_active', style={'display': 'none'}, children=[
                        html.P("% of population")
                    ]),
                ]),
                dcc.Graph(id='active-plot'),
            ]),
            html.Div(id='daily-cases-container', children=[
                html.H3(children='Daily New Cases', style={'textAlign': 'center', 'color': colors['text'],
                                                    'margin-top': '10px'}),
                html.Div(style={'display': 'inline-block', 'textAlign': 'left'}, children=[
                    dcc.Checklist(
                        id='align-daily-cases-check',
                        options=[{'label': "Align countries by the date when the number of confirmed cases was ",
                                  'value': 'align'}],
                        value=[],
                        style={'textAlign': 'left', "margin-right": "4px", 'display': 'inline-block'},
                        inputStyle={"margin-right": "5px"}
                    ),
                    dcc.Input(
                        id="align-daily-cases-input",
                        type="number",
                        placeholder='Number of cases',
                        value=1000,
                        min=0,
                        debounce=True,
                        style={'width': 80},
                    ),
                    html.Div(id='display_percentage_text_daily_cases', style={'display': 'none'}, children=[
                        html.P("% of population")
                    ]),
                ]),
                dcc.Graph(id='daily-cases-plot'),
            ]),

            html.Div(id='daily-deaths-container', children=[
                html.H3(children='Daily New Deaths', style={'textAlign': 'center', 'color': colors['text'],
                                                    'margin-top': '10px'}),
                html.Div(style={'display': 'inline-block', 'textAlign': 'left'}, children=[
                    dcc.Checklist(
                        id='align-daily-deaths-check',
                        options=[{'label': "Align countries by the date when the number of confirmed deaths was ",
                                  'value': 'align'}],
                        value=[],
                        style={'textAlign': 'left', "margin-right": "4px", 'display': 'inline-block'},
                        inputStyle={"margin-right": "5px"}
                    ),
                    dcc.Input(
                        id="align-daily-deaths-input",
                        type="number",
                        placeholder='Number of deaths',
                        value=1000,
                        min=0,
                        debounce=True,
                        style={'width': 80},
                    ),
                    html.Div(id='display_percentage_text_daily_deaths', style={'display': 'none'}, children=[
                        html.P("% of population")
                    ]),
                ]),
                dcc.Graph(id='daily-deaths-plot'),
            ]),

            html.H3(children='New Cases vs Total Cases', style={'textAlign': 'center', 'color': colors['text'],
                                                    'margin-top': '10px'}),
            dcc.Graph(id='new-vs-total-cases'),

            html.H3(children='New Deaths vs Total Deaths', style={'textAlign': 'center', 'color': colors['text'],
                                                                'margin-top': '10px'}),
            dcc.Graph(id='new-vs-total-deaths'),

            html.Li(html.I(
                "Caution should be applied when directly comparing the number of confirmed cases of each country. "
                "Different countries have different testing rates, and may underestimate the number of cases "
                "by varying amounts."),
                style={'textAlign': 'left', 'color': colors['text']}),
            html.Li(html.I(
                "The models assume exponential growth - social distancing, quarantining, herd immunity, "
                "and other factors will slow down the predicted trajectories. "
                "Thus, predicting too far in the future is not recommended."),
                style={'textAlign': 'left', 'color': colors['text']}),
            html.Li(html.I(
                "Some countries do not have available data for the number of Active Cases. "),
                style={'textAlign': 'left', 'color': colors['text']}),
            html.Li(html.I(
                "The final two plots are an informative way to compare how each country was increasing when they had "
                "different numbers of total cases/deaths (each point is a different day); countries that fall below "
                "the general linear line on the log-log plot are reducing their growth rate of COVID-19 cases."),
                style={'textAlign': 'left', 'color': colors['text']}),
        ], style={'width': '75%', 'display': 'inline-block', 'vertical-align': 'top', 'horizontal-align': 'center',
                  'textAlign': 'center', "margin-left": "0px"}),
        html.Hr(),
        html.Div(id='hidden-stored-data', style={'display': 'none'}),
        html.Footer(["Author: ",
                     html.A('Daniel Muthukrishna', href='https://twitter.com/DanMuthukrishna'), ". ",
                     html.A('Source code', href='https://github.com/daniel-muthukrishna/covid19'), ". ",
                     html.Br(),
                     "Data is taken from ",
                     html.A("Worldometer", href='https://www.worldometers.info/coronavirus/'), " if available or otherwise ",
                     html.A("Johns Hopkins University (JHU) CSSE", href="https://github.com/ExpDev07/coronavirus-tracker-api"), "."],
                    style={'textAlign': 'center', 'color': colors['text'], "margin-bottom": "40px"}),
    ], style={'horizontal-align': 'center', 'textAlign': 'center'}),
])


@app.callback([Output('align-cases-check', 'options'),
               Output('align-cases-input', 'value'),
               Output('display_percentage_text_cases', 'style'),
               Output('align-deaths-check', 'options'),
               Output('align-deaths-input', 'value'),
               Output('display_percentage_text_deaths', 'style'),
               Output('align-active-cases-check', 'options'),
               Output('align-active-cases-input', 'value'),
               Output('display_percentage_text_active', 'style'),
               Output('align-daily-cases-check', 'options'),
               Output('align-daily-cases-input', 'value'),
               Output('display_percentage_text_daily_cases', 'style'),
               Output('align-daily-deaths-check', 'options'),
               Output('align-daily-deaths-input', 'value'),
               Output('display_percentage_text_daily_deaths', 'style')],
              [Input('normalise-check', 'value')])
def update_align_options(normalise_by_pop):
    if normalise_by_pop:
        options_cases = [{'label': "Align countries by the date when the percentage of confirmed cases was ",
                    'value': 'align'}]
        options_deaths = [{'label': "Align countries by the date when the number of confirmed deaths was ",
                    'value': 'align'}]
        hidden_text = {'display': 'inline-block'}
        return [options_cases, 0.0015, hidden_text,
                options_deaths, 0.000034, hidden_text,
                options_cases, 0.0015, hidden_text,
                options_cases, 0.0015, hidden_text,
                options_deaths, 0.000034, hidden_text]
    else:
        options_cases = [{'label': "Align countries by the date when the number of confirmed cases was ",
                    'value': 'align'}]
        options_deaths = [{'label': "Align countries by the date when the number of confirmed deaths was ",
                    'value': 'align'}]
        hidden_text = {'display': 'none'}
        return[options_cases, 1000, hidden_text,
               options_deaths, 20, hidden_text,
               options_cases, 1000, hidden_text,
               options_cases, 1000, hidden_text,
               options_deaths, 20, hidden_text]


@app.callback([Output('infections-plot', 'figure'),
               Output('deaths-plot', 'figure'),
               Output('active-plot', 'figure'),
               Output('daily-cases-plot', 'figure'),
               Output('daily-deaths-plot', 'figure'),
               Output('new-vs-total-cases', 'figure'),
               Output('new-vs-total-deaths', 'figure'),
               Output('hidden-stored-data', 'children'),
               Output("loading-icon", "children"),],
              [Input('button-plot', 'n_clicks'),
               Input('start-date', 'date'),
               Input('end-date', 'date'),
               Input('show-exponential-check', 'value'),
               Input('normalise-check', 'value'),
               Input('align-cases-check', 'value'),
               Input('align-cases-input', 'value'),
               Input('align-deaths-check', 'value'),
               Input('align-deaths-input', 'value'),
               Input('align-active-cases-check', 'value'),
               Input('align-active-cases-input', 'value'),
               Input('align-daily-cases-check', 'value'),
               Input('align-daily-cases-input', 'value'),
               Input('align-daily-deaths-check', 'value'),
               Input('align-daily-deaths-input', 'value')],
              [State('hidden-stored-data', 'children')] +
              [State(c_name, 'value') for c_name in COUNTRY_LIST])
def update_plots(n_clicks, start_date, end_date, show_exponential, normalise_by_pop,
                 align_cases_check, align_cases_input, align_deaths_check, align_deaths_input, align_active_cases_check,
                 align_active_cases_input, align_daily_cases_check, align_daily_cases_input,
                 align_daily_deaths_check, align_daily_deaths_input, saved_json_data, *args):
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
            try:
                data = get_data(country)
                country_data[country] = data
            except Exception as e:
                print(e)
                country_names.remove(country)
                continue

    out = []
    for title in ['Cases', 'Deaths', 'Currently Infected', 'Daily New Cases', 'Daily New Deaths']:
        if normalise_by_pop:
            axis_title = f"{title} (% of population)"
        else:
            axis_title = title

        if title == 'Cases':
            align_countries = align_cases_check
            align_input = align_cases_input
        elif title == 'Deaths':
            align_countries = align_deaths_check
            align_input = align_deaths_input
        elif title == 'Currently Infected':
            align_countries = align_active_cases_check
            align_input = align_active_cases_input
        elif title == 'Daily New Cases':
            align_countries = align_daily_cases_check
            align_input = align_daily_cases_input
        elif title == 'Daily New Deaths':
            align_countries = align_daily_deaths_check
            align_input = align_daily_deaths_input

        figs = []

        if align_countries:
            xaxis_title = f'Days since the total confirmed cases reached {align_input}'
            if normalise_by_pop:
                xaxis_title += '% of the population'
        else:
            xaxis_title = ''

        layout_normal = {
            'yaxis': {'title': axis_title, 'type': 'linear', 'showgrid': True},
            'xaxis': {'title': xaxis_title, 'showgrid': True},
            'showlegend': True,
            'margin': {'l': 70, 'b': 100, 't': 0, 'r': 0},
            'updatemenus': [
                dict(
                    buttons=list([
                        dict(
                            args=["yaxis", {'title': axis_title, 'type': 'linear', 'showgrid': True}],
                            label="Linear",
                            method="relayout"
                        ),
                        dict(
                            args=["yaxis", {'title': axis_title, 'type': 'log', 'showgrid': True}],
                            label="Logarithmic",
                            method="relayout"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10, "b": 10},
                    showactive=True,
                    x=0.,
                    xanchor="left",
                    y=1.2,
                    yanchor="top"
                ),
            ]
        }
        # if normalise_by_pop:
        #     layout_normal['yaxis']['tickformat'] = '%.2f'

        layout_daily_plot = copy.deepcopy(layout_normal)
        layout_daily_plot['updatemenus'].append(
            dict(
                buttons=list([
                    dict(
                        args=[{"visible": [False, False] + [False, False, True]*len(country_names) if show_exponential else [False] + [False, True]*len(country_names)}],
                        label="Bar",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [True, True] + [True, True, False]*len(country_names) if show_exponential else [True] + [True, False]*len(country_names)}],
                        label="Scatter",
                        method="update"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10, "b": 10},
                showactive=True,
                x=0.2,
                xanchor="left",
                y=1.2,
                yanchor="top"
                ),
            )

        if show_exponential:
            figs.append(go.Scatter(x=[datetime.date(2020, 2, 20)] if not align_countries else [0],
                                   y=[0],
                                   mode='lines',
                                   line={'color': 'black', 'dash': 'dash'},
                                   showlegend=True,
                                   visible=False if title in ['Daily New Cases', 'Daily New Deaths']else 'legendonly',
                                   name=fr'Best exponential fits',
                                   yaxis='y1',
                                   legendgroup='group2', ))
            label = fr'COUNTRY : best fit (doubling time)'
        else:
            label = fr'COUNTRY'
        figs.append(go.Scatter(x=[datetime.date(2020, 2, 20)] if not align_countries else [0],
                               y=[0],
                               mode='lines+markers',
                               line={'color': 'black'},
                               showlegend=True,
                               visible=False if title in ['Daily New Cases', 'Daily New Deaths'] else 'legendonly',
                               name=label,
                               yaxis='y1',
                               legendgroup='group2', ))

        for i, c in enumerate(country_names):
            print(c)
            if country_data[c] is None:
                print("Cannot retrieve data from country:", c)
                continue
            if title == 'Daily New Cases':
                dates = country_data[c]['Cases']['dates'][1:]
                xdata = np.arange(len(dates))
                ydata = np.diff(np.array(country_data[c]['Cases']['data']).astype('float'))
            elif title == 'Daily New Deaths':
                dates = country_data[c]['Deaths']['dates'][1:]
                xdata = np.arange(len(dates))
                ydata = np.diff(np.array(country_data[c]['Deaths']['data']).astype('float'))
            elif title not in country_data[c]:
                continue
            else:
                dates = country_data[c][title]['dates']
                xdata = np.arange(len(dates))
                ydata = country_data[c][title]['data']
                ydata = np.array(ydata).astype('float')

            date_objects = []
            for date in dates:
                date_objects.append(datetime.datetime.strptime(date, '%Y-%m-%d').date())
            date_objects = np.asarray(date_objects)

            if normalise_by_pop:
                ydata = ydata/POPULATIONS[c] * 100

            if align_countries:
                if title in ['Cases', 'Deaths']:
                    idx_when_n_cases = np.abs(ydata - align_input).argmin()
                elif title in ['Currently Infected', 'Daily New Cases']:
                    ydata_cases = np.array(country_data[c]['Cases']['data']).astype('float')
                    ydata_cases = ydata_cases / POPULATIONS[c] * 100 if normalise_by_pop else ydata_cases
                    idx_when_n_cases = np.abs(ydata_cases - align_input).argmin()
                elif title in ['Daily New Deaths']:
                    ydata_cases = np.array(country_data[c]['Deaths']['data']).astype('float')
                    ydata_cases = ydata_cases / POPULATIONS[c] * 100 if normalise_by_pop else ydata_cases
                    idx_when_n_cases = np.abs(ydata_cases - align_input).argmin()
                if title in ['Daily New Cases', 'Daily New Deaths']:
                    idx_when_n_cases -= 1

                xdata = xdata - idx_when_n_cases

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
                if np.log(2) / b > 1000 or np.log(2) / b < 0:
                    double_time = 'no growth'
                else:
                    double_time = fr'{np.log(2) / b:.1f} days to double'
                label = fr'{c.upper():<10s}: {np.exp(b):.2f}^t ({double_time})'
            else:
                label = fr'{c.upper():<10s}'

            figs.append(go.Scatter(x=date_objects if not align_countries else xdata,
                                   y=ydata,
                                   hovertext=[f"Date: {d.strftime('%d-%b-%Y')}" for d in date_objects] if align_countries else '',
                                   mode='lines+markers',
                                   marker={'color': colours[i]},
                                   line={'color': colours[i]},
                                   showlegend=True,
                                   visible=False if title in ['Daily New Cases', 'Daily New Deaths'] else True,
                                   name=label,
                                   yaxis='y1',
                                   legendgroup='group1', ))

            if show_exponential:
                if np.log(2) / b < 0:
                    show_plot = False
                else:
                    show_plot = True
                figs.append(go.Scatter(x=model_dates if not align_countries else model_xdata,
                                       y=lin_yfit,
                                       hovertext=[f"Date: {d.strftime('%d-%b-%Y')}" for d in model_dates] if align_countries else '',
                                       mode='lines',
                                       line={'color': colours[i], 'dash': 'dash'},
                                       showlegend=False,
                                       visible=False if title in ['Daily New Cases', 'Daily New Deaths'] else show_plot,
                                       name=fr'Model {c.upper():<10s}',
                                       yaxis='y1',
                                       legendgroup='group1', ))

            if title in ['Daily New Cases', 'Daily New Deaths'] :
                figs.append(go.Bar(x=date_objects if not align_countries else xdata,
                                   y=ydata,
                                   hovertext=[f"Date: {d.strftime('%d-%b-%Y')}" for d in date_objects] if align_countries else '',
                                   showlegend=True,
                                   visible=True,
                                   name=label,
                                   marker={'color': colours[i]},
                                   yaxis='y1',
                                   legendgroup='group1'))
                layout_out = copy.deepcopy(layout_daily_plot)
            else:
                layout_out = copy.deepcopy(layout_normal)

        out.append({'data': figs, 'layout': layout_out})

    # Plot 'New Cases vs Total Cases' and 'New Deaths vs Total Deaths'
    for title in ['Cases', 'Deaths']:
        fig_new_vs_total = []
        for i, c in enumerate(country_names):
            l = 7  # Number of days to look back
            cases = np.array(country_data[c][title]['data']).astype('float')
            xdata = np.copy(cases[l:])
            ydata = np.diff(cases)
            len_ydata = len(ydata)

            # Compute new cases over the past l days
            ydata = np.sum([np.array(ydata[i:i + l]) for i in range(len_ydata) if i <= (len_ydata - l)], axis=1)

            dates = country_data[c][title]['dates'][l:]
            date_objects = []
            for date in dates:
                date_objects.append(datetime.datetime.strptime(date, '%Y-%m-%d').date())
            date_objects = np.asarray(date_objects)

            mask = xdata > 100 if title == 'Cases' else xdata > 10
            xdata = xdata[mask]
            ydata = ydata[mask]
            date_objects = date_objects[mask]

            if normalise_by_pop:
                xdata = xdata / POPULATIONS[c] * 100
                ydata = ydata / POPULATIONS[c] * 100

            fig_new_vs_total.append(go.Scatter(x=xdata,
                                               y=ydata,
                                               hovertext=[f"Date: {d.strftime('%d-%b-%Y')}" for d in date_objects],
                                               mode='lines+markers',
                                               marker={'color': colours[i]},
                                               line={'color': colours[i]},
                                               showlegend=True,
                                               name=fr'{c.upper():<10s}',
                                               yaxis='y1',
                                               legendgroup='group1', ))
        if normalise_by_pop:
            yaxis_title = f'New {title} (% of population) per week (log scale)'  # {l} days'
            xaxis_title = f'Total {title} (% of population) (log scale)'
        else:
            yaxis_title = f'New {title} per week'  # {l} days)'
            xaxis_title = f'Total {title}'
        layout_new_vs_total = {
            'yaxis': {'title': yaxis_title, 'type': 'log', 'showgrid': True},
            'xaxis': {'title': xaxis_title, 'type': 'log', 'showgrid': True},
            'showlegend': True,
            'margin': {'l': 70, 'b': 100, 't': 50, 'r': 0},
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
