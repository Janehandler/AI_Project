import socket
import json
import threading
import time

class AINetwork:
    def __init__(self, host='localhost', port=7087):
        """ AI Network Bot: Manages AI-to-AI communication and knowledge sharing """
        self.host = host
        self.port = port
        self.neural_bots = {
            "brain_ai": 7070,
            "logic_ai": 7078,
            "memory_ai": 7073,
            "learning_ai": 7080,
            "self_analysis_ai": 7077,
            "news_ai": 7074,
            "trading_ai": 7081,
            "psychology_ai": 7076,
            "linguistic_ai": 7085,  # Fixed
            "security_ai": 7082,
            "attention_ai": 7086,  # Fixed
            "network_ai": 7087  # Fixed
        }
        self.running = True

    # ========================== AI COMMUNICATION SYSTEM ==========================
    def send_message(self, target_bot, message):
        """ Sends a message to another AI bot """
        if target_bot not in self.neural_bots:
            return f"⚠️ Target bot '{target_bot}' not recognized."

        target_port = self.neural_bots[target_bot]
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, target_port))
                s.sendall(message.encode())
                response = s.recv(1024).decode()
                return response
        except Exception as e:
            return f"❌ Error communicating with {target_bot}: {e}"

    def receive_message(self, conn):
        """ Processes incoming messages from AI Brain or other AI bots """
        try:
            with conn:
                message = conn.recv(1024).decode().strip()
                return self.process_request(message)
        except Exception as e:
            return f"⚠️ Connection Error: {e}"

    def process_request(self, message):
        """ Handles incoming requests and routes them to appropriate AI subsystems """
        if message.startswith("BROADCAST:"):
            return self.broadcast_message(message.replace("BROADCAST:", "").strip())
        elif message.startswith("REQUEST:"):
            parts = message.split(":")
            if len(parts) == 3:
                return self.send_message(parts[1], parts[2])
            return "⚠️ Invalid REQUEST format."
        return f"📡 Received message: {message} | No specialized response set."

    def broadcast_message(self, data):
        """ Sends the same message to all AI bots """
        responses = {}
        for bot_name in self.neural_bots.keys():
            responses[bot_name] = self.send_message(bot_name, data)
        return json.dumps(responses, indent=4)

    # ========================== AI SERVER SYSTEM ==========================
    def start_server(self):
        """ Starts the AI Network bot's server """
        server_thread = threading.Thread(target=self._server_loop, daemon=True)
        server_thread.start()
        print("\n🔗 AI Network is Active and LISTENING...")

    def _server_loop(self):
        """ Runs the AI network server to handle incoming requests """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while self.running:
                try:
                    conn, addr = s.accept()
                    response = self.receive_message(conn)
                    conn.sendall(response.encode())
                except Exception as e:
                    print(f"❌ Server Error: {e}")

    def stop(self):
        """ Gracefully stops the AI Network bot """
        self.running = False
        print("🛑 AI Network has been shut down.")

# ========================== AI NETWORK SYSTEM INITIALIZATION ==========================
if __name__ == "__main__":
    network_ai = AINetwork()
    network_ai.start_server()

# AI Improvements:
❌ OpenAI API Error: 

You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742
