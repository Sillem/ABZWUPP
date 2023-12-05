from bs4 import BeautifulSoup
from requests import get
import requests
import time, datetime
import re
import json
import os


from utils import remove_char, create_folder


url = "https://sylabus.sggw.edu.pl/pl/1/19/3/4/40"
domain_url = "https://sylabus.sggw.edu.pl"

payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, headers=headers, data=payload)

bs = BeautifulSoup(response.content, "html.parser")
masterElement = bs.find(class_="elements-masterElement")
a_tags = masterElement.find_all("a")

links = []
for i, item in enumerate(a_tags):
    print(i, ". ", item.get_text().strip())
    print(domain_url + item.get("href"))
    links.append(domain_url + item.get("href"))

time.sleep(0.1)
chosen_one = int(input("Which one: "))

### go to the chosen link

sub_url = links[chosen_one]

print("Chosen ", sub_url)
response = requests.request("GET", sub_url, headers=headers, data=payload)

bs2 = BeautifulSoup(response.content, "html.parser")
masterElement = bs2.find(class_="elements-major")
a_tags2 = masterElement.find_all("a")
sublinks = []
for i, item in enumerate(a_tags2):
    print(i, ". ", item.get_text().strip())
    print(domain_url + item.get("href"))
    sublinks.append(domain_url + item.get("href"))

time.sleep(0.1)
chosen_one2 = int(input("Which one: "))
sub_sub_url = sublinks[chosen_one2]
print("Chosen ", sub_sub_url)

the_class = "syl-get-document syl-pointer"

payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

response = requests.request("GET", sub_sub_url, headers=headers, data=payload)

bs3 = BeautifulSoup(response.content, "html.parser")

# print(bs3.prettify())

subject_divs = bs3.find_all(class_=the_class)

# item22 = bs3.find(class_=the_class)
# item22.
# print(item22)
subject_names = []
subject_ids = []

print(len(subject_divs))
for i, item in enumerate(subject_divs):
    subject_names.append(item.string.strip())
    subject_ids.append(item.get("id"))
    print(i, ".", item.string.strip())
    print(item.get("id"))

time.sleep(0.1)
subject_chosen = int(input("Which one? Enter number:"))
chosen_id = subject_ids[subject_chosen]
course_name = subject_names[subject_chosen]
print("Chosen ", course_name)


doc_url = "https://sylabus.sggw.edu.pl/pl/document/" + chosen_id + ".jsonHtml"

print("link:", doc_url)

payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

response = requests.request("GET", doc_url, headers=headers, data=payload)

html = response.json()["html"]
# print(html)

# print(json.load(response.json))

bs4 = BeautifulSoup(html, "html.parser")
# print(bs4.prettify())
course_content = ""
learning_effects = ""

h1s = bs4.find_all("h1")
for h1 in h1s:
    if h1.get_text().strip() == "Efekty uczenia się dla przedmiotu":
        print("-----EFEKTY UCZENIA SIE-----")
        print(h1)
        efekty_tag = h1.find_next()

        for i, item in enumerate(efekty_tag.find_all("td", class_="code")):
            if "row_code" not in item["class"] and "row_header" not in item["class"]:
                if item.find("span") is None:
                    print(i, item.find_next().get_text().strip())
                    learning_effects += item.find_next().get_text().strip() + " "

    if h1.get_text().strip() == "Treści programowe":
        print("-----TREŚCI PROGRAMOWE-----")
        # print(h1)
        tresc_tag = h1.find_next()
        # print(tresc_tag)

        for i, item in enumerate(tresc_tag.find_all("td", class_="code")):
            if "row_code" not in item["class"] and "row_header" not in item["class"]:
                # print(i, item)
                the_text = item.find_next().get_text().strip()
                print(the_text)
                course_content += the_text + " "


codes_and_descriptions1 = []
codes_and_descriptions2 = []

print("-----KODY-----")
for item2 in bs4.find_all("span", class_="popup"):
    if item2.get("data-bs-original-title") is not None:
        code = remove_char(item2.get_text().strip(), ",")
        code_description = item2.get("data-bs-original-title")
        codes_and_descriptions1.append((code, code_description))
        print(code)
        print(code_description)
    if item2.get("title") is not None:
        code = remove_char(item2.get_text().strip(), ",")
        code_description = item2.get("title")
        codes_and_descriptions2.append((code, code_description))
        print(code)
        print(code_description)
    else:
        print("No popup title found")


create_folder(chosen_id)
# Create a path for the subfolder within the current directory
subfolder_path = os.path.join(os.getcwd(), chosen_id)
###ZAPISYWANIE NAZWY
with open(
    os.path.join(subfolder_path, course_name + ".txt"), "w", encoding="utf-8"
) as txt:
    txt.write("")


###ZAPISYWANIE EFEKTÓW UCZENIA SIE
with open(
    os.path.join(subfolder_path, "efekty_uczenia.json"), "w", encoding="utf-8"
) as json_file:
    json.dump(learning_effects, json_file, ensure_ascii=False)

###ZAPISYWANIE TRESCI PROGRAMOWYCH
with open(
    os.path.join(subfolder_path, "tresci_programowe.json"), "w", encoding="utf-8"
) as json_file:
    json.dump(course_content, json_file, ensure_ascii=False)

### ZAPISYWANIE KODÓW
# json_serializable_data = [(str(item[0]), item[1]) for item in codes_and_descriptions1]
json_serializable_data2 = [(str(item[0]), item[1]) for item in codes_and_descriptions2]
# Save the JSON data to a file
# with open(os.path.join(subfolder_path, "kody1.json"), "w", encoding='utf-8') as json_file:
#     json.dump(
#         codes_and_descriptions1,
#         json_file,
#         ensure_ascii=False,
#     )

with open(
    os.path.join(subfolder_path, "kody2.json"), "w", encoding="utf-8"
) as json_file:
    json.dump(codes_and_descriptions2[1:], json_file, ensure_ascii=False)


# cele kształcenia
def get_learning_objectives():
    pass


# efekty uczenia się
def get_learning_effects():
    pass


# treści programowe
def get_course_content():
    pass
