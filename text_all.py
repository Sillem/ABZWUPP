### funkcja do otwierania dwóch plików json i robienia z nich jednego stringa


import json

# read JSON from file
with open(
    "Selected_fields_of_study/gospodarka przestrzenna/efekty_uczenia.json",
    encoding="utf-8",
) as f:
    data = json.load(f)


combined_string = ""
for key in data.keys():
    combined_string = (
        combined_string + key.replace("\xa0", " ") + data[key].replace("\xa0", " ")
    )


with open(
    "Selected_fields_of_study/gospodarka przestrzenna/tresci_programowe.json",
    encoding="utf-8",
) as f:
    data = json.load(f)

for key in data.keys():
    combined_string = (
        combined_string + key.replace("\xa0", " ") + data[key].replace("\xa0", " ")
    )

print(combined_string)
