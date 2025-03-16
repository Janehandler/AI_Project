import openai
import os

# Set OpenAI API Key
openai.api_key = "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"

def analyze_code(file_path):
    """ Reads a Python file and suggests improvements using OpenAI """
    with open(file_path, "r") as file:
        code = file.read()
    
    prompt = f"Analyze the following Python code and suggest improvements:\n\n{code}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ OpenAI API Error: {e}"

def improve_files():
    """ Goes through all AI files and improves them """
    ai_files = [f for f in os.listdir() if f.endswith(".py") and f != "self_improve_ai.py"]
    
    for file in ai_files:
        improvements = analyze_code(file)
        with open(file, "a") as f:
            f.write("\n\n# AI Improvements:\n")
            f.write(improvements)
        print(f"✅ Improved {file}")

if __name__ == "__main__":
    improve_files()


# AI Improvements:
❌ OpenAI API Error: 

You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742
