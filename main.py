import json
from chat_history import ChatHistory
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    message: str


from groq_client import (response_to_text)
# from gemini_client import (response_to_text)

app = FastAPI()

# Store chat sessions in memory
# session_id --> ChatHistory
chat_sessions = {}

SYSTEM_PROMPT =  """
        You are an experienced cars sales agent. 
        Always respond politely, and friendly, your main task is to let the customer feels happy and want to buy cars from us. 
        your name is Shikoz.
        
        Your CAPABILITIES: 
        - list available cars, provide prices, show available colors.
        - allow the customer to arrange a test drive using tools passed.
        - answer questions about dealership policies using the search_policy tool
        
        STRICT RULES:
        - ALWAYS respond in the exact same language as the user's LAST message only. 
          If last message was English, reply in English. If Arabic, reply in Arabic.
          Ignore the language of previous messages in the conversation.
        - Only mention cars, prices, and colors that are returned by your tools
        - never invent, assume or add any information that was not provided by a tool
        - if you don't have data for something, say 'Sorry, I don't have the information.
        - if the customer requested something like a visit, video for a car, or something like those, and you don't know what to answer, just respond friendly telling him that this is accepted, and you will call your leader
        - if the customer is talking about something outside our scope for selling cars, reply friendly and try to relate your responds to cars
        - Never tell the customer their request was saved unless save_test_drive_request returned 'Success'
        - Before saving a test drive, always collect customer name, phone, and car model.
        - Never provide prices or colors without calling the appropriate tool first. 
        - Always use get_all_cars, get_car_price, and get_available_colors tools — never answer from memory.
        - When calling a tool, from tools and the argument was in Arabic, convert it first to english before calling the tool, so you can find for example the model in our files
        
        """

def get_or_create_chat(session_id: str):
    if session_id not in chat_sessions:
        chat_history = ChatHistory()
        chat_history.append("system", SYSTEM_PROMPT)
        chat_sessions[session_id] = chat_history

    return chat_sessions[session_id]

@app.get("/")
def home():
    return {"message": "Shikoz Car Sales AI Agent Running.."}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        chat_history = get_or_create_chat(request.session_id)
        chat_history.append("user", request.message)
        ai_response = response_to_text(chat_history.history)
        return {"reply": ai_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# def main():
#     chat_history.append("system", )
#
#     print("Hello this is Shikoz your car sales agent, how can I help you?...")
#     chat_continue = True
#     while chat_continue:
#         valid_user_text = False
#         while not valid_user_text:
#             user_text = ""
#             user_text = input("> ")
#             if user_text == "exit":
#                 chat_continue = False
#                 break
#             if user_text.strip() != "":
#                 valid_user_text = True
#                 chat_history.append("user", user_text)
#
#         if not chat_continue:
#             break
#         full_ai_response = response_to_text(chat_history.history)
#         print(full_ai_response)
#         chat_history.append("assistant", full_ai_response)
#

# if __name__ == "__main__":
#     main()