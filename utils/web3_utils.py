from web3 import Web3
import os


def get_token_balance(address):
    # Initialize Web3 with the Infura provider
    w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))

    # Ensure the address is valid and has the correct checksum
    try:
        # Use Web3.to_checksum_address as a class method
        checksum_address = Web3.to_checksum_address(address)

        # Check if the connection is successful
        if not w3.is_connected():
            return "Failed to connect to Infura."

        # Get the balance in Wei and convert to Ether
        balance = w3.eth.get_balance(checksum_address)
        return w3.fromWei(balance, 'ether')
    except ValueError as e:
        return f"Invalid address format: {address} - {str(e)}"
    except Exception as e:
        return str(e)
