from solcx import compile_standard, install_solc
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

# Load smart contract source code
with open("./SolveMe.sol", "r") as file:
    solveme_file = file.read()

# Install complile version
install_solc('0.8.0')

# Compile the smart contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"SolveMe.sol": {"content": solveme_file}},
    "settings": {
        "outputSelection": {
            "*" : {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    },
},
solc_version="0.8.0",
)

# Write the compiled code. Useful info to extract the bytecode and abi
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# Get bytecode from complied code
bytecode = compiled_sol["contracts"]["SolveMe.sol"]["SolveMe"]["evm"]["bytecode"]["object"]


# Get ABI from complied code
abi = compiled_sol["contracts"]["SolveMe.sol"]["SolveMe"]["abi"]


# Connect to the blockchain
w3 = Web3(Web3.HTTPProvider("https://blockchain-solveme-7daf9384e419044f-eth.2022.ductf.dev:443"))

# Fix issue with middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Information from the challenge
chain_id = 31337
my_address = "0x02b35b4804e95bA8c5bF4104e8939b0E1f9E3126"
private_key = "0x7752b93dff30096398ed18bb76830db85fe4d267ab4a644c2d7aaf1d92f8cf36"
contract_address = "0x734B26e5cfF97983704D92202760f83372784061"

# Get nonce
nonce = w3.eth.getTransactionCount(my_address)


# Connect to the contract
ctfcontract = w3.eth.contract(contract_address, abi=abi)


# STEPS TO CREATE A TRANSACTION
# 1 - Create a transaction
# 2 - Sign transaction
# 3 - Send transaction

# ------ TRANSACTION PART ------
# 1 - Create a transaction -> Execute function solveChallenge()
ctf_transaction = ctfcontract.functions.solveChallenge().buildTransaction(
    {"chainId": chain_id,
    "from": my_address,
    "nonce": nonce,
    "gasPrice": w3.eth.gas_price
    }
)

# 2 - Sign transaction
signed_ctf_txn = w3.eth.account.sign_transaction(ctf_transaction, private_key=private_key)

# 3 - Send transaction
send_ctf_tx = w3.eth.send_raw_transaction(signed_ctf_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_ctf_tx)

print("Successful transaction! Check the changes in the blockchain.")
print(f'Transaction hash: { tx_receipt.transactionHash.hex() }')
