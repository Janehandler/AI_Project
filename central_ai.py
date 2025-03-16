import socket
import json
import os
import threading
import subprocess
from datetime import datetime

class UltimateBrainAI:
    def __init__(self):
        self.host = 'localhost'
        self.port = 7070
        self.memory = []
        self.logs = []
        self.running = True
        
        # ✅ Updated port numbers
        self.neural_bots = {
            "logic_ai": ("localhost", 7078),
            "memory_ai": ("localhost", 7073),
            "learning_ai": ("localhost", 7080),
            "self_analysis_ai": ("localhost", 7077),
            "news_ai": ("localhost", 7074),
            "trading_ai": ("localhost", 7081),
            "psychology_ai": ("localhost", 7076),
            "linguistic_ai": ("localhost", 7085),  # Fixed
            "security_ai": ("localhost", 7082),
            "attention_ai": ("localhost", 7086),  # Fixed
            "network_ai": ("localhost", 7087)  # Fixed
        }
        self.task_queue = []
        self.load_memory()
        self.start_multi_threading()

    # ========================== MEMORY SYSTEM ==========================
    def load_memory(self):
        """ Load memory data into the system """
        if os.path.exists("memory_data.json"):
            with open("memory_data.json", "r") as file:
                self.memory = json.load(file)

    def save_memory(self, message):
        """ Store memory in the system """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"timestamp": timestamp, "message": message}
        self.memory.append(entry)
        with open("memory_data.json", "w") as file:
            json.dump(self.memory, file)

    # ========================== TASK SYSTEM ==========================
    def start_multi_threading(self):
        """ Start the threads that will handle various tasks """
        num_threads = 6
        for _ in range(num_threads):
            thread = threading.Thread(target=self.task_worker, daemon=True)
            thread.start()

    def task_worker(self):
        """ Handle AI tasks in the background """
        while self.running:
            if self.task_queue:
                task = self.task_queue.pop(0)
                self.process_task(task)

    def process_task(self, task):
        """ Assign AI tasks to appropriate bots """
        if "TRADE" in task:
            response = self.communicate_with_bot("trading_ai", task)
        elif "ANALYZE" in task:
            response = self.communicate_with_bot("self_analysis_ai", task)
        elif "LEARN" in task:
            response = self.communicate_with_bot("learning_ai", task)
        else:
            response = "⚠️ Task format not recognized."

        self.save_memory(f"Task Processed: {task} -> Response: {response}")

    # ========================== COMMUNICATION SYSTEM ==========================
    def communicate_with_bot(self, bot_name, message):
        """ Sends a message to an AI bot and retrieves the response """
        if bot_name in self.neural_bots:
            host, port = self.neural_bots[bot_name]
            try:
                with socket.create_connection((host, port), timeout=2) as s:
                    s.sendall(message.encode())
                    response = s.recv(1024).decode()
                    return response
            except Exception as e:
                return f"❌ Error communicating with {bot_name}: {e}"
        return "⚠️ Invalid bot name."

    def check_bot_status(self):
        """ Checks the status of all bots """
        status = {}
        for bot, (host, port) in self.neural_bots.items():
            try:
                with socket.create_connection((host, port), timeout=1):
                    status[bot] = f"{bot.capitalize()} ✅ Online"
            except:
                status[bot] = f"{bot.capitalize()} ❌ Offline"
        return status

    def execute_command(self, command):
        """ Executes commands directed to AI Brain """
        if command.startswith("STATUS"):
            return self.check_bot_status()
        elif command.startswith("TASK"):
            task = command.replace("TASK:", "").strip()
            self.task_queue.append(task)
            return f"⚙️ Task added: {task}"
        elif command.startswith("BOT"):
            parts = command.split(":")
            if len(parts) == 3:
                return self.communicate_with_bot(parts[1], parts[2])
            else:
                return "⚠️ Invalid BOT command format."
        elif command.startswith("RECALL"):
            return self.communicate_with_bot("memory_ai", "RECALL")
        elif command.startswith("LEARN"):
            return self.communicate_with_bot("learning_ai", "LEARN")
        elif command.startswith("FETCH_NEWS"):
            return self.communicate_with_bot("news_ai", "FETCH")
        elif command.startswith("RESTART"):
            bot_name = command.replace("RESTART:", "").strip()
            return self.restart_bot(bot_name)
        else:
            return "⚠️ Unknown command."

    # ========================== INTERACTIVE AI TERMINAL ==========================
    def start_brain_terminal(self):
        """ Runs AI Brain in interactive mode for debugging and direct communication """
        print("\n🧠 Ultimate Brain AI is Online. Type commands below:")
        while self.running:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("🛑 Shutting down AI Brain...")
                break
            response = self.execute_command(user_input)
            print(f"AI Brain: {response}")

    # ========================== BOT MANAGEMENT SYSTEM ==========================
    def restart_bot(self, bot_name):
        """ Restarts a specific bot process if it crashes """
        if bot_name in self.neural_bots:
            script = f"/workspace/ai_project/{bot_name}.py"
            subprocess.Popen(["python3", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return f"🔄 Restarted {bot_name}."
        return f"⚠️ {bot_name} not found."

# ========================== AI SYSTEM INITIALIZATION ==========================
if __name__ == "__main__":
    brain_ai = UltimateBrainAI()
    brain_ai.start_brain_terminal()

# AI Improvements:
❌ OpenAI API Error: 

You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742
