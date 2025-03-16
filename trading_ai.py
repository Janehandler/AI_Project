import socket
import json
import requests
import threading
import time
import random
from datetime import datetime

class TradingAI:
    def __init__(self, host='localhost', port=7081):  # Fixed Port
        self.host = host
        self.port = port
        self.stock_data = {}
        self.api_key = "YOUR_FINANCIAL_API_KEY"
        self.running = True
        self.lock = threading.Lock()

        # ✅ Updated Neural Bots Port Mapping
        self.neural_bots = {
            "brain_ai": 7070,
            "memory_ai": 7073,
            "logic_ai": 7078,
            "learning_ai": 7080,
            "self_analysis_ai": 7077,
            "news_ai": 7074,
            "psychology_ai": 7076,
            "linguistic_ai": 7085,  # Fixed
            "security_ai": 7082,
            "attention_ai": 7086,  # Fixed
            "network_ai": 7087  # Fixed
        }

    # ========================== STOCK DATA FETCHING ==========================
    def fetch_stock_data(self, symbol):
        """ Fetches live stock data from financial API """
        url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={self.api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            if data:
                stock_info = data[0]
                stock_entry = {
                    "symbol": stock_info["symbol"],
                    "price": stock_info["price"],
                    "change": stock_info["change"],
                    "percent_change": stock_info["changesPercentage"],
                    "volume": stock_info["volume"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                with self.lock:
                    self.stock_data[symbol] = stock_entry
                return f"📈 {symbol} | ${stock_info['price']} | {stock_info['percent_change']}% change"
            else:
                return "⚠️ No stock data found."
        except Exception as e:
            return f"❌ Stock API Error: {e}"

    def recall_stock_data(self, symbol):
        """ Retrieves latest stored stock data """
        with self.lock:
            if symbol in self.stock_data:
                return json.dumps(self.stock_data[symbol], indent=4)
            return "🛑 No data available for this stock."

    # ========================== STOCK MARKET ANALYSIS ==========================
    def generate_market_report(self, symbol):
        """ Generates a smart trading alert based on multiple AI signals """
        stock_info = self.recall_stock_data(symbol)
        sentiment = self.send_message("news_ai", f"ANALYZE_SENTIMENT:{symbol}")
        chart_patterns = self.send_message("logic_ai", f"ANALYZE_TRENDS:{symbol}")

        return f"📊 Market Report for {symbol}\n{stock_info}\n{sentiment}\n{chart_patterns}"

    # ========================== NETWORK COMMUNICATION ==========================
    def send_message(self, target_bot, message):
        """ Sends a message to another bot within the network """
        if target_bot not in self.neural_bots:
            return f"⚠️ Bot {target_bot} not recognized."

        target_port = self.neural_bots[target_bot]
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", target_port))
                s.sendall(message.encode())
                response = s.recv(1024).decode()
                return response
        except Exception as e:
            return f"❌ Error communicating with {target_bot}: {e}"

    # ========================== TRADING AI SERVER ==========================
    def start(self):
        """ Starts the Trading AI server """
        server_thread = threading.Thread(target=self._server_loop, daemon=True)
        server_thread.start()
        print("\n💹 Trading AI is Active and LISTENING...")

    def _server_loop(self):
        """ Handles incoming stock data requests via sockets """
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
        """ Processes stock market queries """
        try:
            with conn:
                message = conn.recv(1024).decode().strip()
                if message.startswith("FETCH"):
                    response = self.fetch_stock_data(message.replace("FETCH:", "").strip())
                elif message.startswith("RECALL"):
                    response = self.recall_stock_data(message.replace("RECALL:", "").strip())
                elif message.startswith("ANALYZE"):
                    response = self.generate_market_report(message.replace("ANALYZE:", "").strip())
                else:
                    response = "⚠️ Invalid command. Use FETCH, RECALL, ANALYZE."
                conn.sendall(response.encode())
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")

    def stop(self):
        """ Stops the AI """
        self.running = False
        print("🛑 Trading AI has been stopped.")

# ========================== TRADING AI INITIALIZATION ==========================
if __name__ == "__main__":
    trading_ai = TradingAI()
    trading_ai.start()