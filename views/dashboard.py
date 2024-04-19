import requests
import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import re


def dashboard():
    # Get the sitemap URL from the user
    sitemap_url = st.text_input('Enter sitemap URL')

    # If the user has entered a sitemap URL, send it to the API
    if sitemap_url:
        pattern = re.compile(r'https?://[\w\.-]+/[\w\.-]*sitemap\d*\.xml$')
        if sitemap_url:
            if not pattern.match(sitemap_url):
                st.error("Please enter a valid XML sitemap URL.")
            else:
                with st.spinner('Loading URLs...'):
                    response = requests.post('http://localhost:8000/load_urls', json={"sitemap_url": sitemap_url})
                if response.status_code == 200:
                    st.success("URLs loaded successfully")
                else:
                    st.error("Failed to load URLs")

                with st.spinner('Generating embeddings...'):
                    response = requests.post('http://localhost:8000/generate_embeddings')
                if response.status_code == 200:
                    st.success("Embeddings generated successfully")
                else:
                    st.error("Failed to generate embeddings")

                with st.spinner('Fetching results...'):
                    response = requests.get('http://localhost:8000/results')
                if response.status_code == 200:
                    results = response.json()
                    st.success("Results fetched successfully")
                    reduced_embeddings = results['reduced_embeddings']
                    cluster_labels = results['cluster_labels']
                    urls = results['urls']

                    tab1, tab2 = st.tabs(["DataFrame", "Graph"])

                    with tab1:

                        df = pd.DataFrame({
                            'URL': results['urls'],
                            'Cluster': results['cluster_labels']
                        })
                        st.dataframe(df, use_container_width=True)

                    with tab2:

                        # Now we can use the data to create a plot
                        traces = []
                        for cluster_id in set(cluster_labels):
                            cluster_embeddings = [reduced_embeddings[i] for i in range(len(reduced_embeddings)) if
                                                  cluster_labels[i] == cluster_id]
                            cluster_urls = [url for url, label in zip(urls, cluster_labels) if label == cluster_id]
                            trace = go.Scattergl(
                                x=[embedding[0] for embedding in cluster_embeddings],
                                y=[embedding[1] for embedding in cluster_embeddings],
                                mode='markers',
                                marker=dict(size=6),
                                name=f'Cluster {cluster_id}',
                                text=cluster_urls,
                                hoverinfo='text'
                            )
                            traces.append(trace)

                        layout = go.Layout(
                            title=dict(
                                text='Document Clusters',
                                x=0.1,
                                y=0.9,
                                xanchor='center',
                                yanchor='top'
                            ),
                            plot_bgcolor='white',
                            xaxis=dict(title='', showticklabels=False),
                            yaxis=dict(title='', showticklabels=False)
                        )

                        fig = go.Figure(data=traces, layout=layout)
                        fig.update_layout(height=800)
                        config = {'displayModeBar': False}
                        st.plotly_chart(fig, use_container_width=True, config=config, height=800)
                else:
                    st.error("Failed to fetch results")
