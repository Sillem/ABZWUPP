import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import sklearn.cluster as cl
import streamlit as st
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage

# Rysowanie wykresu z analizy skupień
def plot_results(model, title, file_name):
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
def dendogram(title, file_name):
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

