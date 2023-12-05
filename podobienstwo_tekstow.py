from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

path = os.path.join(os.getcwd(), "Selected_subjects")
content = os.listdir(path)
subjects_count = sum(os.path.isdir(os.path.join(path, element)) for element in content)

efekty = []
kody = []
tresci = []

for folder in content:
    subpath = os.path.join(path, folder)
    efekty_path = os.path.join(subpath, 'efekty_uczenia.json')
    kody_path = os.path.join(subpath, 'kody2.json')
    tresci_path = os.path.join(subpath, 'tresci_programowe.json')

    if os.path.exists(efekty_path):
        with open(efekty_path, 'r', encoding="utf-8") as file:
            efekty.append(json.dumps(json.load(file), ensure_ascii=False))
    if os.path.exists(kody_path):
        with open(kody_path, 'r', encoding="utf-8") as file:
            kody.append(json.dumps(json.load(file), ensure_ascii=False))
    if os.path.exists(tresci_path):
        with open(tresci_path, 'r', encoding="utf-8") as file:
            tresci.append(json.dumps(json.load(file), ensure_ascii=False))


###########################

# =========== #
# METODA PODOBIENSTWA COSINUSOWEGO
# =========== #


# Tworzenie macierzy wektorów cech
vectorizer_efekty = CountVectorizer().fit_transform(efekty)
vectorizer_kody = CountVectorizer().fit_transform(kody)
vectorizer_tresci = CountVectorizer().fit_transform(tresci)

# Obliczanie podobieństwa kosinusowego
print("METODA COSINUSOWA")
similarity_efekty = cosine_similarity(vectorizer_efekty)
similarity_kody = cosine_similarity(vectorizer_kody)
similarity_tresci = cosine_similarity(vectorizer_tresci)
print(similarity_efekty)
print(similarity_kody)
print(similarity_tresci)
print()

##############################


# =========== #
# METODA TF-IDF i PODOBIENSTWA COSINUSOWEGO
# =========== #


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Przekształcenie tekstu za pomocą TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix_efekty = vectorizer.fit_transform(efekty)
tfidf_matrix_kody = vectorizer.fit_transform(kody)
tfidf_matrix_tresci = vectorizer.fit_transform(tresci)

# Obliczenie macierzy podobieństwa
print("METODA TF-IDF")
similarity_matrix_efekty = cosine_similarity(tfidf_matrix_efekty, tfidf_matrix_efekty)
similarity_matrix_kody = cosine_similarity(tfidf_matrix_kody, tfidf_matrix_kody)
similarity_matrix_tresci = cosine_similarity(tfidf_matrix_tresci, tfidf_matrix_tresci)
print(similarity_matrix_efekty)
print(similarity_matrix_kody)
print(similarity_matrix_tresci)

##############################




