import smtplib

# Email configuration
sender_email = "adanemoges6@gmail.com"
receiver_email = "adman19940805@gmail.com"
password = "dhva ihym luht jurc"

# Email content
subject = "Test Email"
body = "Hello, this is a test email."

# Connect to Gmail SMTP server
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    # server.starttls()  # Secure the connection
    server.login(sender_email, password)
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(sender_email, receiver_email, message)

print("Email sent successfully!")
