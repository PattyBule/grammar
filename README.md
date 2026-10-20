# Grammar Naturalizer

A Python project for checking English grammar and rewriting typed sentences into clearer, more natural, and more polite English.

## Project goal

This project helps users turn rough or direct typed English into more natural English, especially in communication scenarios where tone matters. It is designed for:

- people who type in English and need grammar support
- deaf or hard-of-hearing users who communicate primarily through text
- users who want to write more politely or naturally without changing their meaning

## Features

- Grammar checking for common English errors
- Tone analysis for direct, neutral, polite, or friendly text
- Natural sentence rewriting
- Multiple rewrite styles: neutral, natural, polite, formal, friendly
- Lightweight API built with FastAPI
- Quick MVP for local testing and extension

## Tech stack

- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn

## Project structure

```text
app/
  __init__.py
  __main__.py
  config.py
  main.py
  api/
    routes.py
    schemas.py
  services/
    grammar_service.py
    tone_service.py
    rewrite_service.py
  __main__.py

requirements.txt
README.md
```

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
uvicorn app.main:app --reload
```

### 4. Test endpoints

```bash
curl http://localhost:8000/health
```

### 5. Rewrite a sentence

```bash
curl -X POST http://localhost:8000/api/v1/rewrite \
  -H "Content-Type: application/json" \
  -d '{"text":"I need this now.","style":"polite","context":"chat"}'
```

## Example output

Input:

```text
I need this now.
```

Possible output:

```json
{
  "original_text": "I need this now.",
  "corrected_text": "I need this as soon as possible.",
  "tone_analysis": {
    "tone": "direct",
    "intensity": 0.9,
    "confidence": 0.9,
    "reasons": ["The sentence sounds urgent or demanding."]
  },
  "rewrite_options": [
    {
      "style": "neutral",
      "text": "I need this as soon as possible.",
      "explanation": "Keeps the message clear and direct while remaining natural."
    },
    {
      "style": "polite",
      "text": "Could you please take care of this for me as soon as possible?",
      "explanation": "This version softens the request and makes it more respectful."
    }
  ],
  "summary": "The sentence was checked for grammar and rewritten in a more natural and socially polite style."
}
```

## Future improvements

- Better grammar detection with LanguageTool or spaCy
- More advanced style and tone classification
- User profiles and saved preferences
- Paragraph-level rewriting
- Email and chat templates
- History and feedback tracking
- Frontend UI for easier use

## License

This project is currently set up as an MVP and is intended for learning and product prototyping.
