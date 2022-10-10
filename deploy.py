from unittest.mock import NonCallableMagicMock
from solcx import compile_standard, install_solc
from web3 import Web3
import json

#install_solc('0.8.0') 

with open("./Voting.sol", "r") as file:
    simple_storage_file = file.read()
    #print(simple_storage_file)

# Compile Sol
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Voting.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*" : {
                    "*" : ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version = "0.8.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get Bytecode (This is walking down the JSON)
bytecode = compiled_sol["contracts"]["Voting.sol"]["DecentraPoll"]["evm"]["bytecode"]["object"]

# Get ABI
abi = compiled_sol["contracts"]["Voting.sol"]["DecentraPoll"]["abi"]

# Connecting to Ganache 
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xD1536172A5Dc13e8a37497FFc6C3E7497AF3A870"
private_key = "a95515dd9079dcc6e754cc51a93a531b6dd8ac007d96d034c92638f4ff1f51f3"

# Create the contract in Python
Voting_Contract = w3.eth.contract(abi = abi, bytecode = bytecode)

# To fully deploy (Build Contract Deploy Tx -> Sign the Tx -> Send the Tx)

#Get latest tx
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build Tx
# 2. Sign a Tx
# 3. Send a Tx
transaction = Voting_Contract.constructor().buildTransaction( {
    "gasPrice": w3.eth.gas_price, 
    "chainId": chain_id, 
    "from": my_address, 
    "nonce": nonce, }
)
signed_txn = w3.eth.account.sign_transaction(transaction,private_key = private_key)

#Send tx to chain
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with contract
voting = w3.eth.contract(address= tx_receipt.contractAddress, abi = abi)

#Call vs Transact
    # Call -> Simulate making the call and getting ta return value, dont make a state change
    # Transact -> Make a state change
store_transaction = Voting_Contract.functions.addPoll("First Test.").buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }  # this is creating a transaction
)
# then we will sign the transaction
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# we send the transaction
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# we wait for the transaction to finish
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx) 