import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage


class Analityk(object):
    #wykres słupkowy z udziałami poszczególnych kodów
    def draw_plot_01(self, file_name):
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(default_path, "Selected_fields_of_study", f"{file_name}")
        file_path = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path).set_index('Przedmioty')


        plt.figure(figsize=(12, 6))

        suma_codes = [df[col].sum() for col in df.columns]
        variable_names = df.columns

        bar_plot = plt.bar(variable_names, suma_codes, color="orange")

        plt.xticks(rotation=45, ha='right')  
        plt.xlabel('Zmienne')
        plt.ylabel('Liczebność')
        plt.title('Liczebność dla poszczególnych kodów')

        for bar, name in zip(bar_plot, variable_names):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), name, ha='center', va='bottom', fontsize=8)

        plt.grid(True)
        st.pyplot(plt)
    # Rysowanie wykresu kołowego z procentowym udziałem poszczególnych kodów
    def draw_plot_02(self, file_name):
        current_path = os.path.dirname(__file__)
        default_path = os.path.abspath(os.path.join(current_path, os.pardir))
        folder_path = os.path.join(default_path, "Selected_fields_of_study", f"{file_name}")
        file_path = os.path.join(folder_path, f"{file_name}.xlsx")
        df = pd.read_excel(file_path).set_index('Przedmioty')

        suma_codes = [df[col].sum() for col in df.columns]
        variable_names = df.columns

        total = sum(suma_codes)
        percentages = [(count / total) * 100 for count in suma_codes]
        labels = [f'{name}' if percentage > 2 else '' for name, percentage in zip(variable_names, percentages)]

        plt.figure(figsize=(16, 10))  # Rozmiar wykresu

        # Definicja palety kolorów (tab20b)
        palette = plt.cm.get_cmap('tab20b', len(variable_names))

        # Wygenerowanie więcej kolorów z palety interpolując między dostępnymi kolorami
        colors = palette(np.linspace(0, 1, len(variable_names)))

        # Tworzenie wykresu kołowego z wygenerowanymi kolorami
        patches, _, _ = plt.pie(suma_codes, labels=labels, colors=colors, startangle=90, autopct=lambda pct: f'{pct:.1f}%' if pct > 2 else '', labeldistance=1.05)

        plt.title('Procentowy udział dla poszczególnych zmiennych', fontsize=20)  # Zwiększenie rozmiaru tytułu
        plt.legend(patches, variable_names, loc='upper right')

        plt.axis('equal')  # Ustawienie równych proporcji, aby wykres był kołem

        st.pyplot(plt)
    def plot_results(self, model, title, file_name):
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

        pca = PCA(n_components=2)
        dim_reduced_df = pca.fit_transform(final_df)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))

        if cluster_preds.size:
            ax.set_title(f"Podział obiektów według metody {title}, liczba klastrów = {np.unique(cluster_preds).shape[0]}")
            ax.scatter(dim_reduced_df[:, 0], dim_reduced_df[:, 1], c=cluster_preds, cmap='cool')
        else:
            ax.scatter(dim_reduced_df[:, 0], dim_reduced_df[:, 1])
        for num, country in enumerate(final_df.index):
            plt.text(dim_reduced_df[num, 0], dim_reduced_df[num,1], country)

        st.pyplot(plt)
    # Rysowanie dendogramu
    def dendogram(self,title, file_name):
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
