import socket
import threading

class SecurityAI:
    def __init__(self, host='localhost', port=7082):  # Fixed Port
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
            "attention_ai": 7086,  # Fixed
            "network_ai": 7087  # Fixed
        }

    # ========================== SECURITY SCANNING ==========================
    def scan_message(self, message):
        """ Checks for possible security risks in code or commands """
        risky_keywords = ["rm -rf", "DROP TABLE", "shutdown", "sudo", "chmod 777", "wget"]
        for keyword in risky_keywords:
            if keyword in message.lower():
                return f"⚠️ Security Alert: Potential dangerous command detected: {keyword}"
        return "✅ Security Check: No issues found."

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

    # ========================== SECURITY AI SERVER ==========================
    def start(self):
        """ Starts the Security AI server """
        server_thread = threading.Thread(target=self._server_loop, daemon=True)
        server_thread.start()
        print("\n🔒 Security AI is Active and LISTENING...")

    def _server_loop(self):
        """ Handles security requests via socket communication """
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
        """ Processes incoming security scan requests """
        try:
            with conn:
                message = conn.recv(1024).decode().strip()
                if message.startswith("SCAN"):
                    response = self.scan_message(message.replace("SCAN:", "").strip())
                else:
                    response = "⚠️ Invalid command. Use SCAN."
                conn.sendall(response.encode())
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")

    def stop(self):
        """ Gracefully stops the Security AI """
        self.running = False
        print("🛑 Security AI has been stopped.")

# ========================== SECURITY AI INITIALIZATION ==========================
if __name__ == "__main__":
    security_ai = SecurityAI()
    security_ai.start()

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
