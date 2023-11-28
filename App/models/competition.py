#from datetime import datetime
from App.database import db
from App.models import Host

class Competition(db.Model):
    __tablename__='competition'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    #date = db.Column(db.DateTime, default= datetime.utcnow)
    #location = db.Column(db.String(120), nullable=False)

    host_id = db.Column(db.Integer, nullable=False)
    participants = db.relationship('Student', secondary="competition_student", overlaps='competitions', lazy=True)

    def __init__(self, name, host_id):
        self.name = name
        self.host_id = host_id
        #self.location = location
    
    """def add_host(self, host):
        competition_host = CompetitionHost(comp_id=self.id, host_id=host.host_id)
        try:
            self.hosts.append(host)
            host.competitions.append(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    """
    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            #'date': self.date,
            #'location': self.location,
            #'hosts' : [host.username for host in self.hosts],
            'host_id': self.host_id,
            'participants': [student.username for student in self.participants]
        }

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            #"date": self.date,
            #"location": self.location,
            #'hosts' : [host.username for host in self.hosts],
            "host_id": self.host_id,
            "participants": [participant.toDict() for participant in self.participants]
        }

    def __repr__(self):
        return f'<Competition {self.id} : {self.name}>'
