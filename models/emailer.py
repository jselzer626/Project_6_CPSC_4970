import yagmail

class Emailer():
    """Singleton class that sends emails with a recipient list, 
    subject and message. Send_plain_email method is 
    called by team_members, competitions and teams. """

    _sole_instance = None
    sender_address = ""
    
    @classmethod 
    def configure(sender_address):
        sender_address = sender_address
    
    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance
    
    def __init__(self):
        self.recipients = []
        self.subject = ""
        self.message = ""
    
    def send_plain_email(self, recipients, subject, message):
        self.recipients = recipients
        self.subject = subject
        self.message = message
        try:
            yagmail.SMTP('testAuburnModule5@gmail.com').send(recipients, subject, message)
            return "Success - process complete."
        except:
            return "Error - send not successful."
    