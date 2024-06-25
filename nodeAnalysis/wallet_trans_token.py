import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_KEY = 'J8WGWVGPU54DZEW2KEPT49V1ISF6VTXHBU'
ADDRESS = '0x38B762FC4d538efD9adDEfd4F6dae8472ffD9B74'

def get_transactions(address, api_key):
    url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock=0&endblock=999999999&sort=asc&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['result']

def extract_tokens(transactions):
    token_dict = {}
    for tx in transactions:
        token_symbol = tx['tokenSymbol']
        if token_symbol in token_dict:
            token_dict[token_symbol] += 1
        else:
            token_dict[token_symbol] = 1
    return token_dict

transactions = get_transactions(ADDRESS, API_KEY)
token_dict = extract_tokens(transactions)

# 將結果寫入文件
with open('transactions.txt', 'w', encoding='utf-8') as file:
    file.write("Tokens transacted by the wallet:\n")
    for token, count in token_dict.items():
        for _ in range(count):
            file.write(f"{token}\n")

print("Results have been written to transactions.txt")