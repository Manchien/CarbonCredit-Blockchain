# By LXN
import networkx as nx
import pandas as pd
from ipywidgets import interact_manual
import gradio as gr
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# df = pd.read_csv('transactions.csv')
dataset_name = '0427data'
df = pd.read_csv(f'{dataset_name}.csv')

# Create an directed graph
G = nx.DiGraph()

for _, transaction in df.iterrows():
    # try:
    G.add_node(transaction['From'])
    #print(transaction['from'])
    G.add_node(transaction['To'])

    value = transaction['Amount']
    # value = int(transaction['value'], 16)
    # print(value)
    G.add_edge(transaction['From'], transaction['To'], weight=value)

betweenness_scores = nx.betweenness_centrality(G)
# Print the top 10 nodes with the highest betweenness centrality scores
top_nodes = sorted(betweenness_scores, key=betweenness_scores.get, reverse=True)[:10]
communities = nx.community.louvain_communities(G)



# count node degrees
degrees_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degrees_dict, 'degree')

# top 5 degrees
top_degrees = sorted(degrees_dict.items(), key=lambda x: x[1], reverse=True)[:5]
top_nodes = [node for node, _ in top_degrees]

# Create a color map based on degree
colors = [degrees_dict[n] for n in G.nodes]
cmap = plt.cm.viridis
color_map = [cmap((degree/max(colors))*1.5) for degree in colors]

# Compute the layout using Fruchterman-Reingold force-directed algorithm
pos = nx.spring_layout(G, k=5, seed=42)

nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=[v * 10 for v in degrees_dict.values()], alpha=0.6)
nx.draw_networkx_edges(G, pos, edge_color='grey', arrowsize=2, width=0.5, alpha=0.5)

labels = {node: node for node in top_nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=2, font_color='black')

# list nodes with top 5 degrees
legend_patches = [mpatches.Patch(color=cmap(degrees_dict[node]/max(colors)*1.5), label=node) for node, _ in top_degrees]
plt.legend(handles=legend_patches, fontsize=5, loc='upper right')

plt.title(dataset_name)
plt.savefig(f'0427data.png', dpi=300, bbox_inches='tight')
plt.show()

def ai_master(text_input):
    output_text = "token: " + text_input
    output_image = Image.open("0427data.png")
    return output_text, output_image

# interact_manual(ai_master, text_input='enter address');

iface = gr.Interface(
    fn=ai_master,
    inputs='text',
    outputs=['text', 'image'],
    # theme='Clean'  # 將主題更改為 Elegance
)

iface.launch()
