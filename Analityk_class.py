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

    def draw_plot_01(self, file_name):
        """
        Ta funkcja rysuje wykres słupkowy z udziałem procentowym 10 najczęściej występujących
        kodów na danym kierunku nauczania.

        Args:
            file_name (str): string z nazwą wybranego kierunku studiów
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(
            default_path, "Selected_fields_of_study", f"{file_name}"
        )
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

        # Skrócenie opisów do jednego zdania
        # df["Opis_skrocony"] = df["Opisy"].apply(
        #     lambda x: "xdddddd" + x  # split_string_at_nearest_space(x)
        # )
        # Wybór pierwszego zdania jako skrócony opis

        fig = px.bar(
            df,
            x=variable_names,
            y=suma_codes,
            labels={"x": "Kody", "y": "Liczebność"},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis=dict(tickangle=-45),
            title="Dziesięć najczęściej występujących kodów",
            xaxis_title="Kody",
            yaxis_title="Liczebność",
        )

        st.plotly_chart(fig)

    # def draw_plot_01(self, file_name):
    #     """
    #     Ta funkcja rysuje wykres słupkowy z udziałem procentowym 10 najczęściej występujących
    #     kodów na danym kierunku nauczania.

    #     Args:
    #         file_name (str): string z nazwą wybranego kierunku studiów
    #     """
    #     current_path = os.path.dirname(__file__)
    #     default_path = os.path.abspath(os.path.join(current_path, os.pardir))
    #     folder_path = os.path.join(default_path, "Selected_fields_of_study", f"{file_name}")

    #     file_path = os.path.join(folder_path, f"{file_name}.xlsx")
    #     df = pd.read_excel(file_path).set_index("Przedmioty")

    #     plt.figure(figsize=(12, 6))

    #     suma_codes = [df[col].sum() for col in df.columns]
    #     słownik = {col: suma for col, suma in zip(df.columns, suma_codes)}
    #     sorted_słownik = dict(sorted(słownik.items(), key=lambda item: item[1], reverse=True)[:10])  # Sortowanie i wybór 10 największych wartości

    #     variable_names = list(sorted_słownik.keys()) # Zmienne z największymi sumami
    #     suma_codes = list(sorted_słownik.values()) # Sumy odpowiadające tym zmiennym

    #     bar_plot = plt.bar(variable_names, suma_codes, color = "orange")

    #     plt.xticks(rotation = 45, ha = 'right')
    #     plt.xlabel('Kody')
    #     plt.ylabel('Liczebność')

    #     for bar, name in zip(bar_plot, variable_names):
    #         plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), name, ha = 'center', va = 'bottom', fontsize = 8)

    #     plt.grid(True)
    #     st.pyplot(plt)

    def draw_plot_02(self, file_name):
        """Ta funkcja rysuje wykres kołowy z procentowym udziałem 10 najczęściej występujących kodów na
        danym kierunku nauczania.

        Args:
            file_name (str): string z nazwą wybranego kierunku studiów
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(
            default_path, "Selected_fields_of_study", f"{file_name}"
        )
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

        print(df)
        # # Top 10 najczęściej występujących
        # top_10_codes = df[:10]

        # Skrócenie opisów do jednego zdania
        # Wybór pierwszego zdania jako skrócony opis
        # df["Opis_skrocony"] = df["Opisy"].apply(lambda x: x.split(".")[0])
        # print(df)

        fig = px.pie(
            df,
            values="Wartości",
            names="Kody",
            title="Procentowy udział występujących kodów na wybranym kierunku",
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
        st.markdown("(kliknij dwukrotnie na opis, żeby wyświetlić całość)")
        st.dataframe(data=df[["Kody", "Wartości", "Opisy"]])

        codes_ranking_path = os.path.join(folder_path, "Ranking kodów.xlsx")
        df.to_excel(codes_ranking_path, index=False)

    # def draw_plot_02(self, file_name):
    #     """
    #     Ta funkcja rysuje wykres kołowy z udziałem procentowym 10 najczęściej występujących
    #     kodów na danym kierunku nauczania.

    #     Args:
    #         file_name (str): string z nazwą wybranego kierunku studiów
    #     """
    #     current_path = os.path.dirname(__file__)
    #     default_path = os.path.abspath(os.path.join(current_path, os.pardir))
    #     folder_path = os.path.join(default_path, "Selected_fields_of_study", f"{file_name}")

    #     file_path = os.path.join(folder_path, f"{file_name}.xlsx")
    #     df = pd.read_excel(file_path).set_index("Przedmioty")

    #     plt.figure(figsize=(8, 8))

    #     suma_codes = [df[col].sum() for col in df.columns]
    #     słownik = {col: suma for col, suma in zip(df.columns, suma_codes)}
    #     sorted_słownik = dict(sorted(słownik.items(), key=lambda item: item[1], reverse=True)[:10])  # Sortowanie i wybór 10 największych wartości

    #     variable_names = list(sorted_słownik.keys())  # Zmienne z największymi sumami
    #     suma_codes = list(sorted_słownik.values())   # Sumy odpowiadające tym zmiennym

    #     palette = plt.cm.get_cmap('tab20b', len(variable_names))
    #     colors = palette(np.linspace(0, 1, len(variable_names)))

    #     plt.pie(suma_codes, labels=variable_names, colors=colors, autopct='%1.1f%%', startangle=140)
    #     plt.axis('equal')

    #     st.pyplot(plt)

    def plot_results(
        self,
        file_name,
        model=cl.KMeans(n_clusters=3),
        title="KMeans",
    ):
        """
            Ta funkcja rysuje wykres punktowy z przypisaniem poszczegolnych przedmiotow z danego kierunku
            do podobnych klastrow za pomocą biblioteki plotly oraz rysuje taki sam wykres z wykorzystaniem
            biblioteki matplotlib do zapisania w pliku .xslx.
        Args:
            model (sklearn.cluster): wybrany model z pakietu sklearn, domyslnie kmeans z podzialem na 3 klastry
            title (str):  string z nazwa wykresu
            file_name (str): string z nazwa wybranego kierunku studiow
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(
            default_path, "Selected_fields_of_study", f"{file_name}"
        )
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
        plt.savefig("wykres.svg", format="svg", bbox_inches="tight", pad_inches=0.1)

    # def dendrogram_func(self, file_name, title="ward"):
    #     """
    #     Ta funkcja rysuje dendrogram ukazujący związki między przedmiotami na wybranym kierunku nauczania.

    #     Args:
    #         title (str): string z nazwą wybranej metody tworzenia dendrogramu, domyślnie ward
    #         file_name (str): string z nazwą wybranego kierunku studiów
    #     """
    #     current_path = os.path.dirname(__file__)
    #     default_path = os.path.abspath(os.path.join(current_path, os.pardir))
    #     folder_path = os.path.join(
    #         default_path, "Selected_fields_of_study", f"{file_name}"
    #     )
    #     file_path = os.path.join(folder_path, f"{file_name}.xlsx")
    #     df = pd.read_excel(file_path).set_index("Przedmioty")

    #     scaler = StandardScaler()
    #     scaled_df = scaler.fit_transform(df)
    #     scaled_df = pd.DataFrame(scaled_df, index=df.index, columns=df.columns)
    #     final_df = scaled_df.copy()

    #     linked = linkage(final_df, f"{title}")
    #     plt.figure(figsize=(12, 8))
    #     dendrogram(
    #         linked,
    #         labels=df.index,
    #         orientation="right",
    #         distance_sort="descending",
    #         show_leaf_counts=True,
    #     )

    #     plt.title(f"Dendrogram - {title}")
    #     plt.xlabel("Objects")
    #     plt.ylabel("Distance")
    #     st.pyplot(plt)

    def dendrogram_func(self, file_name, title="ward"):
        """
        Ta funkcja rysuje dendrogram ukazujący związki między przedmiotami na wybranym kierunku nauczania.

        Args:
            title (str): string z nazwą wybranej metody tworzenia dendrogramu, domyślnie ward
            file_name (str): string z nazwą wybranego kierunku studiów
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(
            default_path, "Selected_fields_of_study", f"{file_name}"
        )
        file_path = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path).set_index("Przedmioty")

        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_df, index=df.index, columns=df.columns)
        final_df = scaled_df.copy()

        linked = linkage(final_df, f"{title}")

        # Create dendrogram with right orientation using plotly.figure_factory
        dendrogram = ff.create_dendrogram(
            final_df.T, labels=df.index, orientation="left", linkagefun=lambda x: linked
        )

        dendrogram.update_layout(
            xaxis=dict(title="Distance"),
            yaxis=dict(title="Objects"),
            title=f"Dendrogram - {title}",
            width=800,
            height=600,
        )

        # Show the interactive dendrogram
        st.plotly_chart(dendrogram)
