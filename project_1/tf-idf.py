from sklearn.feature_extraction.text import TfidfVectorizer
import json

data = json.load(open("data/data.json", "r"))

# Get the documents (disease descriptions)
documents = [disease + " " + str(info) for disease, info in data.items()]

# Create the TF-IDF model
tfidf = TfidfVectorizer(stop_words="english")

# Fit and transform the documents
tfidf_matrix = tfidf.fit_transform(documents)

# Get the feature names (keywords)
feature_names = tfidf.get_feature_names_out()

# Convert TF-IDF matrix to a dense format (easy to read)
dense_matrix = tfidf_matrix.todense()

# Display the first document's TF-IDF scores
doc_tfidf = dense_matrix[0].tolist()[0]

# Get keyword-score pairs
keyword_score_pairs = {feature_names[i]: doc_tfidf[i] for i in range(len(feature_names))}

# Sort and display keywords by score
sorted_keywords = sorted(keyword_score_pairs.items(), key=lambda x: x[1], reverse=True)[:10]
print("Keywords in document 1:", sorted_keywords)

