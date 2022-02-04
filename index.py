import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime
import pymysql


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])




app.layout = html.Div([
    html.Div([
        dcc.Interval(id = 'update_chart',
                     interval = 5000,
                     n_intervals = 0)
        ]),
        html.Div([
            dcc.Graph(id = 'temperature_chart',
            animate=True,
            config = {'displayModeBar': 'hover'},
        ),
])
])

@app.callback(Output('temperature_chart', 'figure'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    header_list = ['Time', 'Data']
    #df = pd.read_csv('file.csv', names = header_list)

    db = pymysql.connect(host="192.185.176.234", user="fabio_python",
                            password="pJaSaRtbk_3Yswy", database="fabio_PyMySQL")

    cursor = db.cursor()

    sql = """
            SELECT * FROM LOG
            """

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

    except:
        db.rollback()

    db.close()

    df = pd.DataFrame(data=result, columns=header_list)

    get_time = df['Time'].tail(8640)
    get_data= df['Data'].tail(8640)
    
    if n_intervals == 0:
        raise PreventUpdate

    return {
        'data': [go.Scatter(
            x = get_time,
            y = get_data,
            mode = 'lines',
        )],

        'layout': go.Layout(
            autosize=True,
            height=1000,         
            margin = dict(t = 25, r = 25, l = 50),
            xaxis = dict(range = [min(get_time), max(get_time)],
                         title = header_list[0],
                         showline = True,
                         showgrid = True
                         ),
            yaxis = dict(range = [min(get_data), max(get_data)],
                         title = header_list[1],
                         color = 'black',
                         showline = True,
                         showgrid = True
                         )
                        )
            }





if __name__ == "__main__":
        app.run_server()