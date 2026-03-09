## Real-Time News Sentiment Dashboard

A live web app that fetches real-time news headlines on any topic and analyzes their sentiment using NLP.

Live Demo: https://code-by-ace-sentiment-analysis-dashboard.streamlit.app

## Summary

Type any topic such as AI, climate change, or elections and instantly see how positive, negative, or neutral the news coverage is, a sentiment score for each headline, a word cloud of the most common terms, and a full table of all analyzed headlines.


## Tech Stack

- Python — core language
- Streamlit — web app framework
- VADER (vaderSentiment) — sentiment analysis model
- GNews API — fetches live news headlines
- Matplotlib — charts and visualizations
- WordCloud — generates word cloud from headlines
- Pandas — data handling and structuring

## Future Improvements

- Upgrade from VADER to BERT for more accurate sentiment analysis
- Add topic comparison
- Add time-series sentiment tracking over days and weeks
- Export results as CSV


## Run Locally

Clone the repo, install dependencies with pip install -r requirements.txt, then run streamlit run app.py.

Add your GNews API key to .streamlit/secrets.toml:
GNEWS_API_KEY = "your_key_here"
