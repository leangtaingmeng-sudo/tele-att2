from huggingface_hub import InferenceClient
import os
# 1. Initialize the official client
HF_TOKEN = os.environ.get("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

def query_huggingface(user_text: str):
    try:
        # The client automatically handles the correct URLs and formatting!
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=250,
            temperature=0.7
        )
        # Extract the text from the response
        return response.choices[0].message.content
        
    except Exception as e:
        return f"API Error: {str(e)}"

# Test it out
if __name__ == "__main__":
    prompt = "Explain quantum computing in one simple sentence."
    print("Asking Hugging Face...\n")
    print(query_huggingface(prompt))
