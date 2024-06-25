import requests
import networkx as nx
import matplotlib.pyplot as plt

API_KEY = 'J8WGWVGPU54DZEW2KEPT49V1ISF6VTXHBU'
ADDRESS = '0x38B762FC4d538efD9adDEfd4F6dae8472ffD9B74'


def get_transactions(address, api_key):
    url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock=0&endblock=999999999&sort=asc&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['result']

def count_token_transactions(transactions):
    token_counts = {}
    for tx in transactions:
        token_symbol = tx['tokenSymbol']
        if token_symbol in token_counts:
            token_counts[token_symbol] += 1
        else:
            token_counts[token_symbol] = 1
    return token_counts

def plot_pie_chart(token_counts, threshold=1):
    labels = []
    sizes = []
    other_count = 0

    for token, count in token_counts.items():
        if count <= threshold:
            other_count += count
        else:
            labels.append(token)
            sizes.append(count)
    
    if other_count > 0:
        labels.append('Other')
        sizes.append(other_count)

    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Token Transaction Distribution')
    plt.savefig('token_transaction_pie_chart.png')  # Save the figure as a PNG file
    plt.show()

def main():
    transactions = get_transactions(ADDRESS, API_KEY)
    token_counts = count_token_transactions(transactions)
    plot_pie_chart(token_counts, threshold=10)  # Merge tokens with less than or equal to 10 transactions
    print("Pie chart has been saved as token_transaction_pie_chart.png")

if __name__ == "__main__":
    main()