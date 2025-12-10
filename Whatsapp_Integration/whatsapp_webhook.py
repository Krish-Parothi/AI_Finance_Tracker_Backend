# whatsapp_webhook.py
from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from Whatsapp_Integration.whatsapp_user_service import signup_user, login_user
from Whatsapp_Integration.expense_service import add_expense
from Whatsapp_Integration.llm_parser import parse_text

router = APIRouter()

# In-memory session state mapping phone -> logged-in user
session_state = {}

@router.post("/webhook")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    resp = MessagingResponse()
    
    # Normalize message
    msg_lower = Body.strip().lower()
    
    # Check if user is logged in
    user = session_state.get(From)

    # Handle logout
    if msg_lower == "logout":
        if From in session_state:
            session_state.pop(From)
            resp.message("✅ You have been logged out.")
        else:
            resp.message("⚠️ You are not logged in.")
        return PlainTextResponse(str(resp), media_type="application/xml")
    
    if not user:
        if msg_lower.startswith("signup"):
            # Expect message like: "signup username password"
            try:
                _, username, password = Body.split()
                user_doc = signup_user(From, username, password)
                if user_doc:
                    resp.message("✅ Signup successful. Please login: send 'login <password>'")
                else:
                    resp.message("⚠️ User already exists. Please login.")
            except:
                resp.message("Send 'signup <username> <password>' to register.")
        elif msg_lower.startswith("login"):
            # Expect message like: "login password"
            try:
                _, password = Body.split()
                user_doc = login_user(From, password)
                if user_doc:
                    session_state[From] = user_doc  # mark as logged in
                    resp.message(f"✅ Login successful. Welcome {user_doc['username']}.\nYou can now add expenses.")
                else:
                    resp.message("❌ Login failed. Check your phone or password.")
            except:
                resp.message("Send 'login <password>' to login.")
        else:
            resp.message(
                "👋 Welcome to AI Finance Expense Tracker.\n"
                "Choose an option:\n"
                "1) Create a new account → send: signup <username> <password>\n"
                "2) Login to existing account → send: login <password>"
            )
    else:
        # Logged-in user; parse expenses
        parsed_entries = parse_text(Body)
        if not parsed_entries:
            resp.message("⚠️ Could not parse expenses. Try: 'Spent 500 on groceries'")
        else:
            for entry in parsed_entries:
                add_expense(user_id=user["public_code"], expense_data=entry)
            resp.message("✅ Expense added successfully.")
    
    return PlainTextResponse(str(resp), media_type="application/xml")
