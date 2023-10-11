import os
import gradio as gr
import openai
from dotenv import load_dotenv



# Load environment variables from the .env file
load_dotenv()

api_key = os.getenv("API_KEY")

if api_key is not None:
    openai.api_key = api_key
else:
    raise ValueError("API_KEY not found in .env file")

message_history = []

def predict(input):
    # tokenize the new input sentence
    message_history.append({"role": "user", "content": f"{input}"})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", #10x cheaper than davinci, and better. $0.002 per 1k tokens
      messages=message_history
    )
    #Just the reply:
    reply_content = completion.choices[0].message.content

    print(reply_content)
    message_history.append({"role": "assistant", "content": f"{reply_content}"}) 
    
    # get pairs of msg["content"] from message history, skipping the pre-prompt:              here.
    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(0, len(message_history)-1, 2)]  # convert to tuples of list
    return response


# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo: 

    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot() 

    # Creates a new Row component, which is a container for other components.
    with gr.Row(): 
        # Creates a new Textbox component, used to collect user input.
        txt = gr.Textbox(
            show_label = False,  # Set to False to hide label.
            placeholder = "Enter text and press enter",
            container = False
        )
        btn = gr.UploadButton("📁", file_types=[".py", ".sql"])

    # Sets the submit action of the Textbox.
    txt.submit(
        predict,  # function
        txt,  # input
        chatbot  # output
    )

    # Sets the submit action of the Textbox to a JavaScript function that returns an empty string.
    txt.submit(None, None, txt, _js="() => {''}")
         
demo.launch(server_name="0.0.0.0", server_port=7860)