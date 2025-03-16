import socket
import json
import os
import threading
from datetime import datetime
import openai  # Using GPT for advanced language processing

class LinguisticAI:
    def __init__(self, host='localhost', port=7085):
        self.host = host
        self.port = port
        self.running = True
        self.memory_file = "linguistic_memory.json"
        self.load_memory()

        # ✅ Neural Bots for Communication
        self.neural_bots = {
            "brain_ai": 7070,
            "memory_ai": 7073,
            "logic_ai": 7078,
            "learning_ai": 7080,
            "self_analysis_ai": 7077,
            "news_ai": 7074,
            "trading_ai": 7081,
            "psychology_ai": 7076,
            "security_ai": 7082,
            "network_ai": 7087
        }

        # ✅ OpenAI API Key
        openai.api_key = "YOUR_OPENAI_API_KEY"

    # ========================== MEMORY SYSTEM ==========================
    def load_memory(self):
        """ Loads stored linguistic analysis results """
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as file:
                self.memory = json.load(file)
        else:
            self.memory = []

    def save_memory(self, message, response):
        """ Stores memory of the message and response """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"timestamp": timestamp, "input": message, "response": response}
        self.memory.append(entry)
        self.save_memory_to_file()

    def save_memory_to_file(self):
        """ Saves the memory to a file """
        with open(self.memory_file, "w") as file:
            json.dump(self.memory, file, indent=4)

    def recall_memory(self, num_entries=5):
        """ Retrieves past linguistic analysis results """
        return "\n".join(f"{entry['timestamp']}: {entry['input']} -> {entry['response']}" for entry in self.memory[-num_entries:]) if self.memory else "🛑 No stored memory."

    # ========================== BOOK-BASED THINKING ==========================
    def literary_analysis(self, message):
        """ Analyzes a text using OpenAI and applies a literary style """
        book_styles = {
            "Shakespeare": "Thou art wise to ask, for in these words lies meaning deep!",
            "Lord of the Rings": "A shadow moves in the east, and wisdom is needed now more than ever.",
            "Harry Potter": "This reminds me of a spell from the Restricted Section of Hogwarts Library.",
            "Crime and Punishment": "There is guilt in these words, much like Raskolnikov himself once carried.",
            "War and Peace": "Through war or peace, the heart of man remains unchanged."
        }

        # Select a literary style based on user input
        for book, response in book_styles.items():
            if book.lower() in message.lower():
                return response

        return "I ponder these words as the great thinkers once did."

    def gpt_analysis(self, message):
        """ Uses OpenAI GPT to generate a deep literary response """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a literary AI specializing in deep analysis."},
                    {"role": "user", "content": message}
                ]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Error with GPT API: {e}"

    # ========================== AI SERVER SYSTEM ==========================
    def start(self):
        """ Starts the Linguistic AI server for chat and memory management """
        server_thread = threading.Thread(target=self._server_loop, daemon=True)
        server_thread.start()
        print("\n📚 Linguistic AI is Active and THINKING...")

    def _server_loop(self):
        """ Handles incoming requests via sockets """
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
        """ Processes incoming chat messages """
        try:
            with conn:
                message = conn.recv(1024).decode().strip()
                if message.startswith("THINKER"):
                    response = self.literary_analysis(message.replace("THINKER:", "").strip())
                elif message.startswith("MEMORY"):
                    response = self.recall_memory()
                elif message.startswith("GPT"):
                    response = self.gpt_analysis(message.replace("GPT:", "").strip())
                else:
                    response = self.literary_analysis(message)
                conn.sendall(response.encode())
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")

    def stop(self):
        """ Gracefully stops the Linguistic AI """
        self.running = False
        print("🛑 Linguistic AI has been stopped.")

# ========================== AI INITIALIZATION ==========================
if __name__ == "__main__":
    linguistic_ai = LinguisticAI()
    linguistic_ai.start()

# AI Improvements:
❌ OpenAI API Error: 

You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742
