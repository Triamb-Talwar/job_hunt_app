from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import os

# Step 1: Define your input schema
class SendEmailToolInput(BaseModel):
    recipient_email: str = Field(..., description="Email address of the recipient.")
    subject: str = Field(..., description="Subject of the email.")
    body: str = Field(..., description="Body text of the email.")

# Step 2: Define the tool itself
class SendEmailTool(BaseTool):
    name: str = "Send Gmail Email Tool"
    description: str = "Sends an email via Gmail using the Gmail API."
    args_schema: Type[BaseModel] = SendEmailToolInput

    def _run(self, recipient_email: str, subject: str, body: str) -> str:
        try:
            # Auth flow
            SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            service = build("gmail", "v1", credentials=creds)

            # Create the email message
            message = EmailMessage()
            message.set_content(body)
            message["To"] = 'triambtalwar03@gmail.com'
            message["From"] = "me"
            message["Subject"] = subject

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {
                "raw": encoded_message
            }

            send_message = service.users().messages().send(userId="me", body=create_message).execute()
            return f"✅ Email sent successfully! Message ID: {send_message['id']}"
        except Exception as e:
            return f"❌ Failed to send email: {str(e)}"
