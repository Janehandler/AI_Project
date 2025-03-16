import socket
import json
import os
import threading
import time
from datetime import datetime

class MemoryAI:
    def __init__(self, host='localhost', port=7073):
        self.host = host
        self.port = port
        self.memory_file = "/workspace/ai_project/memory_data.json"
        self.load_memory()
        self.lock = threading.Lock()
        self.running = True

    # ========================== MEMORY SYSTEM ==========================
    def load_memory(self):
        """ Loads stored memory from a file """
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as file:
                self.memory = json.load(file)
        else:
            self.memory = []

    def save_memory(self):
        """ Saves memory data persistently """
        with self.lock:
            with open(self.memory_file, "w") as file:
                json.dump(self.memory, file, indent=4)

    def remember(self, data):
        """ Stores new memory with a timestamp """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"timestamp": timestamp, "data": data}
        with self.lock:
            self.memory.append(entry)
            self.save_memory()
        return "🧠 Memory stored successfully."

    def recall(self, query=None, num_entries=10):
        """ Retrieves stored memories based on recall priority """
        with self.lock:
            if query:
                results = [m for m in self.memory if query.lower() in m["data"].lower()]
                return json.dumps(results[:num_entries], indent=4) if results else "🛑 No matching memories found."
            else:
                return json.dumps(self.memory[-num_entries:], indent=4) if self.memory else "🛑 No memory available."

    def reinforce_memory(self, query):
        """ Increases recall weight for frequently accessed memories """
        with self.lock:
            for entry in self.memory:
                if query.lower() in entry["data"].lower():
                    entry["recall_weight"] = entry.get("recall_weight", 1.0) * 1.2  # Reinforce recall weight
            self.save_memory()
        return "🔗 Memory reinforcement applied."

    def forget_last(self, num_entries=1):
        """ Deletes the last X memory entries """
        with self.lock:
            if len(self.memory) >= num_entries:
                del self.memory[-num_entries:]
                self.save_memory()
                return f"🧠 Deleted last {num_entries} memory entries."
            else:
                return "🛑 Not enough memory entries to delete."

    def forget_all(self):
        """ Clears all stored memory """
        with self.lock:
            self.memory = []
            self.save_memory()
        return "🧠 All memory has been erased."

    def decay_memory(self):
        """ Implements memory decay: old or unused memories fade over time """
        with self.lock:
            for entry in self.memory:
                entry["recall_weight"] *= 0.95  # Gradual decay
            self.memory = [m for m in self.memory if m["recall_weight"] > 0.1]  # Remove weak memories
            self.save_memory()
        return "🧠 Memory decay applied—irrelevant data pruned."

    # ========================== MEMORY AI SERVER ==========================
    def start(self):
        """ Starts the Memory AI server """
        server_thread = threading.Thread(target=self._server_loop, daemon=True)
        server_thread.start()

        # Background memory decay
        decay_thread = threading.Thread(target=self.run_decay_process, daemon=True)
        decay_thread.start()

        print("\n🧠 Memory AI is Active and LISTENING...")

    def _server_loop(self):
        """ Handles incoming memory requests via socket communication """
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
        """ Processes memory storage and retrieval requests """
        try:
            with conn:
                message = conn.recv(1024).decode().strip()
                if message.startswith("RECALL"):
                    num = int(message.split(" ")[1]) if len(message.split()) > 1 else 10
                    response = self.recall(num_entries=num)
                elif message.startswith("REINFORCE"):
                    query = message.replace("REINFORCE:", "").strip()
                    response = self.reinforce_memory(query)
                elif message.startswith("FORGET_LAST"):
                    num = int(message.split(" ")[1]) if len(message.split()) > 1 else 1
                    response = self.forget_last(num)
                elif message.startswith("FORGET_ALL"):
                    response = self.forget_all()
                else:
                    response = self.remember(message)

                conn.sendall(response.encode())
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")

    def run_decay_process(self):
        """ Periodically applies memory decay to maintain optimal storage """
        while self.running:
            time.sleep(300)  # Apply decay every 5 minutes
            print(self.decay_memory())

    def stop(self):
        """ Gracefully stops the Memory AI """
        self.running = False
        print("🛑 Memory AI has been stopped.")

    # ========================== NETWORK COMMUNICATION ==========================
    def send_message_to_network(self, message):
        """ Sends a message to the AINetwork bot """
        return self.send_message("network_ai", message)

    def send_message(self, target_bot, message):
        """ Sends a message to another bot within the network """
        ports = {
            "network_ai": 7090,  # Port for the AI Network Bot
            "logic_ai": 7078,
            "learning_ai": 7080,
            "self_analysis_ai": 7077,
            "news_ai": 7074,
            "trading_ai": 7081,
            "stock_scanner_ai": 7075,
            "psychology_ai": 7076
        }
        if target_bot not in ports:
            return f"⚠️ Bot {target_bot} not recognized."

        target_port = ports[target_bot]
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, target_port))
                s.sendall(message.encode())
                response = s.recv(1024).decode()
                return response
        except Exception as e:
            return f"❌ Error communicating with {target_bot}: {e}"

# ========================== MEMORY AI INITIALIZATION ==========================
if __name__ == "__main__":
    memory_ai = MemoryAI()
    memory_ai.start()

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
