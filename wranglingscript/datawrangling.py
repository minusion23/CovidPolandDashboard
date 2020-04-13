import pandas as pd
import plotly.graph_objs as go
import requests
from collections import defaultdict
# Get data from the API

def unpack(response, queryword):
    ''''
    Args: Takes a JSON response from the API with Covid Numbers and a QueryWord - which values should the response
    be queried for

    Returns: a list with the values

    '''
    search_by = queryword
    queryword = defaultdict(list)
    queryword = [[], []]
    for entry in response.json()[search_by]['locations']:
        if entry['country'] == "Poland":
            # queryword['Latest'].append(float(entry['latest']))
            print(entry)
            for item, value in entry['history'].items():
                if value > 100 and search_by == 'confirmed' or value > 10 and search_by == 'deaths':
                    print(item)
                    print(value)
                # queryword[item] = value
                    queryword[0].append(item)
                    queryword[1].append(value)
    return queryword


def return_figures():
    r = requests.get("https://coronavirus-tracker-api.herokuapp.com/all")
    confirmed_data = unpack(r, "confirmed")
    deceased_data = unpack(r, "deaths")
    """Creates two plotly visualisations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    graph_one = []
    x_val = confirmed_data[0]
    y_val = confirmed_data[1]
    graph_one.append(
        go.Scatter(
            x=x_val,
            y=y_val,
            mode='lines',
            name='Confirmed Cases'
        ))
    layout_one = dict(title='Confirmed cases in Poland (graph starts from 100th case)',
                      xaxis=dict(title = 'Date'),
                      yaxis=dict(title = 'Confirmed cases total on the day', type = 'log'),
                      )
    graph_two = []
    x_val = deceased_data [0]
    y_val = deceased_data [1]
    graph_two.append(
        go.Scatter(
            x=x_val,
            y=y_val,
            mode='lines',
            name='Deceased Cases'
        ))
    layout_two = dict(title='Deceased cases in Poland (graph starts from 10th case)',
                      xaxis=dict(title='Date'),
                      yaxis=dict(title='Deceased cases total on the day', type = 'log'),
                      )
    figures = [dict(data=graph_one, layout=layout_one), dict(data=graph_two, layout=layout_two)]
    return figures

