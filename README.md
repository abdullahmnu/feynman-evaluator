# eynman Evaluator

An application designed to help students master academic concepts using the **Feynman Technique**. Users explain a concept in their own words, and the AI evaluates their explanation, identifies knowledge gaps, and provides feedback to simplify the information.

I developed this project primarily as a personal challenge to improve my software development and backend engineering skills.

## 🚀 Features

- **Full Auth System:** Secure user registration and session-based login.
- **Chat Management:** Create multiple independent chats and access complete session history.
- **Conversational Memory:** The AI remembers past context within a chat to provide continuous, cumulative feedback.
- **Smart Evaluation:** Analyzes explanations based on simplicity, clarity, and scientific accuracy.

## 🛠️ Tech Stack

- **Backend:** [Python](https://www.python.org/) with [FastAPI](https://fastapi.tiangolo.com/) framework.
- **Database:** PostgreSQL (Managed on Render) for relational data storage.
- **AI Engine:** [Upstage Solar] model accessed via the [OpenRouter] platform.
- **Authentication:** Session-based auth using SHA-256 hashing.
- **Frontend:** Vanilla HTML, CSS, and JavaScript (UI layouts and styling assisted by AI).

## 🧠 How It Works

The system converts the ongoing chat history into an interactive conversational memory. This context is sent to the AI with every user prompt, allowing for a continuous educational dialogue rather than isolated, single-turn responses.

## 📥 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/abdullahmnu/feynman-evaluator.git](https://github.com/abdullahmnu/feynman-evaluator.git)
   cd feynman-evaluator

    Install the required dependencies:
    Bash

    pip install -r requirements.txt

    Configure your environment variables (Create a .env file):
    مقتطف الرمز

    API_KEY=your_api_key_here
    SECRET_KEY=your_secret_key_here

    Run the development server:
    Bash

    uvicorn main:app --reload
   

## 📝 Notes & Credits

This project focuses on providing a clean, distraction-free, and simple UI for students. AI integration is utilized to ensure a highly interactive and practical learning experience.

Developed by: [abdullahmnu]

#📄 License

MIT License

Copyright (c) 2026 abdullahmnu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
