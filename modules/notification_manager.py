import smtplib

from email.mime.text import MIMEText

from modules.wg import WG


class NotificationManager:
    def __init__(self, email: str, password: str):
        self.email: str = email
        self.password: str = password

    def send_email(self, new_wgs: list[WG]):
        """
        Sends an email with the data of the new WGs
        """
        body: str = "These new offers meet all your filters: \n\n"
        for wg in new_wgs:
            body += f"- {str(wg)}\n"

        msg: MIMEText = MIMEText(body)
        msg["Subject"] = f"{len(new_wgs)} new WG offers found!"
        msg["From"] = self.email
        msg["To"] = self.email

        with smtplib.SMTP("smtp.gmail.com") as server:
            server.starttls()
            server.login(user=self.email, password=self.password)
            server.sendmail(self.email, self.email, msg.as_string())
