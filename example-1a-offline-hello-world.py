from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

import json
import plotly
import numpy as np

import dash.utils as utils
from dash.components import element as el
from dash.components import graph

name = 'dash-1a-offline-hello-world'
app = Flask(name)
app.debug = True
app.config['key'] = 'secret'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template(
        'layouts/layout_single_column_and_controls.html'.format(name),
        app_name=name)


@socketio.on('replot')
def replot(app_state):
    print(app_state)
    frequency = float(app_state['frequency'])
    x = np.linspace(0, 2 * 3.14, 500)
    y = np.sin(frequency * x)
    messages = [
        {
            'id': 'sine-wave',
            'task': 'newPlot',
            'data': [{
                'x': x,
                'y': y,
            }],
            'layout': {
                'xaxis': {
                    'range': [0, 2 * 3.14]
                },
                'title': app_state.get('title', '')
            }
        }
    ]

    emit('postMessage', json.dumps(messages,
                                   cls=plotly.utils.PlotlyJSONEncoder))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9991)
