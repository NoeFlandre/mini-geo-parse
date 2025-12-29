"""

NER Extractor Module

Extracts geographic named entities from text using SpaCy

"""

import spacy

nlp = spacy.load("en_core_web_lg") # here we are loading the model once as it is an expensive operation hence why we load it at the module level. The model chosen is a small English language model trained on web text. It includes a pre-trained NER component that can already recognize locations, people, organizations and so o

GEO_LABELS = {"LOC", "GPE"} # here we are specifying the labels we consider as geographic. These includes Geo-Political Entity (GPE) (countries, cities, states) and Non-GPE locations (LOC) (moutains, rivers, regions)

def extract_locations(text : str) -> list[str] :

    """

    Extract geographic entities from a given text

    Args : A given string of text to be parsed

    Output : A list of strings representing geographic entites found in the given text

    """

    doc = nlp(text)
    locations = []

    for ent in doc.ents :
        if ent.label_ in GEO_LABELS :
            locations.append(ent.text)

    return locations

if __name__ == "__main__":
     sample = "The wildfire spread near Montpellier, affecting the Hérault department."
     print(f"Input : {sample}")

     # Debug : Show ALL entities the model finds
     doc = nlp(sample)
     print("\n All entities found by the model :")
     for ent in doc.ents:
        print(f"Found entity : {ent.text} with the label {ent.label_}")

     print(f"Filtered locations found : {extract_locations(sample)}")