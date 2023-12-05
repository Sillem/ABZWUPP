
### METODA 1 ###
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Przykładowe teksty
text1 = "To jest pierwszy tekst do porównania."
text2 = "To jest drugi tekst do porównania."

# Tworzenie macierzy wektorów cech
vectorizer = CountVectorizer().fit_transform([text1, text2])

# Obliczanie podobieństwa kosinusowego
similarity = cosine_similarity(vectorizer)
print(similarity)



### METDOA 2 ###
import Levenshtein

# Przykładowe teksty
text1 = "To jest pierwszy tekst do porównania."
text2 = "To jest drugi tekst do porównania."

# Obliczanie odległości Levenshteina
distance = Levenshtein.distance(text1, text2)
similarity = 1 - distance / max(len(text1), len(text2))
print(similarity)



### METODA 3 ###
from difflib import SequenceMatcher

# Przykładowe teksty
text1 = "To jest pierwszy tekst do porównania."
text2 = "To jest drugi tekst do porównania."

# Obliczanie podobieństwa za pomocą SequenceMatcher
similarity_ratio = SequenceMatcher(None, text1, text2).ratio()
print(similarity_ratio)



### METODA 4 ###
from nltk.metrics import edit_distance

# Przykładowe teksty
text1 = "To jest pierwszy tekst do porównania."
text2 = "To jest drugi tekst do porównania."

# Obliczanie odległości edycyjnej
distance = edit_distance(text1.lower(), text2.lower())
similarity = 1 - (distance / max(len(text1), len(text2)))
print(similarity)
