import os
import openai
import gradio as gr
from dotenv import load_dotenv
import json

# Load environment variables from the .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# Handle if "API_KEY" is absent or expired.
try:
    if api_key is not None:
        openai.api_key = api_key
    else:
        raise ValueError("API_KEY not found in .env file")
except Exception as e:
    print(f'Caught an Exception: {e}')


history_file = "chat_history.json"

def predict(message, history):
    history_openai_format = []
    if os.path.isfile(history_file):
        with open(history_file, "r") as f:
            history_openai_format = json.load(f)

    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
        
    history_openai_format.append({"role": "user", "content": message})

    with open(history_file, "w") as f:
        json.dump(history_openai_format, f)

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=history_openai_format,
        temperature=1.0,
        stream=True
    )

    partial_message = ""
    for chunk in response:
        if len(chunk['choices'][0]['delta']) != 0:
            partial_message = partial_message + chunk['choices'][0]['delta']['content']
            yield partial_message

demo = gr.ChatInterface(
    predict,
    chatbot=gr.Chatbot(
        show_copy_button=False,
        show_share_button=True,
        bubble_full_width=False,
        avatar_images=("./assets/img/user.svg", "./assets/img/bot.png")
    ),
    title='ChatBot',
    theme=gr.themes.Soft(),
    css="footer {visibility: hidden}",
    analytics_enabled=False
).queue()

if __name__=='__main__':
    demo.launch(server_name="0.0.0.0", server_port=7878, favicon_path="./assets/favicon/icons8-chatbot-32.png")