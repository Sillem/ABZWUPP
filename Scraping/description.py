import requests
import streamlit as st
from bs4 import BeautifulSoup

# Opis wybranego kierunku
def get_description(selected_field, sub_sub_url):
    st.write(f"Wybrany kierunek: {selected_field}")
    the_class = "syl-grid-tab-content tab-pane fade active show"
    payload = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", sub_sub_url, headers = headers, data = payload)
    bs3 = BeautifulSoup(response.content, "html.parser")
    paragraphs = bs3.find('div', {'id': 'syl-grid-period-info'}).find_all('p')

    for paragraph in paragraphs:
        st.write(paragraph.get_text(strip=True))