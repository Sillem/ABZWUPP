import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage
import sklearn.cluster as cl
import matplotlib.lines as mlines
import mplcursors
import plotly.express as px
from plotly.figure_factory import create_dendrogram
import json
import plotly.figure_factory as ff
import requests

from openpyxl import Workbook
from openpyxl.drawing.image import Image


def split_string_at_nearest_space(text):
    # Find the index of the nearest space to the center
    middle = len(text) // 2
    index = text.rfind(" ", 0, middle + 1)  # Search for space before the middle
    if index == -1:
        index = text.find(
            " ", middle
        )  # If not found, search for space after the middle

    if index != -1:
        # Split the string at the found space
        first_half = text[:index]
        second_half = text[index + 1 :]  # Exclude the space itself
        return first_half + "\n" + second_half
    else:
        # No space found, return the original string
        return text


class Analityk(object):
    """
    Klasa Analityk ma za zadanie wizualizowac dane pobrane ze strony https://sylabusy.sggw.edu.pl za pomoca
    klasy Scraper.
    """

    def draw_plot_01(self, file_name, selected_field_folder_name):
        """
        Ta funkcja rysuje wykres słupkowy z udziałem procentowym 10 najczęściej występujących
        kodów na danym kierunku nauczania.

        Args:
            file_name (str): string z nazwą wybranego kierunku studiów
            selected_field_folder_name (str): string z nazwą folderu z danymi dla wybranego kierunku studiów
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(
            default_path, "Selected_fields_of_study", f"{selected_field_folder_name}"
        )
        print("folder_path: ", folder_path)
        plot_path = os.path.join(folder_path, "Wykresy")
        file_path_excel = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path_excel).set_index("Przedmioty")

        file_path_des = os.path.join(folder_path, "opis_kodow.json")
        with open(file_path_des, "r") as plik_json:
            codes = json.load(plik_json)

        suma_codes = [df[col].sum() for col in df.columns]
        słownik = {col: suma for col, suma in zip(df.columns, suma_codes)}
        sorted_słownik = dict(
            sorted(słownik.items(), key=lambda item: item[1], reverse=True)[:10]
        )  # Sortowanie i wybór 10 największych wartości

        variable_names = list(sorted_słownik.keys())
        suma_codes = list(sorted_słownik.values())

        dict_plot = {}
        for name in variable_names:
            for kod, opis in codes.items():
                if kod == name:
                    dict_plot[kod] = opis

        # print("Słownik do wykresu: ", dict_plot)
        # Tworzenie ramki danych na podstawie słownika data
        df = pd.DataFrame(list(dict_plot.items()), columns=["Kody", "Opisy"])

        # Dodanie wartości z tablicy values do ramki danych
        df["Wartości"] = suma_codes

        fig = px.bar(
            df,
            x=variable_names,
            y=suma_codes,
            labels={"x": "Kody", "y": "Liczebność"},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis=dict(tickangle=-45),
            title="Dziesięć najczęściej występujących kodów efektów uczenia się",
            xaxis_title="Kody",
            yaxis_title="Liczebność",
        )

        st.plotly_chart(fig)

        with open(os.path.join(plot_path, "wykres słupkowy.svg"), "wb") as plot_file:
            fig.write_image(plot_file, format="svg")

    def draw_plot_02(self, file_name, selected_field_folder_name):
        """Ta funkcja rysuje wykres kołowy z procentowym udziałem 10 najczęściej występujących kodów na
        danym kierunku nauczania oraz rysuje taki sam wykres w bibliotece matplotlib do zapisania w pliku
         .svg. Funkcja tworzy plik .xlsx z rankingiem kodów występujących na danym kierunku
        nauczania.

        Args:
            file_name (str): string z nazwą wybranego kierunku studiów
            selected_field_folder_name (str): string z nazwą folderu z danymi dla wybranego kierunku studiów
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(
            default_path, "Selected_fields_of_study", f"{selected_field_folder_name}"
        )
        plot_path = os.path.join(folder_path, "Wykresy")
        file_path_excel = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path_excel).set_index("Przedmioty")

        file_path_des = os.path.join(folder_path, "opis_kodow.json")
        with open(file_path_des, "r") as plik_json:
            codes = json.load(plik_json)

        suma_codes = [df[col].sum() for col in df.columns]
        słownik = {col: suma for col, suma in zip(df.columns, suma_codes)}
        sorted_słownik = dict(
            sorted(słownik.items(), key=lambda item: item[1], reverse=True)
        )  # Sortowanie i wybór 10 największych wartości

        variable_names = list(sorted_słownik.keys())
        suma_codes = list(sorted_słownik.values())

        dict_plot = {}
        for name in variable_names:
            for kod, opis in codes.items():
                if kod == name:
                    dict_plot[kod] = opis

        # print("Słownik do wykresu: ", dict_plot)
        # Tworzenie ramki danych na podstawie słownika data
        df = pd.DataFrame(list(dict_plot.items()), columns=["Kody", "Opisy"])

        # Dodanie wartości z tablicy values do ramki danych
        df["Wartości"] = suma_codes

        # Przekształcenie danych na procenty
        df["Procentowe Wartości"] = df["Wartości"] / df["Wartości"].sum()
        df["Procentowe Wartości"] = df["Procentowe Wartości"].map("{:.2%}".format)

        fig = px.pie(
            df,
            values="Wartości",
            names="Kody",
            title="Procentowy udział występujących kodów efektów uczenia się na wybranym kierunku",
            hover_data=[
                "Procentowe Wartości"
            ],  # Dodaj dane do wyświetlania podczas najechania myszą
            labels={
                "Kody": "Kod",
                "Wartości": "Liczba wystąpień",
                "Procentowe Wartości": "Procent",
            },
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(colors=px.colors.qualitative.T10),
        )
        st.plotly_chart(fig)
        # tworzenie tabeli z opisem kodów
        st.markdown("(kliknij dwukrotnie na opis, żeby wyświetlić całość)")
        st.dataframe(data=df[["Kody", "Wartości", "Opisy"]])

        codes_ranking_path = os.path.join(plot_path, "Ranking kodów.xlsx")
        df.to_excel(codes_ranking_path, index=False)

        plt.figure(figsize=(8, 8))

        df = pd.read_excel(file_path_excel).set_index("Przedmioty")
        suma_codes = [df[col].sum() for col in df.columns]
        słownik = {col: suma for col, suma in zip(df.columns, suma_codes)}
        sorted_słownik = dict(
            sorted(słownik.items(), key=lambda item: item[1], reverse=True)
        )  # Sortowanie i wybór 10 największych wartości

        variable_names = list(sorted_słownik.keys())  # Zmienne z największymi sumami
        suma_codes = list(sorted_słownik.values())  # Sumy odpowiadające tym zmiennym
        for i in range(len(suma_codes)):
            if (suma_codes[i] / sum(suma_codes)) <= 0.019:
                variable_names[i] = "inne"
        suma = 0
        for i in range(len(suma_codes)):
            if variable_names[i] == "inne":
                suma += suma_codes[i]
        nazwy = []
        wartosci = []
        for i in range(len(suma_codes)):
            if variable_names[i] != "inne":
                nazwy.append(variable_names[i])
                wartosci.append(suma_codes[i])
        wartosci.append(suma)
        nazwy.append("inne")

        palette = plt.cm.get_cmap("tab20b", len(nazwy))
        colors = palette(np.linspace(0, 1, len(nazwy)))

        plt.pie(
            wartosci, labels=nazwy, colors=colors, autopct="%1.1f%%", startangle=140
        )
        plt.axis("equal")

        with open(
            os.path.join(plot_path, "wykres_kołowy.svg"), "w", encoding="utf-8"
        ) as plot_file:
            plt.savefig(plot_file, format="svg", bbox_inches="tight", pad_inches=0.1)

    def plot_results(
        self,
        file_name,
        selected_field_folder_name,
        model=cl.KMeans(n_clusters=3),
        title="KMeans",
    ):
        """
            Ta funkcja rysuje wykres punktowy z przypisaniem poszczegolnych przedmiotow z danego kierunku
            do podobnych klastrow za pomocą biblioteki plotly oraz rysuje taki sam wykres z wykorzystaniem
            biblioteki matplotlib do zapisania w pliku .svg.
        Args:
            model (sklearn.cluster): wybrany model z pakietu sklearn, domyslnie kmeans z podzialem na 3 klastry
            title (str):  string z nazwa wykresu
            file_name (str): string z nazwa wybranego kierunku studiow
            selected_field_folder_name (str): string z nazwą folderu z danymi dla wybranego kierunku studiów
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(
            default_path, "Selected_fields_of_study", f"{selected_field_folder_name}"
        )
        plot_path = os.path.join(folder_path, "Wykresy")
        file_path = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path).set_index("Przedmioty")

        # wykres z ruchoma etykieta
        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_df, index=df.index, columns=df.columns)
        final_df = scaled_df.copy()
        cluster_preds = model.fit_predict(final_df)
        cluster_preds += 1
        pca = PCA(n_components=2)
        dim_reduced_df = pca.fit_transform(final_df)
        dim_reduced_df = pd.DataFrame(dim_reduced_df, columns=["PC1", "PC2"])
        dim_reduced_df["Przedmiot"] = final_df.index
        dim_reduced_df["Cluster"] = cluster_preds

        dim_reduced_df["Cluster"] = dim_reduced_df["Cluster"].astype(str)
        fig = px.scatter(
            dim_reduced_df,
            x="PC1",
            y="PC2",
            color="Cluster",
            hover_data=["Przedmiot"],
            title=f"Podział obiektów wg metody {title}, liczba klastrów = {np.unique(cluster_preds).shape[0]}",
        )
        fig.update_layout()
        st.plotly_chart(fig)

        # wykres do eksportu
        cluster_preds -= 1
        dim_reduced_df = pca.fit_transform(final_df)

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(30, 24))
        if cluster_preds.size:
            ax.set_title(
                f"Podział obiektów według metody {title}, liczba klastrów = {np.unique(cluster_preds).shape[0]}"
            )
            wykres = ax.scatter(
                dim_reduced_df[:, 0], dim_reduced_df[:, 1], c=cluster_preds, cmap="cool"
            )
        else:
            wykres = ax.scatter(dim_reduced_df[:, 0], dim_reduced_df[:, 1])

        legend_handles = []
        for num, country in enumerate(final_df.index):
            plt.text(dim_reduced_df[num, 0], dim_reduced_df[num, 1], num)
        for num, country in enumerate(final_df.index):
            point_marker = mlines.Line2D(
                dim_reduced_df[0], dim_reduced_df[1], label=f"{num} - {country}"
            )
            legend_handles.append(point_marker)
        ax.legend(
            title="Legenda",
            handles=legend_handles,
            bbox_to_anchor=(1.05, 1.0),
            loc="upper left",
        )

        with open(
            os.path.join(plot_path, "wykres_klasyfikacja.svg"), "w", encoding="utf-8"
        ) as plot_file:
            plt.savefig(plot_file, format="svg", bbox_inches="tight", pad_inches=0.1)

    def dendrogram_func(self, file_name, selected_field_folder_name, title="ward"):
        """
        Ta funkcja rysuje dendrogram ukazujący związki między przedmiotami na wybranym kierunku nauczania
        oraz rysuje taki sam wykres z wykorzystaniem biblioteki matplotlib do zapisania w pliku .svg.

        Args:
            title (str): string z nazwą wybranej metody tworzenia dendrogramu, domyślnie ward
            file_name (str): string z nazwą wybranego kierunku studiów
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(
            default_path, "Selected_fields_of_study", f"{selected_field_folder_name}"
        )
        plot_path = os.path.join(folder_path, "Wykresy")
        file_path = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path).set_index("Przedmioty")

        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_df, index=df.index, columns=df.columns)
        final_df = scaled_df.copy()

        linked = linkage(final_df, f"{title}")

        # Create dendrogram with right orientation using plotly.figure_factory
        dendrogram_plt = ff.create_dendrogram(
            final_df.T, labels=df.index, orientation="left", linkagefun=lambda x: linked
        )

        dendrogram_plt.update_layout(
            xaxis=dict(title="Distance"),
            yaxis=dict(title="Objects"),
            title=f"Dendrogram - {title}",
            width=800,
            height=1200,
        )
        # Show the interactive dendrogram
        st.plotly_chart(dendrogram_plt)

        plt.figure(figsize=(12, 8))
        dendrogram(
            linked,
            labels=df.index,
            orientation="right",
            distance_sort="descending",
            show_leaf_counts=True,
        )

        plt.title(f"Dendrogram - {title}")
        plt.xlabel("Objects")
        plt.ylabel("Distance")

        with open(
            os.path.join(plot_path, "dendrogram.svg"), "w", encoding="utf-8"
        ) as plot_file:
            plt.savefig(plot_file, format="svg", bbox_inches="tight", pad_inches=0.1)

    def categorize_learning_contents_and_draw_plot(
        self, course_name, selected_field_folder_name, contents
    ):
        """Ta funkcja rysuje wykres kołowy pokazujący stopień przyporządkowania treści programowych studiów do kategorii nauk według naszego autorskiego modelu.

        Funkcja łączy treści programowe w jeden długi string, a następnie wykonuje zapytanie do backendu, na którym uruchomiony jest program zwracający wyniki. Wynikami są stopnie przyporządkowania treści do poszczególnych kategorii.

        Args:
            course_name (str): string z nazwą wybranego kierunku studiów
            selected_field_folder_name (str): string z nazwą folderu z danymi dla wybranego kierunku studiów
            contents (dict): słownik zawierający treści programowe kierunku studiów
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(
            default_path, "Selected_fields_of_study", f"{selected_field_folder_name}"
        )
        plot_path = os.path.join(folder_path, "Wykresy")
        categories_names = {
            "ekonomia-i-finanse": "Ekonomia i finanse",
            "informatyka-techniczna-i-komunikacyjna": "Informatyka techniczna i komunikacyjna",
            "inzynieria-ladowa-geodezja-i-transport": "Inżynieria lądowa, geodezja i transport",
            "inzynieria-mechaniczna": "Inżynieria mechaniczna",
            "inzynieria-srodowiska-gornictwo-i-energetyka": "Inżynieria środowiska, górnictwo i energetyka",
            "nauki-biologiczne": "Nauki biologiczne",
            "nauki-leśne": "Nauki leśne",
            "nauki-o-zarzadzaniu-i-jakosci": "Nauki o zarządzaniu i jakości",
            "nauki-socjologiczne": "Nauki socjologiczne",
            "pedagogika": "Pedagogika",
            "rolnictwo-i-ogrodnictwo": "Rolnictwo i ogrodnictwo",
            "techologia-zywnosci-i-zywienia": "Technologia żywności i żywienia",
            "weterynaria": "Weterynaria",
        }

        combined_string = ""
        for key in contents.keys():
            combined_string = (
                combined_string
                + key.replace("\xa0", " ").replace("\u2013", " ")
                + " "
                + contents[key].replace("\xa0", " ")
            )

        print("Ilość znaków treści programowych: ", len(combined_string))
        # print("Ilość wyrazów: ", len(combined_string.split()))

        ### jeśli długość treści programowych jest większa niż 150 tysięcy znaków, użyj tylko pierwszych 150 tysięcy
        if len(combined_string) > 150000:
            combined_string = combined_string[:150000]
            print(
                "Contents are larger than 150k characters. Using only first 150 characters."
            )

        try:
            wyniki = requests.post(
                "https://abzwupp-classifier.lm.r.appspot.com/predict-proba",
                json={"text": combined_string},
            ).json()

            # print(wyniki)

            df = pd.DataFrame(
                wyniki.values(),
                index=wyniki.keys(),
                columns=["Stopień przyporządkowania"],
            )
            df["Kategoria nauk"] = categories_names.values()
            df.sort_values(
                by="Stopień przyporządkowania", inplace=True, ascending=False
            )

            fig = px.pie(
                df,
                values="Stopień przyporządkowania",
                names="Kategoria nauk",
                title="Stopień przyporządkowania treści programowych kierunku do poszczególnych nauk",
                hover_data=[
                    "Kategoria nauk"
                ],  # Dodaj dane do wyświetlania podczas najechania myszą
                labels={
                    "Kategoria nauk": "Kategoria nauk",
                    "Stopień przyporządkowania": "Stopień przyporządkowania",
                },
            )
            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(colors=px.colors.qualitative.T10),
            )
            fig.update_layout(width=800)
            st.plotly_chart(fig)
            with open(
                os.path.join(plot_path, "przypisanie_dyscyplin.svg"), "wb"
            ) as plot_file:
                fig.write_image(plot_file, format="svg")
        except requests.exceptions.RequestException as e:
            # All exceptions that Requests explicitly raises inherit from requests.exceptions.RequestException.
            st.write("Kategoryzacja treści kierunku niedostępna.")
