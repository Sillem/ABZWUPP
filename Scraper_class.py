import requests
from bs4 import BeautifulSoup
import streamlit as st
import os
import openpyxl
from time import sleep


def remove_char(input_string, char_to_remove):
    result = ""
    for char in input_string:
        if char != char_to_remove:
            result += char
    return result


class Scraper(object):
    def __init__(self):
        self.subject_names = []
        self.subject_ids = []

    def create_folder(self, folder_name, path=None):
        try:
            if path is None:
                path = os.getcwd()  # Domyślna ścieżka to aktualny katalog roboczy

            new_folder_path = os.path.join(path, folder_name)

            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                print(
                    f"Folder '{folder_name}' created successfully at: {new_folder_path}"
                )
            else:
                print(f"Folder '{folder_name}' already exists at: {new_folder_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_data(self):
        field_list_codes_and_des = []
        field_codes = []
        field_codes_dict = {}
        for i in range(len(self.subject_names)):
            chosen_id = self.subject_ids[i]
            doc_url = (
                "https://sylabus.sggw.edu.pl/pl/document/" + chosen_id + ".jsonHtml"
            )

            payload = {}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
            }
            for trail in range(3):
                try:
                    response = requests.request(
                        "GET", doc_url, headers=headers, data=payload
                    )
                    continue
                except requests.exceptions.ConnectTimeout:
                    sleep(1)
            html = response.json()["html"]
            bs4 = BeautifulSoup(html, "html.parser")

            codes_and_descriptions1 = []
            codes_and_descriptions2 = []
            subject_codes = []

            for item2 in bs4.find_all("span", class_="popup"):
                if item2.get("data-bs-original-title") is not None:
                    code = remove_char(item2.get_text().strip(), ",")
                    code_description = item2.get("data-bs-original-title")
                    codes_and_descriptions1.append((code, code_description))
                if item2.get("title") is not None:
                    code = remove_char(item2.get_text().strip(), ",")
                    code_description = item2.get("title")
                    subject_codes.append(code)
                    codes_and_descriptions2.append((code, code_description))
                    field_codes.append(code)

            subject_codes = list(filter(None, subject_codes))
            field_codes_dict[self.subject_names[i]] = subject_codes

        field_list_codes_and_des = list(set(codes_and_descriptions2))
        field_codes = list(filter(None, list(set(field_codes))))

        return field_codes_dict, field_codes

    def get_effects_content_codes(self, chosen_id):
        # pobieranie efektów kształcenia i treści programowych ze strony z sylabusami
        # get effects and content
        payload = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        doc_url = "https://sylabus.sggw.edu.pl/pl/document/" + chosen_id + ".jsonHtml"
        for trail in range(3):
            try:
                response = requests.request(
                    "GET", doc_url, headers=headers, data=payload
                )
                continue
            except requests.exceptions.ConnectTimeout:
                sleep(0.1)
        html = response.json()["html"]
        bs4 = BeautifulSoup(html, "html.parser")
        course_content = ""
        learning_effects = ""

        h1s = bs4.find_all("h1")
        for h1 in h1s:
            if h1.get_text().strip() == "Efekty uczenia się dla przedmiotu":
                efekty_tag = h1.find_next()

                for i, item in enumerate(efekty_tag.find_all("td", class_="code")):
                    if (
                        "row_code" not in item["class"]
                        and "row_header" not in item["class"]
                    ):
                        if item.find("span") is None:
                            learning_effects += (
                                item.find_next().get_text().strip() + " "
                            )

            if h1.get_text().strip() == "Treści programowe":
                tresc_tag = h1.find_next()

                for i, item in enumerate(tresc_tag.find_all("td", class_="code")):
                    if (
                        "row_code" not in item["class"]
                        and "row_header" not in item["class"]
                    ):
                        the_text = item.find_next().get_text().strip()
                        course_content += the_text + " "
        # get codes
        # Pobieranie kodów kierunku ze strony z sylabusami
        doc_url = "https://sylabus.sggw.edu.pl/pl/document/" + chosen_id + ".jsonHtml"
        for trail in range(3):
            try:
                response = requests.request(
                    "GET", doc_url, headers=headers, data=payload
                )
                continue
            except requests.exceptions.ConnectTimeout:
                sleep(0.1)
        html = response.json()["html"]

        bs = BeautifulSoup(html, "html.parser")
        codes_and_descriptions = {}
        for item in bs.find_all("span", class_="popup"):
            if item.get("title") is not None:
                code = remove_char(item.get_text().strip(), ",")
                code_description = item.get("title")
                codes_and_descriptions[code] = code_description
            else:
                print("No popup title found")

        return codes_and_descriptions, learning_effects, course_content

    def save_data(self, selected_field):
        field_codes_dict, field_codes = self.create_data()
        field_codes = list(filter(lambda x: len(x) != 2, field_codes))
        wb = openpyxl.Workbook()
        sheet = wb.active

        # Wpisywanie nazwy przedmiotów w pierwszej kolumnie
        sheet["A1"] = "Przedmioty"
        for index, subject in enumerate(self.subject_names, start=2):
            sheet[f"A{index}"] = subject

        # Tworzenie nagłówków z kodów studiów
        unique_codes = set(code for code in field_codes)
        unique_codes = sorted(unique_codes)
        for index, code in enumerate(unique_codes, start=2):
            sheet[f"{openpyxl.utils.get_column_letter(index)}1"] = code

        # Wypełnianie arkusza kalkulacyjnego wartościami
        for col, subject in enumerate(self.subject_names, start=2):
            codes = field_codes_dict[subject]
            for row, code in enumerate(unique_codes, start=2):
                count = codes.count(code)
                sheet[f"{openpyxl.utils.get_column_letter(row)}{col}"] = count
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        field_names_folder = "Selected_fields_of_study"
        folder_path = os.path.join(default_path, field_names_folder)
        self.create_folder(f"{selected_field}", folder_path)
        file_path = os.path.join(folder_path, selected_field, f"{selected_field}.xlsx")
        wb.save(file_path)

    def get_data(self, sub_sub_url):
        # stare get_subject
        # Pobieranie listy przedmiotów z wybranego kierunku (ze strony z sylabusami)
        the_class = "syl-get-document syl-pointer"
        payload = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        for trail in range(3):
            try:
                response = requests.request(
                    "GET", sub_sub_url, headers=headers, data=payload
                )
                continue
            except requests.exceptions.ConnectTimeout:
                sleep(1)
        bs3 = BeautifulSoup(response.content, "html.parser")

        subject_divs = bs3.find_all(class_=the_class)
        subject_names = []
        subject_ids = []

        for i, item in enumerate(subject_divs):
            subject_names.append(item.string.strip())
            subject_ids.append(item.get("id"))
        self.subject_names = subject_names
        self.subject_ids = subject_ids
        # stare get_dictionaries
        effects = {}
        contents = {}
        codes = {}
        for index, i in enumerate(self.subject_ids):
            learning_effects, course_content = (
                self.get_effects_content_codes(i)[1],
                self.get_effects_content_codes(i)[2],
            )
            codes_and_descriptions = self.get_effects_content_codes(i)[0]
            effects[self.subject_names[index]] = learning_effects
            contents[self.subject_names[index]] = course_content
            codes[self.subject_names[index]] = codes_and_descriptions
        return effects, contents, codes

    # Opis wybranego kierunku
    def get_description(self, selected_field, sub_sub_url):
        st.write(f"Wybrany kierunek: {selected_field}")
        the_class = "syl-grid-tab-content tab-pane fade active show"
        payload = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        for trail in range(3):
            try:
                response = requests.request(
                    "GET", sub_sub_url, headers=headers, data=payload
                )
                continue
            except requests.exceptions.ConnectTimeout:
                sleep(0.1)
        bs3 = BeautifulSoup(response.content, "html.parser")
        paragraphs = bs3.find("div", {"id": "syl-grid-period-info"}).find_all("p")

        for paragraph in paragraphs:
            paragraph_text = paragraph.get_text(strip=True).replace(">", "")
            if paragraph_text != "" and paragraph_text != "Program studiów":
                st.write(paragraph_text)