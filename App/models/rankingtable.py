from App.models import Competition, User, UserCompetition
from App.models.observer import UserObserver
from App.database import db

class RankingTable:
    def __init__(self):
        self.users = {}
        self.observers = set()

    def add_observer(self, observer):
        if observer[user_id] not in self.observers:
            self.observers.add(observer)

    def remove_observer(self, observer):
        for observer in self.observers:
            observer.update_user()
        self.observers.remove(observer)

    def notify_observers(self, user_id, new_rank):
        for observer in self.observers:
            observer.update_user()
            observer.notify_rank_change(user_id, new_rank)
    
    """
    def update_users(self):
        for curr_user in self.users:
            user = User.query.filter_by(id=curr_user.id).first()
            self.curr_user = user
    
    def update_observers(self):
        for observer in self.observers:
            observer.update_user()

    
    def update_ranking(self):
        all_participants = UserCompetition.query.all()

        ranking_data = []
        for participant in all_participants:
            user_id = participant.user_id
            user_score = participant.score
            ranking_data.append({'user_id': user_id, 'score': user_score})

        ranking_data.sort(key=lambda x: x['score'], reverse=True)

        for rank, data in enumerate(ranking_data, start=1):
            user_id = data['user_id']
            user_score = data['score']

            user = User.query.get(user_id)
            if user:
                prev_rank = user.overall_rank
                user.overall_rank = rank

                if prev_rank != rank:
                    self.notify_observers(user_id, rank)

        db.session.commit()  

    def get_user_ranking(self, user_id):
        return self.users.get(user_id, {'rank': None, 'total_score': None})
    """
    
    def update_ranking(self):
        # Collect data for all competitions
        #self.update_users()
        #self.update_observers()
        
        ranking_data = []
        for competition in Competition.query.all():
            for participant in competition.participants:
                user_id = participant.user_id
                user_score = participant.score
                ranking_data.append({'user_id': user_id, 'score': user_score})

        # Calculate overall ranking based on the total score
        overall_ranking_data = {}
        for data in ranking_data:
            user_id = data['user_id']
            user_score = data['score']

            if user_id in overall_ranking_data:
                overall_ranking_data[user_id] += user_score
            else:
                overall_ranking_data[user_id] = user_score

        overall_ranking_data = sorted(overall_ranking_data.items(), key=lambda x: x[1], reverse=True)

        # Update the user's overall rank
        for rank, (user_id, total_score) in enumerate(overall_ranking_data, start=1):
            if user_id in self.users:
                prev_rank = self.users[user_id]['rank']
                self.users[user_id] = {'rank': rank, 'total_score': total_score}

                if prev_rank != rank:
                    self.notify_observers(user_id, rank)
            else:
                self.users[user_id] = {'rank': rank, 'total_score': total_score}
        

    def display_ranking(self):
        # Collect data for all competitions
        #self.update_users()
        #self.update_observers()
        
        ranking_data = []
        for competition in Competition.query.all():
            for participant in competition.participants:
                user_id = participant.user_id
                user_score = participant.score
                ranking_data.append({'user_id': user_id, 'score': user_score})

        # Calculate overall ranking based on the total score
        overall_ranking_data = {}
        for data in ranking_data:
            user_id = data['user_id']
            user_score = data['score']

            if user_id in overall_ranking_data:
                overall_ranking_data[user_id] += user_score
            else:
                overall_ranking_data[user_id] = user_score

        overall_ranking_data = sorted(overall_ranking_data.items(), key=lambda x: x[1], reverse=True)

        # Generates leaderboard
        results = []
        for rank, (user_id, total_score) in enumerate(overall_ranking_data, start=1):
            user = User.query.filter_by(id=user_id).first()
            results += {'username': user.username, 'rank': rank, 'total score': total_score}
        
        return results