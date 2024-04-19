import streamlit as st
import plotly.graph_objs as go
import pickle

# Load results
with open('results.pkl', 'rb') as f:
    results = pickle.load(f)

reduced_embeddings = results['reduced_embeddings']
cluster_labels = results['cluster_labels']
urls = results['urls']

traces = []
for cluster_id in set(cluster_labels):
    cluster_embeddings = reduced_embeddings[cluster_labels == cluster_id]
    cluster_urls = [url for url, label in zip(urls, cluster_labels) if label == cluster_id]
    trace = go.Scattergl(
        x=cluster_embeddings[:, 0],
        y=cluster_embeddings[:, 1],
        mode='markers',
        marker=dict(size=6),
        name=f'Cluster {cluster_id}',
        text=cluster_urls,
        hoverinfo='text'
    )
    traces.append(trace)

layout = go.Layout(
    title='Document Clusters',
    plot_bgcolor='white',
    xaxis=dict(title='UMAP 1', showticklabels=False),
    yaxis=dict(title='UMAP 2', showticklabels=False)
)

fig = go.Figure(data=traces, layout=layout)
config = {'displayModeBar': False}
st.plotly_chart(fig, config=config)
