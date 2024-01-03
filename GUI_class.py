import streamlit as st
import requests
from bs4 import BeautifulSoup
from Scraper_class import Scraper
from Analityk_class import Analityk
import os
import json
import sklearn.cluster as cl
from time import time


class GUI(object):
    def __init__(self):
        self.scraper = Scraper()
        self.analityk = Analityk()

    # Wybór poziomu studiów (inżynierskie, licencjackie, magisterskie itp.)
    # Funkcja zwraca pola: selected_level oraz url do wybranej podstrony o danych poziomach studiów
    def get_level(self, selected_language, languages, selected_form, forms, levels):
        selected_level = st.selectbox("Wybierz stopień studiów: ", levels)

        if selected_language == languages[0]:
            if selected_form == forms[0]:
                if selected_level == "studia pierwszego stopnia (inżynier)":
                    url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
                elif selected_level == "studia pierwszego stopnia (licencjat)":
                    url = "https://sylabus.sggw.edu.pl/pl/1/19/3/2/40"
                elif selected_level == "studia drugiego stopnia (magister inżynier)":
                    url = "https://sylabus.sggw.edu.pl/pl/1/19/3/6/40"
                elif selected_level == "studia drugiego stopnia (magister)":
                    url = "https://sylabus.sggw.edu.pl/pl/1/19/3/3/40"
                elif selected_level == "jednolite studia magisterskie":
                    url = "https://sylabus.sggw.edu.pl/pl/1/19/3/7/40"
                else:
                    KeyError("brak linku do strony")
            else:
                if selected_level == "studia pierwszego stopnia (inżynier)":
                    url = "https://sylabus.sggw.edu.pl/pl/1/19/4/4/40"
                elif selected_level == "studia pierwszego stopnia (licencjat)":
                    url = "https://sylabus.sggw.edu.pl/pl/1/19/4/2/40"
                elif selected_level == "studia drugiego stopnia (magister inżynier)":
                    url = "https://sylabus.sggw.edu.pl/pl/1/19/4/6/40"
                elif selected_level == "studia drugiego stopnia (magister)":
                    url = "https://sylabus.sggw.edu.pl/pl/1/19/4/3/40"
                else:
                    KeyError("brak linku do strony")
        else:
            if selected_level == "studia pierwszego stopnia (inżynier)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/46"
            elif selected_level == "studia pierwszego stopnia (licencjat)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/2/46"
            elif selected_level == "studia drugiego stopnia (magister inżynier)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/6/46"
            elif selected_level == "studia drugiego stopnia (magister)":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/3/46"
            elif selected_level == "jednolite studia magisterskie":
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/7/46"
            else:
                KeyError("brak linku do strony")

        return selected_level, url

    # Wybór formy studiów (stacjo/niestacjo)
    # Funkcja zwraca pola: selected_form, czyli wybraną formę studiów, url czyli link do podstrony z daną
    # formą studiów oraz levels- zaktualizowaną listę stopni studiów
    def get_form(self, bs, selected_language, languages, forms):
        selected_form = st.selectbox("Wybierz formę studiów: ", forms)

        if selected_language == languages[0]:
            if selected_form == forms[0]:
                url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
                links_level = bs.find_all(
                    "li",
                    string=lambda text: text
                    and ("stopnia" in text or "magister" in text),
                )
                levels = [level.get_text(strip=True) for level in links_level]
            else:
                url = "https://sylabus.sggw.edu.pl/pl/1/19/4/4/40"
                links_level = bs.find_all(
                    "li",
                    string=lambda text: text
                    and ("stopnia" in text or "magister" in text),
                )
                levels = [level.get_text(strip=True) for level in links_level]
                levels.remove("jednolite studia magisterskie")
        else:
            url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/46"
            links_level = bs.find_all(
                "li",
                string=lambda text: text and ("stopnia" in text or "magister" in text),
            )
            levels = [level.get_text(strip=True) for level in links_level]

        return selected_form, url, levels

    # Wybór wydziału
    # Funkcja zwraca pola: selected_faculty, faculties, czyli wszystkie dostępne na danym
    # poziomie i formie kierunki studiów i links, czyli linki do wszystkich kierunków
    def get_faculties(self, url):
        payload = {}
        domain_url = "https://sylabus.sggw.edu.pl"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        bs = BeautifulSoup(response.content, "html.parser")
        masterElement = bs.find(class_="elements-masterElement")
        a_tags = masterElement.find_all("a")

        links = []
        faculties = []
        for i, item in enumerate(a_tags):
            faculties.append(item.get_text().strip())
            links.append(domain_url + item.get("href"))

        selected_faculty = st.selectbox("Wybierz wydział:", faculties)

        return selected_faculty, faculties, links

    # Wybór kierunku studiów
    # Funkcja zwraca pola: selected field, fields, czyli wszystkie kierunki na wydziale oraz sublinks czyli
    # podlinki do tych kierunków
    def get_field(self, sub_url):
        payload = {}
        domain_url = "https://sylabus.sggw.edu.pl"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        response = requests.request("GET", sub_url, headers=headers, data=payload)
        bs2 = BeautifulSoup(response.content, "html.parser")
        masterElement = bs2.find(class_="elements-major")
        a_tags2 = masterElement.find_all("a")
        sublinks = []
        fields = []
        for i, item in enumerate(a_tags2):
            fields.append(item.get_text().strip())
            sublinks.append(domain_url + item.get("href"))
        selected_field = st.selectbox("Wybierz kierunek: ", fields)

        return selected_field, fields, sublinks

    # Wybór języka studiów
    # Funkcja zwraca pola: selected_language, languages czyli listę języków studiów,
    # forms czyli listę form studiów oraz url czyli link do zakładki ze studiami w danym języku
    def get_language(self, bs):
        links_languages = bs.find_all(
            "li", string=lambda text: text and "prowadzone" in text
        )
        languages = [link.get_text(strip=True) for link in links_languages]
        selected_language = st.selectbox("Wybierz język studiów: ", languages)

        if selected_language == languages[0]:
            url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
            links_form = bs.find_all(
                "li", string=lambda text: text and "stacjonarne" in text
            )
            forms = [form.get_text(strip=True) for form in links_form]
        else:
            url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/46"
            links_form = bs.find_all(
                "li", string=lambda text: text and "stacjonarne" in text
            )
            forms = [form.get_text(strip=True) for form in links_form]
            forms.remove("studia niestacjonarne")

        return selected_language, languages, forms, url

    def create_formularz(self):
        url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
        payload = {}
        domain_url = "https://sylabus.sggw.edu.pl"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        bs = BeautifulSoup(response.content, "html.parser")
        st.title(
            "Aplikacja do badania zależności wiedzy i umiejętności pomiędzy przedmiotami"
        )  # Tytuł aplikacji
        ### Wybór języka studiów ###
        selected_language, languages, forms, url = self.get_language(bs)
        response = requests.request("GET", url, headers=headers, data=payload)
        bs = BeautifulSoup(response.content, "html.parser")
        ### Wybór formy studiów (stacjonarne/niestacjonarne) ###
        selected_form, url, levels = self.get_form(
            bs, selected_language, languages, forms
        )
        response = requests.request("GET", url, headers=headers, data=payload)
        bs = BeautifulSoup(response.content, "html.parser")
        ### Wybór stopnia studiów (licencjat,inżynier itp.) ###
        selected_level, url = self.get_level(
            selected_language, languages, selected_form, forms, levels
        )
        ### Wybór wydziału ###
        selected_faculty, faculties, links = self.get_faculties(url)
        for i in range(len(faculties)):
            if selected_faculty == faculties[i]:
                chosen_one = i
        ### Wybór kierunku studiów ###
        sub_url = links[chosen_one]
        selected_field, fields, sublinks = self.get_field(sub_url)

        for i in range(len(fields)):
            if selected_field == fields[i]:
                chosen_one2 = i
        sub_sub_url = sublinks[chosen_one2]
        print(sub_sub_url)
        ### Tworzenie przycisku zatwierdzającego wybory ###
        if st.button("Zatwierdź wybory"):
            start = time()
            progress_bar = st.progress(0)
            status_text = st.empty()

            effects, contents, codes = self.scraper.get_data(sub_sub_url)
            print(f"Pobieranie danych zajęło {(time() - start):.{2}f} sekund")
            # Pobieranie słowników z efektami kształcenia, treściami programowymi i kodów z wybranego kierunku
            start = time()
            self.scraper.save_data(
                selected_field
            )  # Tworzenie excela z przedmiotami wybranego kierunku z przyporządkowanymi liczbami poszczególnych kodów
            print(f"Tworzenie excela zajęło {(time() - start):.{2}f} sekund")
            default_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir)
            )
            field_names_folder = "Selected_fields_of_study"
            folder_path = os.path.join(
                default_path, field_names_folder, f"{selected_field}"
            )
            start = time()
            ### ZAPISYWANIE EFEKTÓW UCZENIA SIE ###
            with open(
                os.path.join(folder_path, "efekty_uczenia.json"), "w", encoding="utf-8"
            ) as json_file:
                json.dump(effects, json_file, ensure_ascii=False)
            ### ZAPISYWANIE TRESCI PROGRAMOWYCH ###
            with open(
                os.path.join(folder_path, "tresci_programowe.json"),
                "w",
                encoding="utf-8",
            ) as json_file:
                json.dump(contents, json_file, ensure_ascii=False)
            ### ZAPISYWANIE KODÓW ###
            with open(
                os.path.join(folder_path, "kody2.json"), "w", encoding="utf-8"
            ) as json_file:
                json.dump(codes, json_file, ensure_ascii=False)
            print(
                f"Zapisywanie treści programowych zajęło {(time() - start):.{2}f} sekund."
            )
            ### Opis kierunku ###
            start = time()
            self.scraper.get_description(selected_field, sub_sub_url)
            st.text("Wykres")
            self.analityk.draw_plot_01(selected_field)
            self.analityk.draw_plot_02(selected_field)
            self.analityk.plot_results(
                cl.KMeans(n_clusters=3), "KMeans", selected_field
            )  # próba narysowania wykresu z podziałem na klastry
            self.analityk.dendogram("ward", selected_field)  # dendogram metodą Warda
            print(f"Wyświetlanie danych zajęło {(time() - start):.{2}f} sekund")


def main():
    g = GUI()
    g.create_formularz()


main()
