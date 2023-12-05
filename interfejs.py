from bs4 import BeautifulSoup
from requests import get
import requests
import time, datetime
import json
import os
import streamlit as st
from utils import remove_char, create_folder
from codes_writer import create_data, save_data
from language import get_language
from form import get_form
from level import get_level
from faculties import get_faculties
from subjects import get_subject
from fields_of_study import get_field
from efekty_i_tresci import get_effects_and_content, get_codes

url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
domain_url = "https://sylabus.sggw.edu.pl"

payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, headers = headers, data = payload)
bs = BeautifulSoup(response.content, "html.parser")

st.title("Aplikacja do badania zależności wiedzy i umiejętności pomiędzy przedmiotami")

### Languages ###
selected_language, languages, forms, url = get_language(bs)

response = requests.request("GET", url, headers=headers, data=payload)
bs = BeautifulSoup(response.content, "html.parser")


### Study Form ###
selected_form, url, levels = get_form(bs, selected_language, languages, forms)

response = requests.request("GET", url, headers = headers, data = payload)
bs = BeautifulSoup(response.content, "html.parser")


### Study Level ###
selected_level, url = get_level(selected_language, languages, selected_form, forms, levels)


### Faculties ###
selected_faculty, faculties, links = get_faculties(url)

for i in range(len(faculties)):
    if selected_faculty == faculties[i]:
        chosen_one = i


### Fields of study ###
sub_url = links[chosen_one]
selected_field, fields, sublinks = get_field(sub_url)

for i in range(len(fields)):
    if selected_field == fields[i]:
        chosen_one2 = i
sub_sub_url = sublinks[chosen_one2]

### Subjects ###
selected_subject, subject_names, subject_ids = get_subject(sub_sub_url)


if st.button('Zatwierdź wybory'):
    for i, item in enumerate(subject_names):
        if item == selected_subject:
            subject_chosen = i
    
    chosen_id = subject_ids[subject_chosen]
    course_name = subject_names[subject_chosen]
    print("Chosen ", course_name)

    learning_effects, course_content = get_effects_and_content(chosen_id)

    save_data(subject_names, subject_ids, selected_field)

    codes_and_descriptions = get_codes(chosen_id)

    folder_subjects_name = "Selected_subjects"
    create_folder(folder_subjects_name)
    # Create a path for the subfolder within the current directory
    subfolder_path = os.path.join(os.getcwd(), folder_subjects_name)
    
    create_folder(course_name, subfolder_path)
    subject_folder_path = os.path.join(subfolder_path, course_name)



    ### ZAPISYWANIE EFEKTÓW UCZENIA SIE ###
    with open(
        os.path.join(subject_folder_path, "efekty_uczenia.json"), "w", encoding="utf-8"
    ) as json_file:
        json.dump(learning_effects, json_file, ensure_ascii=False)

    ### ZAPISYWANIE TRESCI PROGRAMOWYCH ###
    with open(
        os.path.join(subject_folder_path, "tresci_programowe.json"), "w", encoding="utf-8"
    ) as json_file:
        json.dump(course_content, json_file, ensure_ascii=False)

    ### ZAPISYWANIE KODÓW ###
    with open(
        os.path.join(subject_folder_path, "kody2.json"), "w", encoding="utf-8"
    ) as json_file:
        json.dump(codes_and_descriptions[1:], json_file, ensure_ascii=False)

