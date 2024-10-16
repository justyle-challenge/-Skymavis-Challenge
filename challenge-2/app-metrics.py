from flask import Flask, jsonify, Response
import requests
from dotenv import load_dotenv
from prometheus_client import Gauge, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

INFURA_ENDPOINT_ID = os.getenv('INFURA_ENDPOINT_ID')
INFURA_URL = f"https://mainnet.infura.io/v3/{INFURA_ENDPOINT_ID}"
ANKR_URL = "https://rpc.ankr.com/eth"

# Prometheus metrics
registry = CollectorRegistry()
infura_block_metric = Gauge('infura_block_number', 'Current block number from Infura', registry=registry)
ankr_block_metric = Gauge('ankr_block_number', 'Current block number from Ankr', registry=registry)
block_diff_metric = Gauge('block_diff', 'Difference in block numbers between Infura and Ankr', registry=registry)
block_diff_status_metric = Gauge('block_diff_status', 'Status of block difference (1 for success, 0 for fail)', registry=registry)

def get_block_number(url, provider_name):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        block_number_hex = response.json()['result']
        block_number = int(block_number_hex, 16)
        return block_number
    else:
        print(f"Error fetching block number from {provider_name}")
        return None

def check_block_diff():
    infura_block_number = get_block_number(INFURA_URL, 'Infura')
    ankr_block_number = get_block_number(ANKR_URL, 'Ankr')

    if infura_block_number is None or ankr_block_number is None:
        return None, None, None, None

    block_diff = abs(infura_block_number - ankr_block_number)
    status = "success" if block_diff < 5 else "fail"

    return infura_block_number, ankr_block_number, block_diff, status

# Route targets with JSON for http sd endpoint
@app.route('/targets', methods=['GET'])
def targets():
    infura_block_number, ankr_block_number, block_diff, status = check_block_diff()

    if infura_block_number is None or ankr_block_number is None:
        targets = []
    else:
        # If no targets should be transmitted, HTTP 200 must also be emitted, with an empty list []
        targets = [
            {
                "targets": ["http-sd-endpoint.demo:5000"],
                "labels": {
                    "job": "ethereum",
                    "provider": "Infura-Ankr",
                    "task" : "check-block-diff"
                }
            }
        ]

    # Ensure HTTP 200 response with the HTTP Header Content-Type: application/json and UTF-8 encoding
    response = Response(
        response=jsonify(targets).get_data(as_text=True),
        status=200,
        mimetype='application/json'
    )
    response.headers["Content-Type"] = "application/json; charset=utf-8"

    return response

# Route metrics for Prometheus
@app.route('/metrics')
def metrics():
    infura_block_number, ankr_block_number, block_diff, status = check_block_diff()

    if infura_block_number is not None and ankr_block_number is not None:
        # Update values for metrics Prometheus
        infura_block_metric.set(infura_block_number)
        ankr_block_metric.set(ankr_block_number)
        block_diff_metric.set(block_diff)

        # Statu (1 if block_diff < 5, 0 if block_diff >=5 )
        status_value = 1 if status == "success" else 0
        block_diff_status_metric.set(status_value)

    # Return metrics Prometheus
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
