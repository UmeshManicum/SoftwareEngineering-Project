from App.database import db

class UserCompetition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)


    def get_json(self):
        return {
            "id": self.id,
            "comp_id": self.comp_id,
            "user_id": self.user_id,
            "score": self.score,
            "rank": self.get_rank()
        }

    def to_dict(self):
        res = {
            "id": self.id,
            "comp_id": self.comp_id,
            "user_id": self.user_id,
            "score": self.score
        } 
        return res

    def get_rank(self):
        user_score = self.score

        rank = UserCompetition.query.filter_by(comp_id=self.comp_id).filter(UserCompetition.score > user_score).count() + 1

        return rank

