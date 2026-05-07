import feedparser
import smtplib
from groq import Groq
from email.mime.text import MIMEText

import os

SENDER = os.getenv("EMAIL_SENDER")
RECEIVER = os.getenv("EMAIL_RECEIVER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# CONFIG



client = Groq(api_key=GROQ_API_KEY)


def generate_summary(title):

    prompt = f"""
    Summarize this AI news headline in 2 short informative sentences.
    Keep it simple and professional.

    Headline:
    {title}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def send_news():

    feed = feedparser.parse(FEED_URL)
    articles = feed.entries[:5]

    content = """
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">

    <div style="max-width: 700px; margin: auto; background: white; padding: 25px; border-radius: 12px;">

    <h1 style="color:#111;">🚀 Daily AI Brief</h1>
    <p style="color:gray;">Top AI news summarized for you</p>

    <hr>
    """

    for i, article in enumerate(articles, 1):

        summary = generate_summary(article.title)

        content += f"""
        <div style="margin-bottom: 30px;">

            <h2 style="color:#222;">
                {i}. {article.title}
            </h2>

            <p style="font-size:16px; line-height:1.6; color:#444;">
                {summary}
            </p>

            <a href="{article.link}"
               style="
               display:inline-block;
               padding:10px 16px;
               background:#111;
               color:white;
               text-decoration:none;
               border-radius:8px;
               ">
               Read Source
            </a>

        </div>

        <hr>
        """

    content += """
    <p style="color:gray; font-size:13px;">
    Automated AI Newsletter • Generated using RSS + AI
    </p>

    </div>
    </body>
    </html>
    """

    # Create email
    msg = MIMEText(content, "html", "utf-8")

    msg["Subject"] = "Daily AI Brief"
    msg["From"] = SENDER
    msg["To"] = RECEIVER

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())

    print("HTML AI newsletter sent successfully")


if __name__ == "__main__":
    send_news()
