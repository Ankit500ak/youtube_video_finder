# Backend for YouTube Video Finder

## Setup
1. Copy `.env.example` to `.env` and fill in your API keys.
2. Install dependencies:
   ```
pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```
python app.py
   ```

## Endpoints
- `POST /api/search` — expects `{ "query": "your search" }`, returns best video and list.
