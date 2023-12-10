import sys
import os

current_path = os.path.dirname(__file__)
default_path = os.path.abspath(os.path.join(current_path, os.pardir))
scrapping_path = os.path.join(default_path, "Scraping")
analiza_path = os.path.join(default_path, "Analiza")
sys.path.append(default_path)
sys.path.append(scrapping_path)
sys.path.append(analiza_path)

from bs4 import BeautifulSoup
from requests import get
import requests
import json
import streamlit as st
from utils import remove_char, create_folder
from codes_writer import create_data, save_data
from language import get_language
from form import get_form
from level import get_level
from faculties import get_faculties
from subjects import get_subject
from fields_of_study import get_field
from efekty_i_tresci import get_dictionaries
from plots import draw_plot_01, draw_plot_02
from analiza import plot_results, dendogram
from description import get_description
import sklearn.cluster as cl


### URL do strony z sylabusami ###
url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
domain_url = "https://sylabus.sggw.edu.pl"
payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, headers = headers, data = payload)
bs = BeautifulSoup(response.content, "html.parser")


st.title("Aplikacja do badania zależności wiedzy i umiejętności pomiędzy przedmiotami") # Tytuł aplikacji


### Wybór języka studiów ###
selected_language, languages, forms, url = get_language(bs)
response = requests.request("GET", url, headers=headers, data=payload)
bs = BeautifulSoup(response.content, "html.parser")


### Wybór formy studiów (stacjonarne/niestacjonarne) ###
selected_form, url, levels = get_form(bs, selected_language, languages, forms)
response = requests.request("GET", url, headers = headers, data = payload)
bs = BeautifulSoup(response.content, "html.parser")


### Wybór stopnia studiów (licencjat,inżynier itp.) ###
selected_level, url = get_level(selected_language, languages, selected_form, forms, levels)


### Wybór wydziału ###
selected_faculty, faculties, links = get_faculties(url)
for i in range(len(faculties)):
    if selected_faculty == faculties[i]:
        chosen_one = i


### Wybór kierunku studiów ###
sub_url = links[chosen_one]
selected_field, fields, sublinks = get_field(sub_url)

for i in range(len(fields)):
    if selected_field == fields[i]:
        chosen_one2 = i
sub_sub_url = sublinks[chosen_one2]


### Pobieranie nazwy przedmiotów i ich id z wybranego kierunku ###
subject_names, subject_ids = get_subject(sub_sub_url)


### Tworzenie przycisku zatwierdzającego wybory ###
if st.button('Zatwierdź wybory'):
    
        
    # for i, item in enumerate(subject_names):
    #     if item == selected_subject:
    #         subject_chosen = i
    
    # chosen_id = subject_ids[subject_chosen]
    # course_name = subject_names[subject_chosen]
    # print("Chosen ", course_name)

    effects, contents, codes = get_dictionaries(subject_names, subject_ids) # Pobieranie słowników z efektami kształcenia, treściami programowymi i kodów z wybranego kierunku

    save_data(subject_names, subject_ids, selected_field) # Tworzenie excela z przedmiotami wybranego kierunku z przyporządkowanymi liczbami poszczególnych kodów

    default_path = os.path.abspath(os.path.join(current_path, os.pardir))
    # folder_subjects_name = "Selected_subjects"
    # create_folder(folder_subjects_name, default_path)
    # Create a path for the subfolder within the current directory
    # subfolder_path = os.path.join(default_path, folder_subjects_name)
    
    # create_folder(course_name, subfolder_path)
    # subject_folder_path = os.path.join(subfolder_path, course_name)

    field_names_folder = "Selected_fields_of_study"
    folder_path = os.path.join(default_path, field_names_folder, f"{selected_field}")

    ### ZAPISYWANIE EFEKTÓW UCZENIA SIE ###
    with open(
        os.path.join(folder_path, "efekty_uczenia.json"), "w", encoding="utf-8"
    ) as json_file:
        json.dump(effects, json_file, ensure_ascii=False)

    ### ZAPISYWANIE TRESCI PROGRAMOWYCH ###
    with open(
        os.path.join(folder_path, "tresci_programowe.json"), "w", encoding="utf-8"
    ) as json_file:
        json.dump(contents, json_file, ensure_ascii=False)

    ### ZAPISYWANIE KODÓW ###
    with open(
        os.path.join(folder_path, "kody2.json"), "w", encoding="utf-8"
    ) as json_file:
        json.dump(codes, json_file, ensure_ascii=False)

    ### Opis kierunku ###
    get_description(selected_field, sub_sub_url)

    st.text("Wykres")
    draw_plot_01(selected_field) # wykres częstości występujących kodów
    draw_plot_02(selected_field) # wykres kołowy z procentowym udziałem poszczególnych kodów
    plot_results(cl.KMeans(n_clusters=3), "KMeans", selected_field) # próba narysowania wykresu z podziałem na klastry
    dendogram("ward", selected_field) # dendogram metodą Warda