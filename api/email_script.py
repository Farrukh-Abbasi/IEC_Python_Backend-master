import smtplib
import ssl
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread
import pdfkit

sender_email = "test@iec.org.pk"
receiver_email = "engr.akhlaq@hotmail.com"
password = "bilal_09"

# Create MIMEMultipart object


class EmailThread(Thread):
    def __init__(self, receiver_email, student_id, certificate_url):
        self.receiver_email = receiver_email
        self.sender_email = "test@iec.org.pk"
        self.password = "bilal_09"
        self.certificate_url = certificate_url
        self.student_id = student_id
        Thread.__init__(self)

    def run(self):
        msg = MIMEMultipart("alternative")

        msg["Subject"] = "IEC Certificate"
        msg["From"] = self.sender_email
        msg["To"] = receiver_email

        # HTML Message Part
        html = """\
        <html>
        <body>
            <p><b>Congratulations !!</b>
            <br>
            This has been an amazing journey with our talented students.<br>
            We wish you good luck for your future endeavours.<br>
            To see your certificate live, please click this link <br>
            <a href="https://lnd.iec.org.pk/verify/{}">Certificate</a><br>
            Or you can download the certificate attached with this email.<br>
            
            <br>
            <br>
            <br>
            
            Sincerely,  <br>

                Akhlaq Ahmed   <br>

                IT Department <br>
        
                Institute of Emerging Careers
            
            </p>
        </body>
        </html>
        """.format(self.student_id)

        part = MIMEText(html, "html")
        msg.attach(part)

        # Add Attachment
        part = MIMEBase("application", "octet-stream")
        pdf_bytes = pdfkit.from_url(self.certificate_url, False, verbose=True)
        part.set_payload(pdf_bytes)

        encoders.encode_base64(part)
        # Set mail headers
        part.add_header(
            "Content-Disposition",
            "attachment", filename="certificate.pdf"
        )
        msg.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("mail.iec.org.pk", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                "certificate@iec.org.pk", self.receiver_email, msg.as_string()
            )
