import spacy
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    return ",".join([t.text for t in doc if t.pos_ in ["NOUN","PROPN"]])
