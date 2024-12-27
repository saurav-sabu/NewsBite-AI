import streamlit as st
from src.helper import fetch_articles
from src.summary_response import get_summary_response
from src.sentiment_analysis import analyze_sentiment  # Assuming you have a sentiment analysis module
from gtts import gTTS
from deep_translator import GoogleTranslator

# Set page config
st.set_page_config(page_title="NewsBite-AI", page_icon="\U0001F4F0", layout="wide")

# App title
st.title("📰 NewsBite-AI: AI-Based News Summarizer")
st.markdown("---")

st.info("Go to the sidebar to configure your summary settings.")

# Initialize session state
if "articles" not in st.session_state:
    st.session_state.articles = []
if "selected_summary" not in st.session_state:
    st.session_state.selected_summary = ""
if "translated_summary" not in st.session_state:
    st.session_state.translated_summary = ""

# Sidebar for user inputs
with st.sidebar:
    st.header("Configure Your Summary")
    summary_length = st.selectbox("Summary Length", ["Short", "Medium", "Long"], index=1)
    search_topic = st.text_input("Topic-Based Search", placeholder="Enter a topic")
    language = st.selectbox("Language for Summary", ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Kannada", "Malayalam", "Punjabi", "Gujarati", "Odia", "Urdu", "Marathi"])
    tts_enabled = st.checkbox("Enable Audio Summary")

# Main content
col1, col2 = st.columns([2, 1])

# User choice for input method
with col1:
    st.subheader("Choose Input Method")
    input_method = st.radio("Select how you want to summarize:", ["Fetch by Topic", "Paste Article"])

    news_article = ""

    if input_method == "Fetch by Topic":
        if not search_topic.strip():
            st.warning("Please enter a topic in the sidebar to fetch articles.")
        else:
            if st.button("Fetch Articles"):
                with st.spinner("Fetching articles..."):
                    articles = fetch_articles(search_topic)
                if articles:
                    st.success("Articles fetched successfully!")
                    # Store fetched articles in session state
                    st.session_state.articles = articles

        # Check if articles are stored
        if st.session_state.articles:
            # Display list of articles with selection option
            article_titles = [article["title"] for article in st.session_state.articles]
            selected_article_title = st.selectbox("Select an article to summarize:", article_titles)

            # Get selected article
            selected_article = next(
                article for article in st.session_state.articles if article["title"] == selected_article_title
            )

            # Display article details
            st.markdown(f"### {selected_article['title']}")
            st.write(f"**Published on**: {selected_article['date']}")
            st.write(f"**Source**: {selected_article['source']}")
            st.write(f"**URL**: [{selected_article['url']}]({selected_article['url']})")
            if selected_article['image']:
                st.image(selected_article['image'], caption="Image", width=300)

            # Generate summary if it doesn't already exist in session state
            if st.session_state.selected_summary != selected_article_title:
                with st.spinner("Generating summary..."):
                    response = get_summary_response(selected_article["text"], summary_length)
                st.session_state.selected_summary = response

            # Display the English summary
            st.markdown("### Your Summary (English)")
            st.write(st.session_state.selected_summary["Summary"])

            # Translate and display the summary in the selected language
            if language != "English":
                target_language_code = {
                    "Hindi": "hi",
                    "Tamil": "ta",
                    "Telugu": "te",
                    "Bengali": "bn",
                    "Kannada": "kn",
                    "Malayalam": "ml",
                    "Punjabi": "pa",
                    "Gujarati": "gu",
                    "Odia": "or",
                    "Urdu": "ur",
                    "Marathi": "mr"
                }.get(language, "en")

                with st.spinner("Translating summary..."):
                    translated = GoogleTranslator(source='en', target=target_language_code).translate(st.session_state.selected_summary["Summary"])
                    st.session_state.translated_summary = translated

                st.markdown(f"### Your Summary ({language})")
                st.write(st.session_state.translated_summary)

            # Sentiment Analysis for the Summary
            st.markdown("### Sentiment Analysis")
            st.write(f"**Tone:** {st.session_state.selected_summary['Tone']}")
            st.metric(label="Sentiment", value=f"{st.session_state.selected_summary['Sentiment_Score']}%")

    elif input_method == "Paste Article":
        news_article = st.text_area("Input", placeholder="Paste the news article you want to summarize here...", height=200)

        if st.button("Summarize"):
            if not news_article.strip():
                st.error("Please provide a news article to summarize.")
            else:
                # Generate summary for pasted article
                response = get_summary_response(news_article, summary_length)
                st.success("Summary Generated Successfully!")
                st.markdown("### Your Summary (English)")
                st.write(response["Summary"])

                # Translate and display the summary in the selected language
                if language != "English":
                    target_language_code = {
                        "Hindi": "hi",
                        "Tamil": "ta",
                        "Telugu": "te",
                        "Bengali": "bn",
                        "Kannada": "kn",
                        "Malayalam": "ml",
                        "Punjabi": "pa",
                        "Gujarati": "gu",
                        "Odia": "or",
                        "Urdu": "ur",
                        "Marathi": "mr"
                    }.get(language, "en")

                    with st.spinner("Translating summary..."):
                        translated = GoogleTranslator(source='en', target=target_language_code).translate(response["Summary"])
                        st.session_state.translated_summary = translated

                    st.markdown(f"### Your Summary ({language})")
                    st.write(st.session_state.translated_summary)

                # Sentiment Analysis for the Pasted Summary
                sentiment_result = analyze_sentiment(news_article)
                st.markdown("### Sentiment Analysis")
                st.write(f"**Tone:** {sentiment_result['tone']}")
                st.metric(label="Confidence", value=f"{sentiment_result['confidence']}%")

# Additional Features
with col2:
    # Text-to-Speech Section
    st.markdown("### Listen To Audio Summary")
    tts_language_codes = {
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "Bengali": "bn",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Punjabi": "pa",
        "Gujarati": "gu",
        "Odia": "or",
        "Urdu": "ur",
        "Marathi": "mr"
    }

    target_language_code = tts_language_codes.get(language, "en")

    if (tts_enabled and st.session_state.selected_summary) or (tts_enabled and st.session_state.translated_summary):
        translated_for_tts = st.session_state.translated_summary if language != "English" else st.session_state.selected_summary["Summary"]
        tts = gTTS(translated_for_tts, lang=target_language_code)
        tts.save('output.mp3')
        st.audio(data="output.mp3", format="audio/mp3", start_time=0)
    elif tts_enabled:
        st.info("TTS is enabled, but no summary is available to generate audio.")

# Footer
st.markdown("---")
st.markdown("**© 2024 NewsBite-AI | All rights reserved.**")

