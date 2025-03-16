import openai
import os

# Set OpenAI API Key (replace with yours)
openai.api_key = "YOUR_OPENAI_API_KEY"

def analyze_code(file_path):
    """ Reads a Python file and suggests improvements using OpenAI """
    with open(file_path, "r") as file:
        code = file.read()
    
    prompt = f"Analyze the following Python code and suggest improvements:\n\n{code}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

def improve_files():
    """ Goes through all AI files and improves them """
    ai_files = [f for f in os.listdir() if f.endswith(".py")]
    
    for file in ai_files:
        improvements = analyze_code(file)
        with open(file, "a") as f:
            f.write("\n\n# AI Improvements:\n")
            f.write(improvements)
        print(f"✅ Improved {file}")

if __name__ == "__main__":
    improve_files()
