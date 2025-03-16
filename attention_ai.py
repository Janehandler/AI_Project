import socket
import random
import threading
import time

class AttentionAI:
    def __init__(self, host='localhost', port=7086):  # Fixed Port
        self.host = host
        self.port = port
        self.running = True

        # ✅ Updated Neural Bots Port Mapping
        self.neural_bots = {
            "brain_ai": 7070,
            "memory_ai": 7073,
            "logic_ai": 7078,
            "learning_ai": 7080,
            "self_analysis_ai": 7077,
            "news_ai": 7074,
            "trading_ai": 7081,
            "psychology_ai": 7076,
            "linguistic_ai": 7085,  # Fixed
            "security_ai": 7082,
            "network_ai": 7087  # Fixed
        }

    # ========================== ATTENTION & MARKET DATA MANAGEMENT ==========================
    def generate_market_data(self, message):
        """ Simulates market data retrieval based on user request """
        if "price" in message.lower():
            stock_price = round(random.uniform(50, 500), 2)
            return f"📊 Current market price: ${stock_price}"

        elif "trend" in message.lower():
            trend_direction = random.choice(['upward', 'downward', 'stable'])
            return f"📉 Market trend: {trend_direction.capitalize()}"

        elif "volume" in message.lower():
            volume = random.randint(100000, 5000000)
            return f"📊 Trading volume: {volume} shares"

        else:
            return "⚠️ Invalid request. Try asking about price, trend, or volume."

    # ========================== NETWORK COMMUNICATION ==========================
    def send_message_to_network(self, message):
        """ Sends a message to the AINetwork bot """
        return self.send_message("network_ai", message)

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

    # ========================== AI SERVER SYSTEM ==========================
    def start(self):
        """ Starts the Market Data AI server with enhanced capabilities """
        print("\n🧠 Attention AI is Active and Managing Focus...")

        server_thread = threading.Thread(target=self._server_loop, daemon=True)
        server_thread.start()

    def _server_loop(self):
        """ Handles incoming connections and processes market data requests """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while self.running:
                try:
                    conn, addr = s.accept()
                    with conn:
                        message = conn.recv(1024).decode().strip()
                        if message:
                            response = self.generate_market_data(message)
                            conn.sendall(response.encode())
                except Exception as e:
                    print(f"❌ Error in server loop: {e}")
                    time.sleep(1)

    def stop(self):
        """ Gracefully stops the Market Data AI """
        self.running = False
        print("🛑 Attention AI has been stopped.")

# ========================== ATTENTION AI INITIALIZATION ==========================
if __name__ == "__main__":
    attention_ai = AttentionAI()
    attention_ai.start()

# AI Improvements:
❌ OpenAI API Error: 

You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742


# AI Improvements:
OpenAI API Error: 

You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742
