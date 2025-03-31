import chromadb
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(DATA_DIR / "chromadb"))
CHROMA_SERVER_HOST = os.getenv("CHROMA_SERVER_HOST", "localhost")
CHROMA_SERVER_PORT = int(os.getenv("CHROMA_SERVER_PORT", "8000"))
def main():
    client = chromadb.HttpClient(host=CHROMA_SERVER_HOST, port=CHROMA_SERVER_PORT)
    
    
    print("Checking all collections in ChromaDB...")
    collections = client.list_collections()
    
    if not collections:
        print("No collections found.")
        return
    
    print(f"Found {len(collections)} collections:")
    
    # In ChromaDB v0.6.0, list_collections returns a list of collection names
    for coll_name in collections:
        try:
            print(f"\nCollection: {coll_name}")
            
            # Get the collection
            collection = client.get_collection(name=coll_name)
            
            # Get count
            count = collection.count()
            print(f"Document count: {count}")
            
            if count > 0:
                # Get some sample documents
                results = collection.get(limit=min(5, count))
                
                if 'ids' in results and results['ids']:
                    print(f"Sample document IDs: {results['ids']}")
                
                if 'metadatas' in results and results['metadatas']:
                    print("Sample metadata:")
                    for i, meta in enumerate(results['metadatas'][:min(3, len(results['metadatas']))]):
                        if meta:
                            print(f"  Doc {i+1}: {list(meta.keys())[:5]}")
        
        except Exception as e:
            print(f"Error examining collection {coll_info}: {e}")
    
if __name__ == "__main__":
    main()
