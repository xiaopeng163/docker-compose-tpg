import json
import os
from pathlib import Path

from prometheus_client import make_wsgi_app, generate_latest, \
    CONTENT_TYPE_LATEST
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Response, Flask


class CustomCollector(object):
    """custom collector
    """
    def __init__(self):
        self.json_file_path = Path(os.environ.get('JSON_PATH', '/root/json'))

    def collect(self):
        
        for file_name in self.json_file_path.rglob("*.json"):
            with open(file_name) as f:
                metrics = json.load(f)
                for metric in metrics:
                    if not metric.get('values'):
                        continue
                    if metric['type'] == 'gauge':
                        g = GaugeMetricFamily(
                            metric['metric_name'], 
                            metric['help'],
                            labels=metric['labels']
                        )
                    elif metric['type'] == 'counter':
                        g = CounterMetricFamily(
                            metric['metric_name'], 
                            metric['help'],
                            labels=metric['labels']
                        )
                    else:
                        continue
                    for value in metric['values']:
                        g.add_metric(value['labels'], value['value'])
                    yield g


REGISTRY.register(CustomCollector())

# Create my app
app = Flask(__name__)


@app.route('/metrics', methods=['GET'])
def get_data():
    """Returns all data as plaintext."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
