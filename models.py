from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from fastapi import Request
from fastapi.responses import RedirectResponse
from typing import Optional
from fastapi import Form
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("لم يتم العثور على API_KEY! تأكد من ملف .env")

file = 'data.csv'
header = ['subject', 'lesson', 'concept']


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


def airesponse(subject,lesson,explanation):

    response = client.chat.completions.create(
    model="upstage/solar-pro-3:free",
    messages=[
        {
            "role": "system",
            "content": (
            "أنت معلم خبير في تقنية فينمان. وظيفتك تقييم شرح الطلاب باللغة العربية.\n"
            "يجب أن يتكون ردك من 4 أقسام محددة كالتالي:\n"
            "SCORE: درجة من 100.\n"
            "SUMMARY: ملخص لمدى فهم الطالب.\n"
            "MISTAKES: قائمة بالأخطاء إن وجدت.\n"
            "FIX: إعادة شرح المفهوم بأسلوب مبسط جداً (8-20 سطر).\n"
            "قواعد هامة: استخدم اللغة العربية الفصحى البسيطة، كن مشجعاً، واجعل قسم FIX سهلاً جداً."
    )



        
        },
        {
            "role": "user",
            "content": f'start valuation the student explanation, subject={subject} lesson={lesson} , the most important thing is the student understanding = {explanation}   '
        }
    ],
    temperature=0.7
)
    return str(response.choices[0].message.content)


def ai_response_with_history(messages_list):
    response = client.chat.completions.create(
        model="upstage/solar-pro-3:free",
        messages=messages_list, 
        temperature=0.7 
    )
    return str(response.choices[0].message.content)

class User(SQLModel , table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fullname:str
    username:str = Field(unique=True)
    password:str

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id") 
    created_at: datetime = Field(default_factory=datetime.now)
    title: str 
    subject:str
    lesson:str
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str 
    role: str 
    conversation_id: int = Field(foreign_key="conversation.id")
    conversation: Conversation = Relationship(back_populates="messages")


        
