from dotenv import load_dotenv
from duckduckgo_search import DDGS
from phi.tools.newspaper4k import Newspaper4k
from gtts import gTTS

def fetch_articles(topic: str):
    # Search for articles using DuckDuckGo
    news_result = []
    ddgs = DDGS()

    newspaper_tools = Newspaper4k()

    results = ddgs.news(topic, max_results=10)

    for result in results:
        if "url" in result:
            article_data = newspaper_tools.get_article_data(result["url"])

            if article_data and "text" in article_data:
                result["text"] = article_data["text"]
                news_result.append(result)

    return news_result


    
    