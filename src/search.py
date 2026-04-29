from typing import List, Dict, Any, Set
import re

class QuoteSearcher:
    """
    Search engine for Quotes using the inverted index.
    """
    def __init__(self, index: Dict[str, Dict[str, List[int]]], documents: List[Dict[str, Any]]):
        self.index = index
        self.documents = documents

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize query string.
        """
        return re.findall(r'\w+', text.lower())

    def find(self, query_words: List[str]) -> List[Dict[str, Any]]:
        """
        Find documents containing all query words (Intersection).
        """
        if not query_words:
            return []

        # Convert query words to lowercase and get their doc sets
        doc_sets = []
        for word in query_words:
            word = word.lower()
            if word in self.index:
                # Keys in index[word] are doc IDs (as strings due to JSON)
                doc_sets.append(set(map(int, self.index[word].keys())))
            else:
                # If any word is not found, the intersection will be empty
                return []

        # Find intersection of all doc sets
        if not doc_sets:
            return []
            
        common_doc_ids = set.intersection(*doc_sets)
        
        # Return the actual document content
        results = []
        for doc_id in sorted(common_doc_ids):
            if doc_id < len(self.documents):
                results.append(self.documents[doc_id])
                
        return results
