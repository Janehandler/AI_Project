import socket
import json
import os
import threading
from datetime import datetime

class PsychologyAI:
    def __init__(self, host='localhost', port=7076):
        self.host = host
        self.port = port
        self.memory_file = "psychology_memory.json"
        self.load_memory()
        self.running = True

        # ✅ Neural Bots for Communication
        self.neural_bots = {
            "brain_ai": 7070,
            "memory_ai": 7073,
            "logic_ai": 7078,
            "learning_ai": 7080,
            "self_analysis_ai": 7077,
            "news_ai": 7074,
            "trading_ai": 7081,
            "security_ai": 7082,
            "network_ai": 7087
        }

    # ========================== MEMORY SYSTEM ==========================
    def load_memory(self):
        """ Loads past psychological analysis results """
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as file:
                self.memory = json.load(file)
        else:
            self.memory = []

    def save_memory(self, topic, insights):
        """ Stores psychological analysis data persistently """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"timestamp": timestamp, "topic": topic, "insights": insights}
        self.memory.append(entry)
        with open(self.memory_file, "w") as file:
            json.dump(self.memory, file, indent=4)
        return f"🧠 Psychological Analysis Stored: {topic}"

    def recall_analysis(self, topic=None, num_entries=5):
        """ Retrieves past psychology-related insights """
        if topic:
            results = [m for m in self.memory if topic.lower() in m["topic"].lower()]
            return json.dumps(results[:num_entries], indent=4) if results else "🛑 No matching psychological data found."
        else:
            return json.dumps(self.memory[-num_entries:], indent=4) if self.memory else "🛑 No stored psychological analysis."

    # ========================== PSYCHOLOGY AI SERVER ==========================
    def start(self):
        """ Starts the Psychology AI for real-time analysis """
        server_thread = threading.Thread(target=self._server_loop, daemon=True)
        server_thread.start()
        print("\n🧠 Psychology AI is Active and LISTENING...")

    def _server_loop(self):
        """ Handles incoming psychology-related analysis requests """
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
        """ Processes psychology-related analysis requests """
        try:
            with conn:
                message = conn.recv(1024).decode().strip()
                if message.startswith("THINKER"):
                    response = "Analyzing with different psychological perspectives..."
                elif message.startswith("RECALL"):
                    response = self.recall_analysis()
                else:
                    response = "⚠️ Invalid command."
                conn.sendall(response.encode())
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")

    def stop(self):
        """ Gracefully stops the Psychology AI """
        self.running = False
        print("🛑 Psychology AI has been stopped.")

# ========================== AI INITIALIZATION ==========================
if __name__ == "__main__":
    psychology_ai = PsychologyAI()
    psychology_ai.start()

# AI Improvements:
❌ OpenAI API Error: 

You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742
