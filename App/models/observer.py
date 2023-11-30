from App.database import db
from App.models import message, User

class UserObserver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.PickleType)
    
    def __init__(self, user):
        self.user = user

    def update_user(user_id):
        user = User.query.filter_by(id=user_id).first()
        self.user = user
        return user

    def notify_rank_change(self, user_id, new_rank):
        user = update_user(user_id)
        if user_id == self.user.id:
            prev_rank = self.user.overall_rank
            user.overall_rank = new_rank
            user = update_user(user_id)

            if prev_rank is not None:
                if new_rank < prev_rank and new_rank <= 20:
                    message_content = f"You have risen to rank {new_rank} in the overall ranking!"
                elif new_rank > prev_rank and prev_rank <= 20:
                    message_content = f"You have fallen to rank {new_rank} in the overall ranking!"
            else:
                if new_rank <= 20:
                    message_content = f"You have risen to rank {new_rank} in the overall ranking!"

            message = Message(user_id=self.user.id, content=message_content, is_read=False)
            db.session.add(message)
            db.session.commit()
