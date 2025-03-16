import socket
import os
import json
import threading
import subprocess
from datetime import datetime

class SelfAnalysisAI:
    def __init__(self, host='localhost', port=7077):
        self.host = host
        self.port = port
        self.analysis_log = "analysis_log.json"
        self.load_analysis_history()
        self.running = True
        self.lock = threading.Lock()

        # ✅ Updated Neural Bots Port Mapping
        self.neural_bots = {
            "brain_ai": 7070,
            "memory_ai": 7073,
            "logic_ai": 7078,
            "learning_ai": 7080,
            "news_ai": 7074,
            "trading_ai": 7081,
            "psychology_ai": 7076,
            "linguistic_ai": 7085,  # Fixed
            "security_ai": 7082,
            "attention_ai": 7086,  # Fixed
            "network_ai": 7087  # Fixed
        }

    # ========================== ANALYSIS MEMORY ==========================
    def load_analysis_history(self):
        """ Loads past analysis results for self-improvement tracking """
        if os.path.exists(self.analysis_log):
            with open(self.analysis_log, "r") as file:
                self.analysis_history = json.load(file)
        else:
            self.analysis_history = {}

    def save_analysis(self, filename, suggestions):
        """ Stores code analysis results persistently """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.lock:
            self.analysis_history[filename] = {
                "timestamp": timestamp,
                "suggestions": suggestions
            }
            with open(self.analysis_log, "w") as file:
                json.dump(self.analysis_history, file, indent=4)

    def recall_analysis(self, filename):
        """ Retrieves past analysis results for a file """
        with self.lock:
            return json.dumps(self.analysis_history.get(filename, "🛑 No past analysis found."), indent=4)

    # ========================== CODE ANALYSIS ==========================
    def analyze_code(self, filename):
        """ Reads and analyzes Python code to suggest improvements """
        if not os.path.exists(filename):
            return f"❌ Error: {filename} not found."

        with open(filename, "r") as file:
            code = file.read()

        suggestions = self.perform_code_analysis(code)
        self.save_analysis(filename, suggestions)
        return f"📊 Code Analysis for {filename}:\n" + "\n".join(suggestions)

    def perform_code_analysis(self, code):
        """ Performs detailed analysis on AI code """
        suggestions = []
        if "import socket" in code:
            suggestions.append("✅ Code uses sockets—ensure proper connection handling.")
        if "try:" in code and "except" not in code:
            suggestions.append("⚠️ Possible incomplete error handling—try block detected without except.")
        if "time.sleep" in code:
            suggestions.append("⏳ Code uses delays—consider optimizing performance.")
        if "subprocess" in code:
            suggestions.append("🔧 External process detected—ensure secure execution.")
        if len(code) > 3000:
            suggestions.append("⚠️ Large file detected—consider modularizing for maintainability.")

        return suggestions if suggestions else ["✅ No issues detected."]

    # ========================== SELF-ANALYSIS AI SERVER ==========================
    def start(self):
        """ Starts the Self-Analysis AI for real-time code checking """
        server_thread = threading.Thread(target=self._server_loop, daemon=True)
        server_thread.start()
        print("\n🧠 Self-Analysis AI is Active and LISTENING...")

    def _server_loop(self):
        """ Handles incoming self-analysis requests via sockets """
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
        """ Processes self-analysis and security requests """
        try:
            with conn:
                message = conn.recv(1024).decode().strip()
                if message.startswith("ANALYZE"):
                    response = self.analyze_code(message.replace("ANALYZE:", "").strip())
                else:
                    response = "⚠️ Invalid command. Use ANALYZE."
                conn.sendall(response.encode())
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")

    def stop(self):
        """ Gracefully stops the AI """
        self.running = False
        print("🛑 Self-Analysis AI has been stopped.")

# ========================== SELF-ANALYSIS AI INITIALIZATION ==========================
if __name__ == "__main__":
    self_ai = SelfAnalysisAI()
    self_ai.start()

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
