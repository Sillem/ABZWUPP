import requests
from bs4 import BeautifulSoup
import streamlit as st

the_class = "syl-get-document syl-pointer"
payload = {}
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

def get_subject(sub_sub_url):
    response = requests.request("GET", sub_sub_url, headers=headers, data=payload)
    bs3 = BeautifulSoup(response.content, "html.parser")

    subject_divs = bs3.find_all(class_ = the_class)
    subject_names = []
    subject_ids = []

    for i, item in enumerate(subject_divs):
        subject_names.append(item.string.strip())
        subject_ids.append(item.get("id"))
        # print(i, ".", item.string.strip())
        # print(item.get("id"))

    selected_subject = st.selectbox("Wybierz przedmiot: ", subject_names)
    return selected_subject, subject_names, subject_ids