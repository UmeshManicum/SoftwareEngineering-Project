from App.database import db

class UserObserver:
    def __init__(self, user):
        self.user = user

    def notify_rank_change(self, user_id, new_rank):
        if user_id == self.user.id:
            prev_rank = self.user.overall_rank
            self.user.overall_rank = new_rank

            if prev_rank is not None:
                if new_rank < prev_rank:
                    message_content = f"You have risen to rank {new_rank} in the overall ranking!"
                elif new_rank > prev_rank:
                    message_content = f"You have fallen to rank {new_rank} in the overall ranking!"
                else:
                    message_content = f"Your overall rank remains {new_rank}."

                from App.models import Message
                message = Message(user_id=self.user.id, content=message_content, is_read=False)
                db.session.add(message)
                db.session.commit()
