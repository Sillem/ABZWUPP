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

class Analityk(object):
    """
    Klasa Analityk ma za zadanie wizualizowac dane pobrane ze strony https://sylabusy.sggw.edu.pl za pomoca 
    klasy Scraper. 
    """
    def draw_plot_01(self, file_name):
        """ 
        Ta funkcja rysuje wykres slupkowy z udzialem procentowym 10 najczesciej wystepujacych
        kodow na danym kierunku nauczania.

        Args:
            file_name (str): string z nazwa wybranego kierunku studiow
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(default_path, "Selected_fields_of_study", f"{file_name}")
        file_path = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path).set_index('Przedmioty')

        plt.figure(figsize=(12, 6))

        suma_codes = [df[col].sum() for col in df.columns]
        słownik = {col: suma for col, suma in zip(df.columns, suma_codes)}
        sorted_słownik = dict(sorted(słownik.items(), key=lambda item: item[1], reverse=True)[:10])  # Sortowanie i wybór 10 największych wartości

        variable_names = list(sorted_słownik.keys())  # Zmienne z największymi sumami
        suma_codes = list(sorted_słownik.values())   # Sumy odpowiadające tym zmiennym

        bar_plot = plt.bar(variable_names, suma_codes, color="orange")

        plt.xticks(rotation=45, ha='right')  
        plt.xlabel('Kody')
        plt.ylabel('Liczebność')
        #plt.title('Dziesięć najczęściej występujących kodów')

        for bar, name in zip(bar_plot, variable_names):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), name, ha='center', va='bottom', fontsize=8)

        plt.grid(True)
        st.pyplot(plt)

    def draw_plot_02(self, file_name):
        """Ta funkcja rysuje wykres kolowy z procentowym udzialem 10 najczesciej wystepujacych kodow na 
        danym kierunku nauczania.

        Args:
            file_name (str): string z nazwa wybranego kierunku studiow
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(default_path, "Selected_fields_of_study", f"{file_name}")
        file_path = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path).set_index('Przedmioty')

        suma_codes = [df[col].sum() for col in df.columns]
        słownik = {col: suma for col, suma in zip(df.columns, suma_codes)}
        sorted_słownik = dict(sorted(słownik.items(), key=lambda item: item[1], reverse=True)[:10])  # Sortowanie i wybór 10 największych wartości

        variable_names = list(sorted_słownik.keys())
        suma_codes = list(sorted_słownik.values())

        palette = plt.cm.get_cmap('tab20b', len(variable_names))
        colors = palette(np.linspace(0, 1, len(variable_names)))

        plt.figure(figsize=(8, 8))
        plt.pie(suma_codes, labels=variable_names, colors = colors, autopct='%1.1f%%', startangle=140)
        #plt.title('Procentowy udział najczęściej występujących kodów')
        plt.axis('equal')

        st.pyplot(plt)
    def plot_results(self, file_name, model = cl.KMeans(n_clusters=3), title="KMeans",):
        """
            Ta funkcja rysuje wykres punktowy z przypisaniem poszczegolnych przedmiotow z danego kierunku
            do podobnych klastrow.
        
        Args:
            model (sklearn.cluster): wybrany model z pakietu sklearn, domyslnie kmeans z podzialem na 3 klastry
            title (str):  string z nazwa wykresu
            file_name (str): string z nazwa wybranego kierunku studiow
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(default_path, "Selected_fields_of_study", f"{file_name}")
        file_path = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path).set_index('Przedmioty')

        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_df, index=df.index, columns=df.columns)
        final_df = scaled_df.copy()    
        cluster_preds = model.fit_predict(final_df)
        cluster_preds +=1
        pca = PCA(n_components=2)
        dim_reduced_df = pca.fit_transform(final_df)
        dim_reduced_df = pd.DataFrame(dim_reduced_df, columns=['PC1', 'PC2'])
        dim_reduced_df['Przedmiot'] = final_df.index
        dim_reduced_df['Cluster'] = cluster_preds
        """fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))"""
        """if cluster_preds.size:
            ax.set_title(f"Podział obiektów według metody {title}, liczba klastrów = {np.unique(cluster_preds).shape[0]}")
            wykres = ax.scatter(dim_reduced_df[:, 0], dim_reduced_df[:, 1], c=cluster_preds, cmap='cool')
        else:
            wykres = ax.scatter(dim_reduced_df[:, 0], dim_reduced_df[:, 1])"""
        dim_reduced_df['Cluster'] = dim_reduced_df['Cluster'].astype(str)
        fig = px.scatter(dim_reduced_df, x='PC1', y='PC2', color='Cluster', hover_data=['Przedmiot'], title =\
                         f"Podział obiektów wg metody {title}, liczba klastrów = {np.unique(cluster_preds).shape[0]}")
        fig.update_layout()
        st.plotly_chart(fig)
        """st.pyplot(plt)"""
        """
        legend_handles =[]
        for num,country in enumerate(final_df.index):
            plt.text(dim_reduced_df[num, 0], dim_reduced_df[num,1], num)
        for num, country in enumerate(final_df.index):
            point_marker = mlines.Line2D(dim_reduced_df[0], dim_reduced_df[1], 
                                          label = f"{num} - {country}")
            legend_handles.append(point_marker) 

        ax.legend(title= "Legenda", handles = legend_handles,  bbox_to_anchor=(1.05, 1.0), loc='upper left')
        """
        
        
    def dendogram(self, file_name, title = "ward"):
        """
        Ta funkcja rysuje dendrogram ukazujacy zwiazki miedzy przedmiotami na wybranym kierunku nauczania.

        Args:
            title (str): string z nazwa wybranej metody tworzenia dendrogramu, domyslnie ward
            file_name (str): string z nazwa wybranego kierunku studiow
        """
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(default_path, "Selected_fields_of_study", f"{file_name}")
        file_path = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path).set_index('Przedmioty')

        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_df, index=df.index, columns=df.columns)
        final_df = scaled_df.copy()    
        

        linked = linkage(final_df, f"{title}")
        plt.figure(figsize=(12, 8))
        dendrogram(linked, labels = df.index,  orientation='right', distance_sort='descending', show_leaf_counts=True)

        plt.title(f"Dendrogram - {title}")
        plt.xlabel('Objects')
        plt.ylabel('Distance')
        st.pyplot(plt)
