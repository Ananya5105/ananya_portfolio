import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.get("/")
async def serve_portfolio():
    # Serve the HTML file when someone visits the homepage
    return FileResponse("ananya_portfolio.html")

@app.post("/api/send")
async def send_email(form: ContactForm):
    # Configuration
    SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "alphadotdelta@gmail.com")
    SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD") # App Password
    RECEIVER_EMAIL = SENDER_EMAIL # Send to yourself

    if not SENDER_PASSWORD:
        raise HTTPException(status_code=500, detail="Server misconfiguration: SENDER_PASSWORD not set")

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"New Portfolio Message from {form.name}"

    body = f"""
    You have received a new message from your portfolio contact form:
    
    Name:   {form.name}
    Email:  {form.email}
    
    Message:
    {form.message}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail SMTP Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return {"success": True, "message": "Email sent successfully!"}
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")
