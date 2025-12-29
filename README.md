# 🌍 MiniGeoParse

A tiny geoparsing pipeline that extracts locations from text and resolves them to coordinates using LLMs.

## Quick Start

```bash
uv sync
uv run python src/pipeline.py
```

## Example

**Input:**
```
I traveled from Paris to Lyon, then visited the Alps near Geneva.
```

**Output:**
```
Paris   → Paris, Île-de-France, France           📍 (48.86, 2.32)
Lyon    → Lyon, Auvergne-Rhône-Alpes, France     📍 (45.76, 4.83)
Alps    → Auvergne-Rhône-Alpes, France           📍 (45.30, 4.66)
Geneva  → Genève, Switzerland                    📍 (46.20, 6.15)
```

## Architecture

```
Text → SpaCy NER → OpenStreetMap API → LLM Disambiguation → Coordinates
```

## Tech Stack

- **NER**: SpaCy (en_core_web_lg)
- **Gazetteer**: OpenStreetMap Nominatim
- **LLM**: Ollama (local Mistral ministral-3:3B)
- **Package Manager**: uv
