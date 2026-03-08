import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud

#CONFIG
API_KEY = "f033654b1cbf47fa8e4bf367e5b52f21"

#COLORS
POSITIVE_COLOR = '#98D8C8'  # mint
NEGATIVE_COLOR = '#F4A698'  # coral
NEUTRAL_COLOR = '#C9B8E8'   # lavender

#FUNCTIONS
def get_headlines(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&language=en&sortBy=publishedAt&pageSize=20&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    headlines = [article['title'] for article in articles if article['title'] != '[Removed]']
    return headlines

def analyze_headlines(headlines):
    analyzer = SentimentIntensityAnalyzer()
    results = []
    for headline in headlines:
        score = analyzer.polarity_scores(headline)
        results.append({
            'Headline': headline,
            'Positive': score['pos'],
            'Negative': score['neg'],
            'Neutral': score['neu'],
            'Compound': score['compound'],
            'Sentiment': 'Positive' if score['compound'] > 0.05 else ('Negative' if score['compound'] < -0.05 else 'Neutral')
        })
    return pd.DataFrame(results)

def plot_distribution(df):
    sentiment_counts = df['Sentiment'].value_counts()
    fig, ax = plt.subplots(figsize=(7, 4))
    bar_colors = [NEGATIVE_COLOR if x == 'Negative' else POSITIVE_COLOR if x == 'Positive' else NEUTRAL_COLOR
                  for x in sentiment_counts.index]
    sentiment_counts.plot(kind='bar', color=bar_colors, edgecolor='white', ax=ax)
    ax.set_title('Sentiment Distribution', fontsize=14)
    ax.set_xlabel('Sentiment', fontsize=11)
    ax.set_ylabel('Number of Headlines', fontsize=11)
    ax.tick_params(axis='x', rotation=0)
    plt.tight_layout()
    return fig

def plot_compound(df):
    fig, ax = plt.subplots(figsize=(12, 4))
    colors = [POSITIVE_COLOR if c > 0.05 else NEGATIVE_COLOR if c < -0.05 else NEUTRAL_COLOR
              for c in df['Compound']]
    ax.bar(range(len(df)), df['Compound'], color=colors, edgecolor='white')
    ax.axhline(y=0, color='#888888', linestyle='-', linewidth=0.8)
    ax.axhline(y=0.05, color='#98D8C8', linestyle='--', linewidth=0.8, label='Positive threshold')
    ax.axhline(y=-0.05, color='#F4A698', linestyle='--', linewidth=0.8, label='Negative threshold')
    ax.set_title('Sentiment Score per Headline', fontsize=14)
    ax.set_xlabel('Headline Index', fontsize=11)
    ax.set_ylabel('Compound Score', fontsize=11)
    ax.legend()
    plt.tight_layout()
    return fig

from wordcloud import WordCloud, STOPWORDS

def plot_wordcloud(headlines):
    text = ' '.join(headlines)
    wc = WordCloud(
        width=800, height=400,
        background_color='#1a1a2e',
        colormap='cool',
        max_words=50,
        stopwords=STOPWORDS
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout()
    return fig
    
#STREAMLIT UI
st.set_page_config(page_title="Sentiment Dashboard", page_icon="📊", layout="wide")

st.title("📰 Real-Time News Sentiment Dashboard")
st.markdown("Analyze the sentiment of live news headlines on any topic.")

topic = st.text_input("Enter a topic:", placeholder="e.g. climate change, AI, elections...")

if st.button("Analyze") or topic:
    if topic:
        with st.spinner("Fetching live headlines..."):
            headlines = get_headlines(topic)

        if not headlines:
            st.error("No headlines found. Try a different topic.")
        else:
            df = analyze_headlines(headlines)

            #Metrics row
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Headlines", len(df))
            col2.metric("Positive ❤️", len(df[df['Sentiment'] == 'Positive']))
            col3.metric("Negative 🖤", len(df[df['Sentiment'] == 'Negative']))
            col4.metric("Neutral 💜", len(df[df['Sentiment'] == 'Neutral']))

            st.markdown("---")

            #Charts
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Sentiment Distribution")
                st.pyplot(plot_distribution(df))
            with col_b:
                st.subheader("Compound Score per Headline")
                st.pyplot(plot_compound(df))

            st.markdown("---")

            #Word Cloud
            st.subheader("Word Cloud")
            st.pyplot(plot_wordcloud(headlines))

            st.markdown("---")
            
            #Headlines table
            st.subheader("All Headlines")
            st.dataframe(df[['Headline', 'Sentiment', 'Compound']], use_container_width=True)
    else:
        st.warning("Please enter a topic first!")