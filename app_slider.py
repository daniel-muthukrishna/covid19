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

colours = ['green', 'orange', 'red', 'blue', 'purple', 'pink', 'brown', 'cyan',
           'olive', '#FF1493', 'navy', '#aaffc3', 'lightcoral', '#228B22', '#aa6e28', '#FFA07A',
           ] + list(mcolors.CSS4_COLORS.keys())
monthsdict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

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
                options=[{'label': "Germany", 'value': 'germany'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='iran',
                options=[{'label': "Iran", 'value': 'iran'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='france',
                options=[{'label': "France", 'value': 'france'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='ireland',
                options=[{'label': "Ireland", 'value': 'ireland'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='china',
                options=[{'label': "China", 'value': 'china'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='south-korea',
                options=[{'label': "South Korea", 'value': 'south-korea'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='switzerland',
                options=[{'label': "Switzerland", 'value': 'switzerland'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='netherlands',
                options=[{'label': "Netherlands", 'value': 'netherlands'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='austria',
                options=[{'label': "Austria", 'value': 'austria'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='belgium',
                options=[{'label': "Belgium", 'value': 'belgium'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='norway',
                options=[{'label': "Norway", 'value': 'norway'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='sweden',
                options=[{'label': "Sweden", 'value': 'sweden'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='portugal',
                options=[{'label': "Portugal", 'value': 'portugal'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='brazil',
                options=[{'label': "Brazil", 'value': 'brazil'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='canada',
                options=[{'label': "Canada", 'value': 'canada'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='denmark',
                options=[{'label': "Denmark", 'value': 'denmark'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='malaysia',
                options=[{'label': "Malaysia", 'value': 'malaysia'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='poland',
                options=[{'label': "Poland", 'value': 'poland'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='greece',
                options=[{'label': "Greece", 'value': 'greece'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='indonesia',
                options=[{'label': "Indonesia", 'value': 'indonesia'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='philippines',
                options=[{'label': "Philippines", 'value': 'philippines'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='china-hong-kong-sar',
                options=[{'label': "Hong Kong", 'value': 'china-hong-kong-sar'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='iraq',
                options=[{'label': "Iraq", 'value': 'iraq'}],
                value=[],
                style={"margin-left": "15px", }
            ),
            dcc.Checklist(
                id='algeria',
                options=[{'label': "Algeria", 'value': 'algeria'}],
                value=[],
                style={"margin-left": "15px", }
            ),

            html.I("Model date range:", style={'textAlign': 'center', 'color': colors['text'], "margin-left": "15px",}),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=datetime.date(2020, 1, 22),
                max_date_allowed=datetime.date(2022, 1, 1),
                initial_visible_month=datetime.date.today() - datetime.timedelta(days=7),
                start_date=datetime.date.today() - datetime.timedelta(days=7),
                end_date=datetime.date.today(),
            ),
            html.Hr(),
        ], style={'width': '15%', 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='linear', children=[
                        dcc.Graph(id='infections-linear'),
                        dcc.Graph(id='deaths-linear'),
                        dcc.Slider(
                            id='linear-slider',
                            min=-50,
                            max=50,
                            value=0,
                            marks={str(day): str(day) for day in range(-50, 50, 2)},
                            step=1
                        ),
                        ]),
                    dcc.Tab(label='log', children=[
                        dcc.Graph(id='infections-log'),
                        dcc.Graph(id='deaths-log'),
                    ]),
                ]),
            ], style={'width': '84%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Hr(),
        html.Div(id='hidden-stored-data', style={'display': 'none'}),
        html.Footer("Author: Daniel Muthukrishna. Data is taken from https://www.worldometers.info/coronavirus/. "
                    "Source code: https://github.com/daniel-muthukrishna/covid19",
                    style={'textAlign': 'center', 'color': colors['text']}),
    ]),
])


@app.callback([Output('infections-linear', 'figure'),
               Output('infections-log', 'figure'),
               Output('deaths-linear', 'figure'),
               Output('deaths-log', 'figure'),],
              [Input('linear-slider', 'value'),
               Input('hidden-stored-data', 'children')],
              [State('date-range', 'start_date'),
               State('date-range', 'end_date'),
               State('infections-linear', 'figure'),
               State('infections-log', 'figure'),
               State('deaths-linear', 'figure'),
               State('deaths-log', 'figure'),
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
def slider_update(slider_days, json_saved_data, start_date, end_date,
                  infections_linear_fig, infections_log_fig, deaths_linear_fig, deaths_log_fig,
                  *args):
    print('input trigger is linear slider')
    if infections_linear_fig is None:
        return infections_linear_fig, infections_log_fig, deaths_linear_fig, deaths_log_fig

    saved_out = json.loads(json_saved_data)

    out_figs = []
    for figure in saved_out:
        num_curves = len(figure['data'])
        for i in range(num_curves):
            if 'AUSTRALIA' in figure['data'][i]['name']:
                x = figure['data'][i]['x']
                newx = []
                for date in x:
                    newdate = datetime.datetime.strptime(date, '%Y-%m-%d').date() + datetime.timedelta(days=slider_days)
                    newx.append(newdate)
                figure['data'][i]['x'] = newx
        out_figs.append(figure)

    out = out_figs

    return out

@app.callback([Output('infections-linear', 'figure'),
               Output('infections-log', 'figure'),
               Output('deaths-linear', 'figure'),
               Output('deaths-log', 'figure'),
               Output('linear-slider', 'value'),
               Output('hidden-stored-data', 'children')],
              [Input('button-plot', 'n_clicks')],
              [State('date-range', 'start_date'),
               State('date-range', 'end_date'),
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
def update_plots(n_clicks, slider_days, json_saved_data, start_date, end_date,
                 infections_linear_fig, infections_log_fig, deaths_linear_fig, deaths_log_fig,
                 *args):
    print(n_clicks, slider_days, start_date, end_date, args)
    ctx = dash.callback_context
    input_trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    if input_trigger == 'button-plot' or n_clicks is None:
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

        out_figs = []
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

                fig_linear.append(go.Scatter(x=date_objects,
                                             y=ydata,
                                             mode='lines+markers',
                                             marker={'color': colours[i]},
                                             line={'color': colours[i]},
                                             showlegend=True,
                                             name=fr'{c.upper():<10s}: {np.exp(b):.2f}^t ({np.log(2) / b:.1f} days to double)',
                                             yaxis='y1',
                                             legendgroup='group1', ))
                fig_linear.append(go.Scatter(x=model_dates,
                                             y=lin_yfit,
                                             mode='lines',
                                             line={'color': colours[i], 'dash': 'dash'},
                                             showlegend=False,
                                             name=fr'Model {c.upper():<10s}',
                                             yaxis='y1',
                                             legendgroup='group1', ))

                fig_log.append(go.Scatter(x=date_objects,
                                          y=ydata,
                                          mode='lines+markers',
                                          marker={'color': colours[i]},
                                          line={'color': colours[i]},
                                          showlegend=True,
                                          name=fr'{c.upper():<10s}: {np.exp(b):.2f}^t ({np.log(2) / b:.1f} days to double)',
                                          yaxis='y1',
                                          legendgroup='group1', ))
                fig_log.append(go.Scatter(x=model_dates,
                                          y=lin_yfit,
                                          mode='lines',
                                          line={'color': colours[i], 'dash': 'dash'},
                                          showlegend=False,
                                          name=fr'Model {c.upper():<10s}',
                                          yaxis='y1',
                                          legendgroup='group1', ))
            out_figs.append({'data': fig_linear, 'layout': layout_linear})
            out_figs.append({'data': fig_log, 'layout': layout_log})

        json.dumps(out_figs)
        out = copy.copy(out_figs)
        out.append(0)  # Output slider value
        out.append(out_figs)  # Output saved json file

    return out


# Dash CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

if __name__ == '__main__':
    app.run_server(debug=True)
