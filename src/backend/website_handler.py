import requests
from bs4 import BeautifulSoup
from backend.config_backend import ConfigBackend
from llm_engine.model_manager import ModelManager
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

class RAG_Handler():
   def __init__(self):
       pass

   def scrape_website(self, url: str):
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


   def create_database(self):
       websites = ConfigBackend.URLS
       all_docs = []
       for url in websites:
           all_docs.append(self.scrape_website(url))

       return all_docs

   def text_preparation(self, all_texts: list[dict]):

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
       print(f"{len(documents)} documents created.")

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
       return chunks

   def vectorize_and_store(self, chunks, embedding_model):
       vectorstore = FAISS.from_documents(chunks, embedding_model)
       return vectorstore

   def save_faiss_local(self, vectorestore, path="src/data/faiss_index"):
       vectorestore.save_local(path)
       print(f"FAISS-Index saved to {path}")

   def load_faiss_local(self, embedding_model, path="src/data/faiss_index"):
       print(f"Load FAISS index from {path}")
       return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)

   def search_similiar(self, vectorstore: FAISS, user_input, k: int=5):
       results = vectorstore.similarity_search_with_score(user_input, k=k)

       print(f"Top {k} results for this query: {user_input}")
       for i, (doc, score) in enumerate(results,1):
           source = doc.metadata.get('source', 'unbekannt')
           print(f"{i}. Score: {score:.4f} | Source: {source}")
           print(f"   Text: {doc.page_content[:100]}...\n")
       return results



