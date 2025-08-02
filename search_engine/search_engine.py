import re
from collections import defaultdict

class SearchEngine:
    def __init__(self):
        self.stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'of', 'to', 'in', 'it', 'that', 'on', 'for', 'as', 
                          'with', 'by', 'at', 'this', 'be', 'are', 'was', 'were'}
        self.word_doc_matrix = None
        self.documents = []
        self.vocabulary = set()
    
    def preprocess_text(self, text):
        """Tokenize and clean text"""
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if word not in self.stop_words]
    
    def build_matrix(self, documents):
        """Construct word-document frequency matrix"""
        self.documents = documents
        word_counts = []
        
        # Process each document
        for doc in documents:
            words = self.preprocess_text(doc)
            word_dict = defaultdict(int)
            for word in words:
                word_dict[word] += 1
                self.vocabulary.add(word)
            word_counts.append(word_dict)
        
        # Convert to matrix representation
        self.vocabulary = sorted(self.vocabulary)
        self.word_doc_matrix = []
        
        for word in self.vocabulary:
            row = []
            for doc_idx in range(len(documents)):
                row.append(word_counts[doc_idx].get(word, 0))
            self.word_doc_matrix.append(row)
        
        return self.word_doc_matrix
    
    def search(self, query, operator='AND'):
        """Search documents using AND/OR operator"""
        if not self.word_doc_matrix:
            raise ValueError("First build matrix using build_matrix()")
        
        query_words = self.preprocess_text(query)
        if not query_words:
            return []
        
        doc_scores = [0] * len(self.documents)
        found_words = set()
        
        for word in query_words:
            try:
                word_idx = self.vocabulary.index(word)
                found_words.add(word)
            except ValueError:
                continue
            
            for doc_idx in range(len(self.documents)):
                if self.word_doc_matrix[word_idx][doc_idx] > 0:
                    doc_scores[doc_idx] += 1
        
        # Handle AND/OR logic
        results = []
        if operator == 'AND':
            required = len(query_words)
            for doc_idx, score in enumerate(doc_scores):
                if score >= required and len(found_words) == len(query_words):
                    results.append((doc_idx, self.documents[doc_idx]))
        else:  # OR
            for doc_idx, score in enumerate(doc_scores):
                if score > 0:
                    results.append((doc_idx, self.documents[doc_idx]))
        
        return results
    
    def print_matrix(self):
        """Display the word-document matrix"""
        if not self.word_doc_matrix:
            print("Matrix not built yet!")
            return
        
        print(f"\n{'Word':<15}", end="")
        for i in range(len(self.documents)):
            print(f"Doc{i:<7}", end="")
        print("\n" + "-"*60)
        
        for idx, word in enumerate(self.vocabulary):
            print(f"{word:<15}", end="")
            for count in self.word_doc_matrix[idx]:
                print(f"{count:<8}", end="")
            print()

def main():
    # Sample documents
    docs = [
        "Data science is amazing",
        "machine learning and data science",
        "science and technology are evolving"
    ]
    
    # Initialize search engine
    engine = SearchEngine()
    engine.build_matrix(docs)
    
    # Display matrix
    print("Word-Document Frequency Matrix:")
    engine.print_matrix()
    
    # Interactive search
    while True:
        print("\n=== Search ===")
        query = input("Enter search terms (q to quit): ").strip()
        if query.lower() == 'q':
            break
        
        operator = input("Search type [AND/OR]: ").strip().upper()
        while operator not in ['AND', 'OR']:
            print("Invalid operator! Use AND/OR")
            operator = input("Search type [AND/OR]: ").strip().upper()
        
        results = engine.search(query, operator)
        
        print(f"\nFound {len(results)} results:")
        for idx, doc in results:
            print(f"[Doc {idx}] {doc}")

if __name__ == "__main__":
    main()