import asyncio
from fastapi import FastAPI, HTTPException, Depends
from sentence_transformers import SentenceTransformer
from umap import UMAP
from urllib.parse import urlparse
import hdbscan
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
import torch
from aiocache import cached
from concurrent.futures import ThreadPoolExecutor
import trafilatura

torch.set_default_tensor_type('torch.FloatTensor')

# Define FastAPI app
app = FastAPI()


# Define state class for caching
class State:
    def __init__(self):
        self.results = {}
        self.sentence_model = SentenceTransformer("dangvantuan/sentence-camembert-base",
                                                  device='cpu')  # Load model at startup


state = State()


def get_state():
    return state


class UrlModel(BaseModel):
    sitemap_url: str


async def extract_text(urls):
    results = {}
    for url in urls:
        downloaded = await asyncio.get_event_loop().run_in_executor(None, trafilatura.fetch_url, url)
        if downloaded:
            result = trafilatura.extract(downloaded, no_fallback=True, include_comments=False, include_tables=False, favor_precision=True)
            if result:
                results[url] = result
    return results


def scrape_sitemap(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    urls = [loc.string for loc in soup.find_all('loc') if
            not urlparse(loc.string).path.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    # Limit to the first 2000 URLs
    urls = urls[:2000]
    return urls


@cached(ttl=600)  # Cache the result for 60 seconds
@cached(ttl=600)
@app.post("/load_urls")
async def load_urls(url_model: UrlModel, state=Depends(get_state)):
    sitemap_urls = url_model.sitemap_url.split(',')

    with ThreadPoolExecutor() as executor:
        urls = list(executor.map(scrape_sitemap, sitemap_urls))

    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".css", ".js", ".webp", ".avif"}
    urls = [url for sublist in urls for url in sublist if not any(url.endswith(ext) for ext in image_extensions)]

    data = urls
    extractor = await extract_text(data)
    print(extractor)
    documents = [{'text': text, 'url': url} for url, text in extractor.items() if url not in image_extensions]
    state.results['documents'] = documents
    return {"message": "Urls loaded successfully"}


@cached(ttl=600)  # Cache the result for 60 seconds
@app.post("/generate_embeddings")
async def generate_embeddings(state=Depends(get_state)):
    if 'documents' not in state.results:
        raise HTTPException(status_code=400, detail="No documents loaded")

    embeddings = state.sentence_model.encode([doc['text'] for doc in state.results['documents']],
                                             show_progress_bar=False)

    umap = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')
    reduced_embeddings = umap.fit_transform(embeddings)

    clustering_model = hdbscan.HDBSCAN(min_cluster_size=4, min_samples=1, metric='euclidean',
                                       cluster_selection_method='eom', gen_min_span_tree=True, prediction_data=True)
    clusters = clustering_model.fit_predict(reduced_embeddings)
    cluster_labels = clustering_model.labels_

    state.results['reduced_embeddings'] = reduced_embeddings
    state.results['cluster_labels'] = cluster_labels
    return {"message": "Embeddings generated successfully"}


@cached(ttl=600)  # Cache the result for 60 seconds
@app.get("/results")
async def get_results(state=Depends(get_state)):
    if 'reduced_embeddings' not in state.results or 'cluster_labels' not in state.results:
        raise HTTPException(status_code=400, detail="No results available")

    return {'reduced_embeddings': state.results['reduced_embeddings'].tolist(),
            'cluster_labels': state.results['cluster_labels'].tolist(),
            'urls': [doc['url'] for doc in state.results['documents']]}
