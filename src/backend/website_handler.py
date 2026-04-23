import requests
from bs4 import BeautifulSoup
from config_backend import ConfigBackend
from pathlib import Path
import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter

def scrape_website(url: str):
    print(f"Scrape: {url}")

    site = requests.get(url)
    html = BeautifulSoup(site.text, 'html.parser')

    for element in html(['script', 'style', 'nav', 'header', 'footer']):
        element.decompose()

    text = html.get_text(separator='\n', strip=True)

    return {
        'text': text,
        'source': url
    }

def save_data(all_docs: list[str]):
    
    output_path = "src/metadata"
    # hier noch implementieren dass all_docs gespeichert wird

def create_database():
    websites = ConfigBackend.URLS
    all_docs = []
    for url in websites:
        all_docs.append(scrape_website(url))
    
    return all_docs

def text_preparation(all_texts: list[dict]):

    documents = []
    for item in all_texts:
        doc = Document(
            page_content=item['text'],
            metadata={
                'source': item['source'],
                'type': 'scraped_website'
            }
        )
        documents.append(doc)
    print(f"{len(documents)} Documents erstellt")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,          # Target size in characters
        chunk_overlap=100,       # 100-char overlap between consecutive chunks
        length_function=len,
        add_start_index=True,    # Store the original char offset in metadata
    )
    chunks = text_splitter.split_documents(documents)

    print(f"Documents → chunks: {len(documents)} → {len(chunks)}")
    print(f"Average chunk size : {sum(len(c.page_content) for c in chunks) / len(chunks):.0f} chars")
    print(f"Min / Max          : {min(len(c.page_content) for c in chunks)} / {max(len(c.page_content) for c in chunks)} chars")
    




if __name__ == '__main__':
    # Ersetzt das mit einer echten Bahn-Seite
    all_docs = create_database()
    text_preparation(all_docs)