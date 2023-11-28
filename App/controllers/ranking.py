from App.models import Student, Ranking, competition_student
from App.database import db

def create_ranking(student_id):
    newRanking = Ranking(student_id)
    try:
        db.session.add(newRanking)
        db.session.commit()
        #print(f'New Student: {username} created!')
        return newRanking
    except Exception as e:
        db.session.rollback()
        #print(f'Something went wrong creating {username}')
        return None

def get_ranking(id):
    ranking = Ranking.query.filter_by(student_id=id).first()
    return ranking.curr_ranking

def sort_rankings(ranking):
    return ranking.total_points

def update_rankings():
    rankings = Ranking.query.all()
    count = 1
    if rankings:
        rankings.sort(key=sort_rankings,reverse=True)
        curr_high = rankings[0].total_points
        curr_rank = 1
        for ranking in rankings:
            if curr_high != ranking.total_points:
                curr_rank = count
                curr_high = ranking.total_points
            #print(ranking.get_json())
            ranking.set_ranking(curr_rank)
            ranking.update_state()
            db.session.add(ranking)
            db.session.commit()
            rank = ranking.state.notify()
            #if rank:
            #    #create a notification
            #db.session.add(rank)
            #db.session.commit()
            count += 1

def display_rankings():
    rankings = Ranking.query.all()
    if not rankings:
        print("No Rankings found!")
        return None
    else:
        leaderboard = []
        count = 1
        rankings.sort(key=sort_rankings,reverse=True)
        curr_high = rankings[0].total_points
        curr_rank = 1
        for ranking in rankings:
            if curr_high != ranking.total_points:
                curr_rank = count
                curr_high = ranking.total_points

            student = Student.query.filter_by(id=ranking.student_id).first()
            leaderboard.append({"student": student.username, "ranking":ranking.get_json()})
            #leaderboard.append({"rank": ranking.curr_ranking, "student": student.username, "points": ranking.total_points})
            count += 1
        return leaderboard