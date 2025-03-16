import socket
import json
import os
import threading
import requests
from textblob import TextBlob
from datetime import datetime

class NewsAI:
    def __init__(self, host='localhost', port=7074):  # Fixed Port
        self.host = host
        self.port = port
        self.news_file = "/workspace/ai_project/news_data.json"
        self.load_news()
        self.lock = threading.Lock()
        self.running = True

        # ✅ Updated Neural Bots Port Mapping
        self.neural_bots = {
            "brain_ai": 7070,
            "memory_ai": 7073,
            "logic_ai": 7078,
            "learning_ai": 7080,
            "self_analysis_ai": 7077,
            "trading_ai": 7081,
            "psychology_ai": 7076,
            "linguistic_ai": 7085,  # Fixed
            "security_ai": 7082,
            "attention_ai": 7086,  # Fixed
            "network_ai": 7087  # Fixed
        }

    # ========================== NEWS SYSTEM ==========================
    def load_news(self):
        """ Loads stored news history """
        if os.path.exists(self.news_file):
            with open(self.news_file, "r") as file:
                self.news_history = json.load(file)
        else:
            self.news_history = []

    def save_news(self, title, content, source, sentiment, confidence, bias="Unknown"):
        """ Stores news articles with metadata """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        news_entry = {
            "timestamp": timestamp,
            "title": title,
            "content": content,
            "source": source,
            "sentiment": sentiment,
            "confidence": confidence,
            "bias": bias
        }
        with self.lock:
            self.news_history.append(news_entry)
            self.news_history = sorted(self.news_history, key=lambda x: x["confidence"], reverse=True)[:50]  # Keep top 50
            with open(self.news_file, "w") as file:
                json.dump(self.news_history, file, indent=4)

        return f"📰 News stored: {title} (Sentiment: {sentiment}, Confidence: {confidence}%, Bias: {bias})"

    def recall_news(self, query=None, num_entries=5):
        """ Retrieves past news articles based on keywords or latest trends """
        with self.lock:
            if query:
                results = [n for n in self.news_history if query.lower() in n["title"].lower()]
                return json.dumps(results[:num_entries], indent=4) if results else "🛑 No matching news articles found."
            else:
                return json.dumps(self.news_history[:num_entries], indent=4) if self.news_history else "🛑 No news available."

    # ========================== NEWS FETCHING & ANALYSIS ==========================
    def fetch_latest_news(self, keyword="technology"):
        """ Fetches real-time news from an API and ranks it """
        API_URL = f"https://newsapi.org/v2/everything?q={keyword}&apiKey=YOUR_NEWS_API_KEY"
        try:
            response = requests.get(API_URL, timeout=10)
            news_data = response.json()

            if "articles" in news_data:
                top_articles = news_data["articles"][:5]
                summaries = []
                for article in top_articles:
                    title = article["title"]
                    content = article["description"] or "No content available."
                    source = article["source"]["name"]
                    sentiment, confidence = self.analyze_sentiment(content)
                    bias = self.detect_bias(source)
                    self.save_news(title, content, source, sentiment, confidence, bias)
                    summaries.append(f"{title} (Sentiment: {sentiment}, Confidence: {confidence}%, Bias: {bias})")
                return "📰 Latest News:\n" + "\n".join(summaries)
            else:
                return "⚠️ Failed to fetch news."
        except requests.exceptions.RequestException as e:
            return f"❌ News Fetching Error: {e}"

    def analyze_sentiment(self, text):
        """ Analyzes sentiment & assigns a confidence score """
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        confidence = round(abs(polarity) * 100, 2)
        if polarity > 0:
            return "Positive", confidence
        elif polarity < 0:
            return "Negative", confidence
        else:
            return "Neutral", confidence

    # ========================== NEWS AI SERVER ==========================
    def start(self):
        """ Starts the News AI for real-time news retrieval """
        server_thread = threading.Thread(target=self._server_loop, daemon=True)
        server_thread.start()
        print("\n📰 News AI is Active and LISTENING...")

    def _server_loop(self):
        """ Handles incoming news requests via sockets """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while self.running:
                try:
                    conn, addr = s.accept()
                    thread = threading.Thread(target=self.handle_connection, args=(conn,))
                    thread.start()
                except Exception as e:
                    print(f"❌ Server Error: {e}")

    def handle_connection(self, conn):
        """ Processes news and trend queries """
        try:
            with conn:
                message = conn.recv(1024).decode().strip()
                if message.startswith("FETCH"):
                    response = self.fetch_latest_news(message.replace("FETCH:", "").strip())
                elif message.startswith("RECALL"):
                    response = self.recall_news(message.replace("RECALL:", "").strip())
                else:
                    response = "⚠️ Invalid command. Use FETCH, RECALL."
                conn.sendall(response.encode())
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")

    def stop(self):
        """ Stops the AI """
        self.running = False
        print("🛑 News AI has been stopped.")

# ========================== NEWS AI INITIALIZATION ==========================
if __name__ == "__main__":
    news_ai = NewsAI()
    news_ai.start()

# AI Improvements:
❌ OpenAI API Error: 

You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742
