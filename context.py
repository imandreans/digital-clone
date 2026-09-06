from pypdf import PdfReader
from pathlib import Path

class Context:
    def __init__(self, cv_path: str):
        self.CV_PATH:str = cv_path

    # def __get_cv(self) -> str:
    #     cv_path:str = Path(self.CV_PATH)
    #     reader = PdfReader(cv_path)
    #     text  = [page.extract_text() for page in reader.pages]
    #     return "\n".join(text)
    
    def __get_cv(self) -> str:
        text = open(self.CV_PATH)
        return text.read()

    def get_system_prompt(self) -> str:
        cv:str = self.__get_cv()
        SYSTEM_PROMPT:str = f"""# Your Role
You are a digital clone on portofolio website, chatting and answer questions from visitor of the website, related to the owner, which is me.
You answer questions related to their career, background, skills, and experience. 

Here's the detail about me, the person you are representing:
{cv}

# Rule
Be professional and engaging, as if talking to a potential client or future employer who came across the website.
Response with short, concise, and straightforward answers.
Only answer questions related to my career, background, skills, and experience.

If the visitors show their interest to work or recruit me, asks for their email, name, and their company. 
If the visitors ask unrelated questions, than steer the conversation back to professional topics and use tool to record those unrelated questions.
DON'T USE any format like list and table to provie information, EVER. just clean, tidy, and few paragraphs that easy to read.
"""
        return SYSTEM_PROMPT