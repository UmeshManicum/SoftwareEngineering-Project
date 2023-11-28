from datetime import datetime
from App.database import db

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default= datetime.utcnow)
    location = db.Column(db.String(120), nullable=False)

    Competitor_Scores={}

    hosts = db.relationship("CompetitionHost", lazy=True, backref=db.backref("hosts"), cascade="all, delete-orphan")
    participants = db.relationship("UserCompetition", lazy=True, backref=db.backref("users"), cascade="all, delete-orphan")


    def __init__(self, name, location):
        self.name = name
        self.location = location


    def assign_Score(self, user, score):
        self.Competitor_Scores[user.id]=score
    
    def get_Score(self, user):
        return self.Competitor_Scores[user.id]
    
    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat(),  # Convert datetime to a string representation
            'location': self.location,
            'hosts': [host.get_json() for host in self.hosts],  # Assuming CompetitionHost has a get_json method
            'participants': [participant.get_json() for participant in self.participants]  # Assuming UserCompetition has a get_json method
        }


    def toDict(self):
        res = {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "location": self.location,
            "hosts": [host.toDict() for host in self.hosts],
            "participants": [participant.toDict() for participant in self.participants]
        } 
        return res
