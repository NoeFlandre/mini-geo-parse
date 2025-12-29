"""
Pipeline Module

Orchestrates the full geoparsing flow : NER -> Gazetteer -> LLM Resolution

"""

from ner_extractor import extract_locations
from gazetteer import lookup_location
from llm_resolver import resolve_location

def geoparse(text : str) -> list[dict] :
    """

    Full geoparsing pipeline : extract locations, lookup for candidates and resolve ambiguity.

    Args:

        text : The input text to geoparse

    Output:

        List of resolved locations with coordinates

    """

    results = []

    # Step 1 : Extract location entities from the text 

    entities = extract_locations(text)
    print(f"Found {len(entities)} entities in the text. Location entities : {entities}")

    # Step 2 : For each entity, lookup candidates and resolve

    for entity in entities :
        print(f"Processing {entity}")

        candidates = lookup_location(entity, limit=5)
        print(f"Found {len(candidates)} candidates")

        if not candidates:
            print(f"Found no candidates, skipping.")
            continue

        #resolve ambiguity with LLM
        resolved = resolve_location(text, entity, candidates)

        if resolved:
            results.append({
                "mention" : entity,
                "resolved_name" : resolved["name"],
                "coordinates" : [resolved["lat"], resolved["lon"]],
            })
            print(f"Resolved to {resolved["name"]}")

    return results

if __name__ == "__main__":
    test_text = "I traveled from Paris to Lyon, then visited the Alps near Geneva."

    print(f"\n Input : {test_text} \n")
    results = geoparse(test_text)
    print("Results :")

    for r in results :
        print(r)