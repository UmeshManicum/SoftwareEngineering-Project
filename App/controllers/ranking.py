from App.models import Student, Ranking, competition_student
from App.database import db

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
            
            ranking.set_ranking(curr_rank)
            ranking.update_state()
            rank = ranking.state.notify()
            #if rank:
            #    #create a notification
            db.session.add(rank)
            db.session.commit()
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

            student = Student.query.filter_by(id=ranking.student_id)
            leaderboard.append({"rank": ranking.curr_rank, "student": student.username, "points": ranking.total_points})
            count += 1
        return leaderboard