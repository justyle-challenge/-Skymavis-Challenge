from flask import Flask, jsonify, Response
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

INFURA_ENDPOINT_ID = os.getenv('INFURA_ENDPOINT_ID')
INFURA_URL = f"https://mainnet.infura.io/v3/{INFURA_ENDPOINT_ID}"
ANKR_URL = "https://rpc.ankr.com/eth"

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

@app.route('/block_diff_status', methods=['GET'])
def block_diff_status():

    infura_block_number = get_block_number(INFURA_URL, 'Infura')
    ankr_block_number = get_block_number(ANKR_URL, 'Ankr')

    if infura_block_number is None or ankr_block_number is None:
        # If no targets should be transmitted, HTTP 200 must also be emitted, with an empty list []
        targets = []
        # return jsonify({"status": "fail", "message": "Error fetching block numbers"}), 500

    else:
        block_diff = abs(infura_block_number - ankr_block_number)
        status = "success" if block_diff < 5 else "fail"

        targets = [
            {
                "targets": ["infura"],
                "labels": {
                    "job": "ethereum",
                    "provider": "Infura",
                    "block_number": str(infura_block_number)
                }
            },
            {
                "targets": ["ankr"],
                "labels": {
                    "job": "ethereum",
                    "provider": "Ankr",
                    "block_number": str(ankr_block_number)
                }
            },
            {
                "targets": ["block_diff_status"],
                "labels": {
                    "block_diff": str(block_diff),
                    "status": status,
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
