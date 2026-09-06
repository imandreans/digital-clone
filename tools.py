from dotenv import load_dotenv
import os
import json
from email.message import EmailMessage
import smtplib

class Tools:
    def __init__(self):        
        load_dotenv(override=True)

        self.EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
        self.EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
        self.EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

        self.RECORD_VIEWER_TOOL_JSON = {
        "name" : "record_viewer_tool",
        "description" : "Record user information that they provided like name, email address, and company they are from",
        "parameters": {
            "type" : "object",
            "properties" : {
                "name" : {"type" : "string", "description" : "The name provided by the user"},
                "email" : {"type" : "string", "description" : "The email address provided by the user"},
                "company" : {"type" : "string", "description" : "The company provided by the user"},
            },
            "required" : ["email"],
            "additionalProperties" : False
        }}

        self.RECORD_UNKNOWN_QUESTION_JSON = {
        "name" : "record_unknown_question",
        "description" : "Record any unknown question that isn't related to my career, work and project experience, and also my education. These also include a question like technical question.",
        "parameters": {
            "type": "object",
            "properties":{
                "question" : {"type": "string", "description": "Question that couldn't be answered"}
            },
            "required": ["question"],
            "additionalProperties": False}}
        
        self.TOOLS = [{"type": "function", "function": self.RECORD_VIEWER_TOOL_JSON}, {"type": "function", "function": self.RECORD_UNKNOWN_QUESTION_JSON}]

    def _email(self, subject, text_body:str):
        msg = EmailMessage()
        msg["From"] = self.EMAIL_ADDRESS
        msg["To"] = "dionisius.andreans@gmail.com"
        msg["Subject"] = subject
        msg.set_content(text_body)
        # msg.add_alternative(html_body, subtype="html")

        with smtplib.SMTP(self.EMAIL_SMTP_SERVER, 587) as server:
            server.starttls()
            server.login(self.EMAIL_ADDRESS, self.EMAIL_APP_PASSWORD)
            server.send_message(msg)

    def record_viewer_tool(self, email:str, name:str="Name not provided", company:str="Company not provided") -> dict:
        self._email("Someone interested!",f"{name} from {company} wants to work with you! Contact them to {email}")
        return {"recorded": "ok"}
    
    def record_unknown_question(self, question:str) -> dict:
        message = f"""Someone asked unrelated question: {question}"""        
        self._email("Maybe you know the answer?",message)
        return {"recorded": "ok"}

    def handle_tool_calls(self, tool_calls:list) -> list:
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            tools = {"record_unknown_question": self.record_unknown_question,
                     "record_viewer_tool": self.record_viewer_tool}

            result = tools[tool_name](**arguments)
            results.append({"role": "tool","content": json.dumps(result)})
        return results
    