import requests
from bs4 import BeautifulSoup
import streamlit as st

payload = {}
domain_url = "https://sylabus.sggw.edu.pl"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

def get_field(sub_url):
    response = requests.request("GET", sub_url, headers = headers, data = payload)
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