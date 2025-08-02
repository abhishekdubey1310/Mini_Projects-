import re
documents = [
    "Data science is amazing",
    "Machine Learning and data science ",
    "science and technology are evoling"
]
stop_words = {'a', 'an', 'the', 'and', 'or', 'is', 'are', 'in', 'on', 'at'}
all_clean_words = []
for doc in documents:
    words = re.findall(r'\w+', doc.lower())
    clean_words = [word for word in words if word not in stop_words]
    all_clean_words.append(clean_words)

unique_words = []
for doc_words in all_clean_words:
    for word in doc_words:
        if word not in unique_words:
            unique_words.append(word)

word_matrix = []
for word in unique_words:
    row = []
    for doc_words in all_clean_words:
        row.append(doc_words.count(word))
    word_matrix.append(row)

print("\nWord".ljust(15), end="")
for i in range(len(documents)):
    print(f"Doc{i}".ljust(8), end="")
print("\n" + "-"*50)

for i in range(len(unique_words)):
    print(unique_words[i].ljust(15), end="")
    for count in word_matrix[i]:
        print(str(count).ljust(8), end="")
    print()

while True:
    print("\n--- Search ---")
    search_terms = input("Enter words to search (or 'quit'): ").strip().lower()
    
    if search_terms == 'quit':
        break
    
    search_words = re.findall(r'\w+', search_terms)
    search_words = [word for word in search_words if word not in stop_words]
    
    results = []
    for doc_index in range(len(documents)):
        all_found = True
        for word in search_words:
            if word in unique_words:
                word_index = unique_words.index(word)
                if word_matrix[word_index][doc_index] == 0:
                    all_found = False
                    break
            else:
                all_found = False
                break
        
        if all_found and search_words:
            results.append((doc_index, documents[doc_index]))
    
    print(f"\nFound {len(results)} results:")
    for i, (doc_id, doc) in enumerate(results, 1):
        print(f"{i}. [Doc{doc_id}] {doc}")
        search_type = input("Search type (AND/OR): ").strip().upper()
    while search_type not in ['AND', 'OR']:
        print("Invalid option! Use AND or OR")
        search_type = input("Search type (AND/OR): ").strip().upper()
    
    search_words = re.findall(r'\w+', search_terms)
    search_words = [word for word in search_words if word not in stop_words]
    
    results = []
    for doc_index in range(len(documents)):
        matches = 0
        for word in search_words:
            if word in unique_words:
                word_index = unique_words.index(word)
                if word_matrix[word_index][doc_index] > 0:
                    matches += 1
        
    search_type = input("Search type (AND/OR): ").strip().upper()
    while search_type not in ['AND', 'OR']:
        print("Invalid option! Use AND or OR")
        search_type = input("Search type (AND/OR): ").strip().upper()
    
    search_words = re.findall(r'\w+', search_terms)
    search_words = [word for word in search_words if word not in stop_words]
    
    results = []
    for doc_index in range(len(documents)):
        matches = 0
        for word in search_words:
            if word in unique_words:
                word_index = unique_words.index(word)
                if word_matrix[word_index][doc_index] > 0:
                    matches += 1
        
        if search_type == 'AND' and matches == len(search_words):
            results.append((doc_index, documents[doc_index]))
        elif search_type == 'OR' and matches > 0:
            results.append((doc_index, documents[doc_index]))
    
    print(f"\nFound {len(results)} results:")
    for i, (doc_id, doc) in enumerate(results, 1):
        print(f"{i}. [Doc{doc_id}] {doc}")