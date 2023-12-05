import requests
from bs4 import BeautifulSoup
import streamlit as st

payload = {}
domain_url = "https://sylabus.sggw.edu.pl"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

def get_faculties(url):
    response = requests.request("GET", url, headers=headers, data=payload)
    bs = BeautifulSoup(response.content, "html.parser")
    masterElement = bs.find(class_="elements-masterElement")
    a_tags = masterElement.find_all("a")

    ### Faulties ###
    links = []
    faculties = []
    for i, item in enumerate(a_tags):
        faculties.append(item.get_text().strip())
        links.append(domain_url + item.get("href"))

    selected_faculty = st.selectbox("Wybierz wydział:", faculties)
    
    return selected_faculty, faculties, links