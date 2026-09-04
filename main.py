from dotenv import load_dotenv
import os
import gradio as gr
# from ollama import Client
from openai import OpenAI
import copy
from tools import Tools
from context import Context

CV_PATH = 'cv.txt'
MODEL = "openai/gpt-oss-20b"

tool = Tools()
context = Context(cv_path=CV_PATH)

load_dotenv(override=True)

client = OpenAI(
   api_key=os.environ.get('OPENROUTER_API_KEY'),
   base_url=os.environ.get('OPENROUTER_BASE_URL')
)

# Convert content from list into string
def clean_history(history: list[dict[str, any]]) -> list[dict[str, any]]:
  history = copy.deepcopy(history)
  for i, chat in enumerate(history):
    history[i]['content'] = chat['content'][0]['text']
  return history

# Loop conversation 
def convo(message: str, history: list[dict[str, any]]) -> str:
    history = clean_history(history)
    messages = [{"role": "system", "content": context.get_system_prompt()}] + history + [{"role": "user", "content": message}]
    done = False

    while not done:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tool.TOOLS)
        
        # Check if tool is called
        if response.choices[0].finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = tool.handle_tool_calls(tool_calls)
            messages.append(message) # Put single value in the end of messages
            messages.extend(results) # Put multiple values in the end of the messages
        else:
            done = True
    return response.choices[0].message.content

if __name__ == "__main__":
   gr.ChatInterface(convo).launch(
      server_name="0.0.0.0",
      server_port=7860,
      inbrowser=False
   )
