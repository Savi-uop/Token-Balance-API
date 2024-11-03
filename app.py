from flask import Flask, jsonify, request
from web3 import Web3
import os

app = Flask(__name__)

# Utility function to get token balance
def get_token_balance(address):
    # Create a Web3 instance with the Infura provider
    w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))

    # Ensure the address is valid and has the correct checksum
    if not w3.isAddress(address):
        return f"Invalid address format: {address}"

    # Attempt to retrieve the balance in Wei and convert to Ether
    try:
        balance = w3.eth.get_balance(address)
        return w3.fromWei(balance, 'ether')
    except Exception as e:
        return str(e)

# Route to test connection to the backend
@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    return jsonify({"message": "Backend is connected!"}), 200


# Route to test connection to Infura
@app.route('/api/test-infura', methods=['GET'])
def test_infura():
    try:
        infura_url = os.getenv("INFURA_URL")
        w3 = Web3(Web3.HTTPProvider(infura_url))
        latest_block = w3.eth.block_number
        return jsonify({"Connected to Infura": True, "latest_block": latest_block}), 200
    except Exception as e:
        return jsonify({"Connected to Infura": False, "error": str(e)}), 500


# Route to get token balances
@app.route('/api/token-balance', methods=['POST'])
def token_balance():
    data = request.json
    addresses = data.get('addresses', [])  # This should be a list of addresses
    response = {}
    
    for address in addresses:
        try:
            balance = get_token_balance(address)  # Make sure the address is passed
            response[address] = balance
        except Exception as e:
            response[address] = str(e)

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
