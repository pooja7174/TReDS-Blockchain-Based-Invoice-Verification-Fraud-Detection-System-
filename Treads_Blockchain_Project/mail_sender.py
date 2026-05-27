import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Gmail Sender", layout="centered")
st.title("📧 Send Email via Gmail")

# Sidebar for credentials
with st.sidebar:
    st.header("Gmail Configuration")
    sender_email = st.text_input("Your Gmail Address", type="password")
    sender_password = st.text_input("App Password", type="password", help="Use 16-character app-specific password")

# Main form
recipient_email = st.text_input("Recipient Email Address")
email_subject = st.text_input("Email Subject")
email_body = st.text_area("Email Body", height=200)

if st.button("Send Email", type="primary"):
    if not sender_email or not sender_password or not recipient_email or not email_subject:
        st.error("Please fill in all required fields")
    else:
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = email_subject
            message.attach(MIMEText(email_body, "plain"))
            
            # Send email
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            server.quit()
            
            st.success("✅ Email sent successfully!")
        except smtplib.SMTPAuthenticationError:
            st.error("❌ Authentication failed. Check your email and app password.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")