import smtplib, ssl

class EmailManager:

    def sendEmail(self, recip, code):
        port = 465  # For SSL
        password = "Green2GoApp!"
        # Create a secure SSL context
        context = ssl.create_default_context()

        sent_from = "CapstoneSpring2021@gmail.com"
        to = recip
        subject = 'Verification Code For Green2Go'
        body = "Your Verification Code is " + str(code)

        email_text = "From: " + sent_from + '\n' + "To: " + to + '\n' + "Subject: " + subject + '\n' + '\n' + body

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("CapstoneSpring2021@gmail.com", password)
                server.sendmail("CapstoneSpring2021@gmail.com", recip, email_text)
            return "Success!"
        except:
            return "Failed!"