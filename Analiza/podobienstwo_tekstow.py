from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import streamlit as st



# Określanie podobieństwa między efektami, treściami i opisami kodów między poszczególnymi przedmiotami wybranego kierunku
def text_similarity(file_name):

    current_path = os.path.dirname(__file__)
    default_path = os.path.abspath(os.path.join(current_path, os.pardir))
    folder_path = os.path.join(default_path, "Selected_fields_of_study", f"{file_name}")
    # content = os.listdir(folder_path)
    # subjects_count = sum(os.path.isdir(os.path.join(path, element)) for element in content)


    efekty = []
    kody = []
    tresci = []
    opisy_kodow = []
    przedmioty = []

    efekty_path = os.path.join(folder_path, 'efekty_uczenia.json')
    kody_path = os.path.join(folder_path, 'kody2.json')
    tresci_path = os.path.join(folder_path, 'tresci_programowe.json')

    if os.path.exists(efekty_path):
        with open(efekty_path, 'r', encoding="utf-8") as file:
            efekty_dict = json.load(file)
    if os.path.exists(kody_path):
        with open(kody_path, 'r', encoding="utf-8") as file:
            kody_dict = json.load(file)
    if os.path.exists(tresci_path):
        with open(tresci_path, 'r', encoding="utf-8") as file:
            tresci_dict = json.load(file)


    for klucz_01, klucz_02 in zip(efekty_dict, tresci_dict):
        efekty.append(efekty_dict[klucz_01])
        tresci.append(tresci_dict[klucz_02])
        przedmioty.append(klucz_01)

    for klucz_01, podslownik in kody_dict.items():
        for klucz_02, wartosc in podslownik.items():
            kody.append(klucz_02)
            opisy_kodow.append(wartosc)

    ###########################

    # =========== #
    # METODA PODOBIENSTWA COSINUSOWEGO
    # =========== #


    # Tworzenie macierzy wektorów cech
    vectorizer_efekty = CountVectorizer().fit_transform(efekty)
    vectorizer_kody = CountVectorizer().fit_transform(kody)
    vectorizer_tresci = CountVectorizer().fit_transform(tresci)
    vectorizer_opisy_kodow = CountVectorizer().fit_transform(opisy_kodow)

    # Obliczanie podobieństwa kosinusowego
    print("METODA COSINUSOWA")
    similarity_efekty = cosine_similarity(vectorizer_efekty)
    similarity_kody = cosine_similarity(vectorizer_kody)
    similarity_tresci = cosine_similarity(vectorizer_tresci)
    similarity_opisy_kodow = cosine_similarity(vectorizer_opisy_kodow)
    print(similarity_efekty)
    print(similarity_kody)
    print(similarity_tresci)
    print(similarity_opisy_kodow)
    print()

    ##############################


    # =========== #
    # METODA TF-IDF i PODOBIENSTWA COSINUSOWEGO
    # =========== #


    # Przekształcenie tekstu za pomocą TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix_efekty = vectorizer.fit_transform(efekty)
    tfidf_matrix_kody = vectorizer.fit_transform(kody)
    tfidf_matrix_tresci = vectorizer.fit_transform(tresci)
    tfidf_matrix_opisy_kodow = vectorizer.fit_transform(opisy_kodow)

    # Obliczenie macierzy podobieństwa
    print("METODA TF-IDF")
    similarity_matrix_efekty = cosine_similarity(tfidf_matrix_efekty, tfidf_matrix_efekty)
    similarity_matrix_kody = cosine_similarity(tfidf_matrix_kody, tfidf_matrix_kody)
    similarity_matrix_tresci = cosine_similarity(tfidf_matrix_tresci, tfidf_matrix_tresci)
    similarity_matrix_opisy_kodow = cosine_similarity(tfidf_matrix_opisy_kodow, tfidf_matrix_opisy_kodow)

    print(similarity_matrix_efekty)
    print(similarity_matrix_kody)
    print(similarity_matrix_tresci)
    print(similarity_matrix_opisy_kodow)
    ##############################




text_similarity("informatyka")