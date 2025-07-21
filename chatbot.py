import os
import json
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# Load environment variables from the .env file
load_dotenv()
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

# Validate API key
if not api_key:
    raise ValueError("API_KEY not found in .env file")

# Validate base_url
if base_url:
    # Initialize OpenAI client (new SDK style)
    client = OpenAI(base_url=base_url, api_key=api_key)
else:
    # Initialize OpenAI client (new SDK style)
    client = OpenAI(api_key=api_key)

history_file = "chat_history.json"


def predict(message, history):
    history_openai_format = []

    # Load chat history from file
    if os.path.isfile(history_file):
        with open(history_file, "r") as f:
            history_openai_format = json.load(f)

    # Append existing chat pairs
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})

    # Add latest message
    history_openai_format.append({"role": "user", "content": message})

    # Save history
    with open(history_file, "w") as f:
        json.dump(history_openai_format, f)

    # Call OpenAI with streaming response
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=history_openai_format,
            temperature=1.0,
            stream=True,
        )

        partial_message = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                partial_message += chunk.choices[0].delta.content
                yield partial_message
    except OpenAIError as e:
        yield f"Error from OpenAI: {e}"


# Gradio UI
demo = gr.ChatInterface(
    predict,
    chatbot=gr.Chatbot(
        show_copy_button=False,
        show_share_button=True,
        bubble_full_width=False,
        avatar_images=("./assets/img/user.png", "./assets/img/bot.png"),
    ),
    title="ChatBot",
    theme=gr.themes.Soft(),
    css="footer {visibility: hidden}",
    analytics_enabled=False,
).queue()

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        favicon_path="./assets/favicon/icons8-chatbot-32.png",
    )
