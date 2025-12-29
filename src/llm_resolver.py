"""

LLM Resolver Module
Uses a Large Language Model to disambiguate between geographic candidates

"""

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "ministral-3:3b"

def resolve_location(
    #original_text : str,
    #entity : str,
    candidates : list[dict]
) -> dict | None:

    """
    Use LLM to select the most likely location given a text, an entity and a list of candidate locations for this entity

    Args :

    - original_text : The original text from which we extracted the entities. 
    - entity : The entity we are trying to disambiguate
    - candidates : A dictionary of all the candidate locations for the entity

    Returns :

    The selected candidate dictionary according to the LLM or None if the resolution failed

    """

    if not candidates:
        return None

    if len(candidates) == 1:
        return candidates[0] #No ambiguity

    options_text = "\n".join(
        f"{i+1}. {c['name']} (lat: {c['lat']}, lon: {c['lon']})"
        for i, c in enumerate(candidates)
    )

    return options_text

if __name__ == "__main__":
    paris_candidates = [
        {"name": "Paris, Île-de-France, France", "lat": 48.8534951, "lon": 2.3483915},
        {"name": "Paris, Lamar County, Texas, USA", "lat": 33.6617962, "lon": -95.555513},
    ]
    options_text = resolve_location(paris_candidates)
    print(options_text)