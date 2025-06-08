from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()
es = Elasticsearch(os.getenv("ES_HOST"))

def index_product(product):
    es.index(index="products", id=product["id"], document=product)

def search_products(query):
    return es.search(index="products", query={"match": {"name": query}})
