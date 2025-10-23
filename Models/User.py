from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, registration, fullname, email, awsteam, coreteam, pfp_link, year, whatsapp, cloudcaptain=False, mentor=False):
        self.registration = registration
        self.fullname = fullname
        self.email = email
        self.awsteam = awsteam
        self.coreteam = coreteam
        self.cloudcaptain = cloudcaptain
        self.mentor = mentor
        self.pfp_link = pfp_link
        self.year = year
        self.whatsapp = whatsapp

    def get_id(self):
        return self.registration