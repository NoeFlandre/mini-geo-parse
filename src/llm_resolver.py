"""

LLM Resolver Module
Uses a Large Language Model to disambiguate between geographic candidates

"""

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "ministral-3:3b"

def resolve_location(
    original_text : str,
    entity : str,
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

    prompt = f"""Given the following text :
    "{original_text}"

    The entity "{entity}" could refer to one of these locations :
    "{options_text}"

    Which location is most likely being referenced in the text?
    Reply with ONLY the number (1, 2, 3, etc) corresponding to the correct option.

    """

    payload = {
        "model" : MODEL,
        "prompt" : prompt,
        "stream" : False,
    }

    try :
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        answer = result = result.get("response", "").strip() #we retrieve the content for the "response" key and make sure the text is nice and clean
        for char in answer:
            if char.isdigit():
                choice = int(char)
                if 1 <= choice <= len(candidates):
                    print(f"LLM answer : {answer}")
                    print(f"LLM candidate selection : {candidates[choice-1]}")
                    return candidates[choice-1]

        # Fallback: return first candidate
        print(f"Warning : could not parse the LLM response : {answer}. Returning the default first candidate.")
        return candidates[0]

    except Exception as e:
        print(f"Error calling LLM: {e}. Returning back the default first candidate if there is any.")
        return candidates[0] if candidates else None


if __name__ == "__main__":
    paris_candidates = [
        {"name": "Paris, Île-de-France, France", "lat": 48.8534951, "lon": 2.3483915},
        {"name": "Paris, Lamar County, Texas, USA", "lat": 33.6617962, "lon": -95.555513},
    ]

    paris_original_text = "I went to Paris to see the Eiffel Tower."
    entity = "Paris"
    output = resolve_location(paris_original_text, entity, paris_candidates)
    print(output)