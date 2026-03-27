
from rich.console import Console
import json
from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner, trace, function_tool
import requests
import resend
import asyncio
import os

load_dotenv(override=True)


# In your env file, add your values for the following (including OPENAI_API_KEY):  
RESEND_KEY= os.getenv("RESEND_API_KEY");  
RECIPIENT_NAME = os.getenv("RECIPIENT_NAME")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
# OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")


@function_tool
def send_email(body: str):
    """
    Send an email with the given body.
    
    Args:
    body: the content of the email to be sent
    """
    
    print(f"Attempting to send email with the body: {body}")  # Log the attempt to send email with the provided body
    
    try:
        # Prepare headers for the API request including authorization and content type
        headers = {
            "Authorization": f"Bearer {RESEND_KEY}",  # Authorization header using API key
            "Content-Type": "application/json"
        }
        
        formatted_body =  body.replace("\n", "<br>")
        
        
        # prepare the email
        payload = {
            "from": EMAIL_FROM,
            "to": EMAIL_TO,
            "subject": "Your Test Agent SDR",
            "html": f"""
            <html>
            <body>
                {formatted_body}
            </body
            </html>
            """
        }
        
        # make an HTTP request to the Resend API to send an email
        response = requests.post(
            "https://api.resend.com/emails",
            json=payload,
            headers=headers)
        
        
        if response.status_code == 200:
            print("Email sent successfully")
            return {"success": True, "message": "Email sent successfully", "response": response.json}
        else:
            print(f"Failed to send email. Response: {response.text}")
    
    
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        return {"success": False, "message": f"Exception occurred: {str(e)}"}
    

# ready the agent    
async def main():
    print("Starting the email agent...")
    
    agent = Agent(name="Send email agent", tools=[send_email])
    
    email_context = {
        "recipient_name": RECIPIENT_NAME,
        "sender_name": "Agent-SDR-007",
        "topic": "Testing Agent email sending",
        "key-points": ["The email is a test", "it is sent by an agent", "No need to respond to the email"],
    }

    message = f"""
    Send an email with the following details:
    - Recipient: {email_context['recipient_name']}
    - Topic: {email_context['topic']}
    - Key points to include: {', '.join(email_context['key-points'])}
    - Sender name:  {email_context['sender_name']}
    """
    
    result = await Runner.run(agent, message)
        
# start the emailing process 
if __name__ == "__main__":
    asyncio.run(main())


