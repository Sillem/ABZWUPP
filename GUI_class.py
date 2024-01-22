import streamlit as st
import requests
from bs4 import BeautifulSoup
from Scraper_class import Scraper
from Analityk_class import Analityk
import os
import json
import sklearn.cluster as cl
from time import time
import pandas as pd


class GUI(object):
    """
    Klasa odpowiedzialna za tworzenie interfejsu i wyświetlanie wyników analiz danych uzyskanych
    za pomocą klas Analityk i Scraper.

    """

    def __init__(self):
        """
        konstruktor tworzący obiekty klas `Scraper` i `Analityk`
        """
        self.scraper = Scraper()
        self.analityk = Analityk()

    def get_level(self, selected_language, languages, selected_form, forms, levels):
        """

        Ta funkcja wybiera poziom studiow i zwraca wybrany poziom oraz URL do szczegolowych danych.

        Args:
            selected_language (str): string z nazwa wybranego jezyka
            languages (list): lista z dostepnymi jezykami do wyboru
            selected_form (str): string z nazwa wybranej formy studiow
            forms (list): lista z dostepnymi formami studiow do wyboru
            levels (list): lista z dostepnymi poziomami studiow do wyboru

        Returns:
            str selected_level: string z wybranym poziomem studiow
            str url: str z linkiem do podstrony z kierunkami studiow na danym poziomie
        """
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

    def get_form(self, bs, selected_language, languages, forms):
        """
        Wybiera formę studiów (stacjonarne/niestacjonarne) i zwraca wybraną formę,
        URL i listę dostępnych poziomów studiów.

        Args:
            bs (class 'bs4.BeautifulSoup'): obiekt klasy BeautifulSoup do tworzenia zapytan
            selected_language (str): str z nazwa wybranego jezyka studiow
            languages (list): lista z dostepnymi jezykami do wyboru
            forms (list): lista z dostepnymi formami studiow do wyboru

        Returns:
            str selected_form: string z wybrana forma studiow
            str url: string z linkiem do podstrony z kierunkami studiow na danej formie
            list levels: lista z dostepnymi poziomami studiow do wyboru
        """
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

    def get_faculties(self, url):
        """
        Ta funkcja wybiera wydział i zwraca wybrany wydział, listę dostępnych wydziałów i linki do nich.

        Args:
            url (str): string z linkiem do podstrony z wydzialami na wybranym wczesniej poziomie, formie i
            jezyku

        Returns:
            str selected_faculty: string z nazwa wybranego wydzialu
            list faculties: lista z dostepnymi do wyboru kierunkami studiow
            lista links: lista z linkami do faculties
        """
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

    def get_field(self, sub_url):
        """
        Ta funkcja wybiera kierunek studiow i zwraca pola: selected field, fields,
        czyli wszystkie kierunki na wydziale oraz sublinks czyli
        podlinki do tych kierunków
        Args:
            sub_url (str): string z linkiem do wybranego wydzialu

        Returns:
            str selected_filed: string z wybranym kierunkiem studiow
            list fields: lista z dostepnymi do wyboru kierunkami studiow
            list sublinks: lista z linkami do przedmiotow na danym kierunku
        """
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

    def get_language(self, bs):
        """
        Ta funkcja wybiera język studiów i zwraca wybrany język, listę dostępnych języków,
        dostępne formy studiów i URL strony.

        Args:
            bs (class 'bs4.BeautifulSoup'): obiekt klasy BeautifulSoup do tworzenia zapytan

        Returns:
            str selected_language: string z wybranym jezykiem studiow
            list languages: lista z dostepnymi do wyboru jezykami studiow
            list forms: lista z dostepnymi do wyboru formami studiow
            str url: string z linkiem do podstrony z kierunkami studiow w danym jezyku
        """
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
        """
        Ta funkcja odpowaida za caly interfejs aplikacji webowej tworzonej za pomoca modulu streamlit -
        wyswietlanie pol wyboru, wykresow i innych komunikatow.

        """
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

        ### Tworzenie przycisku zatwierdzającego wybory ###
        if st.button("Zatwierdź wybory"):
            st.title(selected_field)
            start = time()
            progress_bar = st.progress(0)
            status_text = st.empty()

            effects, contents, codes = self.scraper.get_data(sub_sub_url, progress_bar)
            print(f"Pobieranie danych zajęło {(time() - start):.{2}f} sekund")
            # Pobieranie słowników z efektami kształcenia, treściami programowymi i kodów z wybranego kierunku

            start = time()
            self.scraper.save_data(selected_field)
            # Tworzenie excela z przedmiotami wybranego kierunku z przyporządkowanymi liczbami poszczególnych kodów
            print(f"Tworzenie excela zajęło {(time() - start):.{2}f} sekund")
            default_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir)
            )
            field_names_folder = "Selected_fields_of_study"
            folder_path = os.path.join(
                default_path, field_names_folder, f"{selected_field}"
            )
            progress_bar.progress(80)
            ### Zapisywanie plików json ###
            start = time()
            self.scraper.save_json(selected_field, codes, effects, contents)
            print(
                f"Zapisywanie treści programowych zajęło {(time() - start):.{2}f} sekund."
            )
            progress_bar.progress(90)
            ### Opis kierunku ###
            start = time()
            st.subheader("Opis wybranego kierunku")
            self.scraper.get_description(selected_field, sub_sub_url)
            st.markdown("# Wyniki analizy")
            st.markdown("### Wykres słupkowy")
            self.analityk.draw_plot_01(selected_field)
            st.markdown("### Wykres kołowy ")
            self.analityk.draw_plot_02(selected_field)
            st.markdown("### Klasteryzacja")
            self.analityk.plot_results(
                selected_field, cl.KMeans(n_clusters=3), "KMeans"
            )  # próba narysowania wykresu z podziałem na klastry
            print("model " + str(type(cl.KMeans(n_clusters=3))))
            st.markdown("### Dendrogram")
            self.analityk.dendrogram_func(selected_field)  # dendrogram metodą Warda
            print(f"Wyświetlanie danych zajęło {(time() - start):.{2}f} sekund")
            progress_bar.progress(100)

            self.analityk.categorize_learning_contents_and_draw_plot(
                selected_field, contents
            )


def main():
    g = GUI()
    g.create_formularz()


main()
