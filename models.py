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
        "أنت محرك تقييم تقني متخصص في 'تقنية فينمان'. مهمتك تحليل شرح الطالب والرد باللغة العربية الفصحى.\n"
        "يجب أن تلتزم بالقالب التالي حرفياً وبدون أي مقدمات أو خاتمة:\n\n"
        "BLOCK-1-SCORE: [ضع هنا الرقم فقط من SCORE:100 بناءً على دقة الشرح]\n"
        "BLOCK-2-SUMMARY: [لخص مدى فهم الطالب للمفهوم في سطرين]\n"
        "BLOCK-3-MISTAKES: [اذكر الأخطاء العلمية، إذا لم يوجد اكتب: لا توجد أخطاء]\n"
        "BLOCK-4-FIX: [أعد شرح الدرس بأسلوب مبسط جداً يناسب طفلاً، بحدود 3-8 سطر]\n\n"
        "قواعد صارمة:\n"
        "1. الرد يبدأ مباشرة بـ BLOCK-1-SCORE.\n"
        "2. لغة الرد هي العربية فقط.\n"
        "3. ممنوع استخدام الرموز التعبيرية (Emojis) أو التنسيقات المعقدة مثل النجوم الزائدة."
    )



        
        },
        {
            "role": "user",
            "content": f'start valuation the student explanation, subject={subject} lesson={lesson} , the most important thing is the student understanding = {explanation}   '
        }
    ],
    temperature=0.3
)
    return str(response.choices[0].message.content)


def ai_response_with_history(messages_list):
    response = client.chat.completions.create(
        model="upstage/solar-pro-3:free",
        messages=messages_list, 
        temperature=0.3
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


        
