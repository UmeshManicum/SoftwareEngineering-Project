from datetime import datetime
from App.database import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, content, is_read=False):
        self.user_id = user_id
        self.content = content
        self.is_read = is_read

    def get_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "is_read": self.is_read,
            "date_created": self.date_created
        }
