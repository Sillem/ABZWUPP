import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage


# Rysowanie wykresu częstoci występowania poszczególnych zmiennych
def draw_plot_01(file_name):
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
def draw_plot_02(file_name):
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




