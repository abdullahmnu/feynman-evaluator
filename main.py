from models import User,Conversation,Message,airesponse,ai_response_with_history
from security import get_password_hash, verify_password
from fastapi import FastAPI ,Request , Form ,Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware     
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
SECRET_KEY = os.getenv("SECRET_KEY")
templates= Jinja2Templates(directory='templates')
engine = create_engine("sqlite:///database.db", echo=True) 
SQLModel.metadata.create_all(engine)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=604800
)

def get_db():
    with Session(engine) as session:
        yield session
def get_session_user(request: Request):
    return request.session.get("user_id")

@app.get("/")
async def main(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")
    u_id = request.session.get("user_id")
    
    conversations = []
    total_ai_msgs = 0
    
    if u_id:
        conversations = db.exec(
            select(Conversation)
            .where(Conversation.user_id == u_id)
            .order_by(Conversation.created_at.desc())
        ).all()
        
        ai_msgs = db.exec(
            select(Message).join(Conversation,Message.conversation_id == Conversation.id)
            .where(Conversation.user_id == u_id, Message.role == "assistant")
        ).all()
        total_ai_msgs = len(ai_msgs)
    
    return templates.TemplateResponse("main.html", {
        "request": request,
        "username": username,
        "conversations": conversations,
        "total_ai_msgs": total_ai_msgs
    })

@app.get("/tos")
async def tos(request: Request):
    return templates.TemplateResponse("tos.html", {"request": request})

@app.get("/privacy")
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@app.api_route("/register", methods=["GET", "POST"])
async def reg_data(request:Request,
    fullname: str = Form(None),
    username: str = Form(None),
    password: str = Form(None)
):
    if request.method == "POST":
        hashed_pass=get_password_hash(password)
        new_user=User(username=username, password=hashed_pass, fullname=fullname)
        with Session(engine) as session:
            session.add(new_user)
            session.commit()
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("register.html", {"request": request})


@app.api_route("/login", methods=["GET", "POST"])
async def login_data(request: Request, username: str = Form(None), password: str = Form(None)):
    if request.method == "POST":
        with Session(engine) as session:
            statement= select(User).where(User.username==username)
            dbUser=session.exec(statement).first()

            if dbUser and verify_password(password, dbUser.password):
                request.session["user_id"] = dbUser.id
                request.session["username"] = dbUser.username
                return RedirectResponse(url="/", status_code=303)
            return {"status": "fail"}
    return templates.TemplateResponse("login.html", {"request": request})



@app.get("/chat/{conv_id}")
async def get_chat_history(
    conv_id: int, 
    request: Request, 
    db: Session = Depends(get_db)
):
    u_id = get_session_user(request)
    if not u_id:
        return RedirectResponse(url="/login", status_code=303)
    all_convs = db.exec(select(Conversation).where(Conversation.user_id == u_id).order_by(Conversation.created_at.desc())).all()
    statement_check = select(Conversation).where(
        Conversation.id == conv_id, 
        Conversation.user_id == u_id
    )
    conversation = db.exec(statement_check).first()

    if not conversation:
        return RedirectResponse(url="/", status_code=303)

    statement = select(Message).where(Message.conversation_id == conv_id).order_by(Message.id)
    history = db.exec(statement).all()

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "all_conversations": all_convs,
        "messages": history,
        "conv_id": conv_id,
        "title": conversation.title 
    })

@app.get("/chat")
async def chat_default(request: Request, db: Session = Depends(get_db)):
    u_id = get_session_user(request)
    if not u_id: return RedirectResponse(url="/login")

    last_conv = db.exec(select(Conversation).where(Conversation.user_id == u_id).order_by(Conversation.created_at.desc())).first()
    
    if last_conv:
        return RedirectResponse(url=f"/chat/{last_conv.id}")
    else:
        return RedirectResponse(url="/")

@app.post("/chat")
async def chat(request: Request, 
    title: str = Form(...),
    lesson: str = Form(...),
    subject: str = Form(...),
    explanation:str=Form(...),
):

    u_id = get_session_user(request)
    if not u_id:
        return RedirectResponse(url="/login", status_code=303)
    
    with Session(engine) as session:
        newConversation = Conversation(user_id=u_id,title=title ,subject=subject,lesson=lesson)
        session.add(newConversation)
        session.commit()
        session.refresh(newConversation)

        newMessages=Message(conversation_id=newConversation.id,content=explanation,role="user")
        AIresponse=Message(conversation_id=newConversation.id,content=airesponse(subject,lesson,explanation),role="assistant")
    
        session.add(newMessages)
        session.add(AIresponse)
        session.commit()

        return RedirectResponse(url=f"/chat/{newConversation.id}", status_code=303)
    
@app.post("/chat/{conv_id}")
async def continue_chat(conv_id: int, request: Request, explanation: str = Form(...), db: Session = Depends(get_db)):
    u_id = get_session_user(request)
    if not u_id: return RedirectResponse(url="/login", status_code=303)

    conv = db.get(Conversation, conv_id)
    old_messages = db.exec(select(Message).where(Message.conversation_id == conv_id).order_by(Message.id)).all()

    ai_memory = [
        {"role": "system", "content": f"You are a Feynman Technique valuation teacher that received students explanation,infirstline block-1-score the student explanation from 100, block-2-Summary is the student undrstant what he is saying, block-3-Mistakes if there is what are they,block-4-Fix and give a simple teaching make it simple and easy and 8-20 lines max, response will be a massage for the student, plain response its a reply message, use the same word after block number in capital like block-1-score type it only SCORE: "}
    ]
    for msg in old_messages:
        ai_memory.append({"role": msg.role, "content": msg.content})

    ai_memory.append({"role": "user", "content": explanation})

    new_user_msg = Message(content=explanation, role="user", conversation_id=conv_id)
    db.add(new_user_msg)
    db.commit()

    ans = ai_response_with_history(ai_memory)

    new_ai_msg = Message(content=ans, role="assistant", conversation_id=conv_id)
    db.add(new_ai_msg)
    db.commit()

    return RedirectResponse(url=f"/chat/{conv_id}", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear() 
    return RedirectResponse(url="/", status_code=303)