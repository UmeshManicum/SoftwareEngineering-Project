from App.database import db

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    website = db.Column(db.String, nullable=True)
    
    competitions = db.relationship("CompetitionHost", lazy=True, backref=db.backref("competitions"), cascade="all, delete-orphan")

    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "website": self.website,
            "competitions": [competition.toDict() for competition in self.competitions]  # Assuming CompetitionHost has a toDict method
        }

    def toDict(self):
        res = {
            "id": self.id,
            "name": self.name,
            "website": self.website
        }
        return res
    