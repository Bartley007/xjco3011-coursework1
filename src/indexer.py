import json
import os
import re
from collections import defaultdict
from typing import Dict, List, Any, Set

class QuoteIndexer:
    """
    Inverted Index for Quotes.
    Stores term frequency, positions, and document IDs.
    """
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.index: Dict[str, Dict[int, List[int]]] = defaultdict(lambda: defaultdict(list))
        self.documents: List[Dict[str, Any]] = []
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text, remove non-alphanumeric characters, and convert to lowercase.
        """
        return re.findall(r'\w+', text.lower())

    def build_index(self, quotes_data: List[Dict[str, Any]]):
        """
        Build inverted index from list of quotes.
        """
        self.documents = quotes_data
        self.index = defaultdict(lambda: defaultdict(list))
        
        for doc_id, doc in enumerate(self.documents):
            # Combine text, author, and tags for indexing
            content = f"{doc['text']} {doc['author']} {doc['tags']}"
            tokens = self._tokenize(content)
            
            for position, token in enumerate(tokens):
                self.index[token][doc_id].append(position)

    def save_index(self, index_file: str = "index.json", docs_file: str = "docs.json"):
        """
        Serialize and save index and documents to data/ directory.
        """
        with open(os.path.join(self.data_dir, index_file), 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False)
            
        with open(os.path.join(self.data_dir, docs_file), 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, ensure_ascii=False)

    def load_index(self, index_file: str = "index.json", docs_file: str = "docs.json"):
        """
        Load index and documents from data/ directory.
        """
        try:
            with open(os.path.join(self.data_dir, index_file), 'r', encoding='utf-8') as f:
                self.index = json.load(f)
            with open(os.path.join(self.data_dir, docs_file), 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Index files not found in data directory.")

    def get_word_index(self, word: str) -> Dict[str, Any]:
        """
        Get inverted index entry for a specific word.
        """
        word = word.lower()
        if word not in self.index:
            return {}
            
        result = {
            "word": word,
            "total_frequency": sum(len(positions) for positions in self.index[word].values()),
            "document_count": len(self.index[word]),
            "occurrences": self.index[word]
        }
        return result
