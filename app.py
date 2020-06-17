# -*- coding: utf-8 -*-
from datetime import datetime
import pytz

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pymongo import MongoClient

import constants
from mongo_test import update_record, get_all_records_of_the_day, convert_mongo_dict_to_graph_input

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.H1(children='Chechi\'s Tracker'),
    html.Button(id='see-graph', n_clicks=0, children='See Today\'s Status'),
    html.Div(id='output-graph'),
    html.P(),
    html.P(),
    html.Div(children="Enter the number of hours you have just productively used \n \n"),
    html.P(),
    html.P(),

    dcc.RadioItems(
        id='person',
        options=constants.PEOPLE_LIST,
    ),
    dcc.Input(id='input-1-state', type='number', value=''),
    html.Button(id='submit-button-state', n_clicks=0, children='Add hours'),
    html.Div(id='output-state'),
    html.Button('Reset', id='reset_button', n_clicks=0),
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('person', 'value')])
def update_output_state(n_clicks, input1, person):
    if n_clicks > 0 and person:
        today = get_today_date_string()
        my_mongo_client = MongoClient('localhost', 27017)
        sum_result = update_record(person, today, input1, my_mongo_client)
        my_mongo_client.close()
        actual_name = next(item["label"] for item in constants.PEOPLE_LIST if item["value"] == person)
        return u'''
                Successfully added to {}\'s  total for today. New total: {}
            '''.format(actual_name, sum_result)


@app.callback(Output('output-graph', 'children'),
              [Input('see-graph', 'n_clicks')], )
def update_output_graph(n_clicks):
    if n_clicks > 0:
        today = get_today_date_string()
        my_mongo_client = MongoClient('localhost', 27017)

        current_data = convert_mongo_dict_to_graph_input(get_all_records_of_the_day(today, my_mongo_client))
        my_mongo_client.close()
        return html.Div(dcc.Graph(
            id='example-graph',
            figure={
                'data': current_data,
                'layout': {
                    'title': "Today's Status ",
                    'plot_bgcolor': constants.colors['background'],
                    'paper_bgcolor': constants.colors['background'],
                    'font': {
                        'color': constants.colors['text']
                    }
                }
            }
        ))


@app.callback([Output('input-1-state', 'value'),
               Output('output-state', 'children')],
              [Input('reset_button', 'n_clicks')])
def update(reset):
    return 0, 0


def get_today_date_string():
    tz_india = pytz.timezone('Asia/Kolkata')
    datetime_india = datetime.now(tz_india)
    return datetime_india.now().strftime("%m/%d/%y")


#  TODO how to add multiple outputs to the same callback and the same output to multiple callbacks
#  TODO remove show status button (auto show everytime + update on adding new hours)
#  TODO remove today's status display when RESET button pressed


if __name__ == '__main__':
    app.run_server(debug=True, port=2508, host="192.168.1.7")
