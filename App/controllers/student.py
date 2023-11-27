from App.models import Student, Competition, competition_student
from App.database import db

def create_student(username, password):
    student = get_student_by_username(username)
    if student:
        print(f'{username} already exists!')
        return None

    newStudent = Student(username=username, password=password)
    try:
        db.session.add(newStudent)
        db.session.commit()
        print(f'New Student: {username} created!')
        return newStudent
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json

def update_student(id, username):
    student = get_student(id)
    if student:
        student.username = username
        try:
            db.session.add(student)
            db.session.commit()
            print("Username was updated!")
            return student
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

#still needs adjusting (everything below)

def get_ranked_users():
    return Student.query.order_by(Student.ranking.asc()).all()

"""def register_student(student_id, comp_id):

    student = get_student(student_id)
    comp = Competition.query.get(comp_id)

    student_comp = CompetitionStudent.query.filter_by(student_id=student.id, comp_id=comp.id).first()
    if student_comp:
        return False
        
    if user and comp:
        user_comp = UserCompetition(user_id=user.id, comp_id=comp.id, rank = rank)
        try:
            db.session.add(user_comp)
            db.session.commit()
            return True
        except Exception as e:
            print("FAILURE")
            db.session.rollback()
            return False
            
        print("success")
        

    return 'Error adding user to competition'"""

def register_student(username, competition_name):
  student = get_student_by_username(username)
  if student:
    competition = Competition.query.filter_by(name=competition_name).first()
    if competition:
      return student.participate_in_competition(competition)
    else:
      print(f'{competition_name} was not found')
      return None
  else:
    print(f'{username} was not found')
    return None

"""
def get_user_competitions(user_id):
    user = User.query.get(user_id)
    
    
    if user:
        userComps = user.competitions
        competitions = [Competition.query.get(inst.comp_id) for inst in userComps]
    # print(competitions)
        if competitions:
            results =  [c.toDict() for c in competitions] 
            return results
        else:
            return competitions
    return ("User not Found")
"""




# def update_ranks():
#   users = User.query.order_by(User.rank.asc()).limit(20).all()
  
#   # Store current ranks
#   ranks = {u.id: u.rank for u in users}
  
#   # Update ranks
#   db.session.query(User).update({User.rank: User.rank + 1})  
#   db.session.commit()

#   # Check if ranks changed
#   for u in users:
#     if u.rank != ranks[u.id]:
#       send_notification(u, f"Your rank changed from {ranks[u.id]} to {u.rank}")
    

def get_user_rankings(user_id):
    users = User.query.get(user_id)
    userComps = users.competitions

    ranks = [UserCompetition.query.get(a.id).toDict() for a in userComps]
    return ranks
    
def display_user_info(username):
    student = get_student_by_username(username)

    if not student:
        return None
    else:
        score = get_points(student.id)
        student.set_points(score)
        profile_info = {
            "profile": student.get_json(),
            "participated_competitions": [comp.name for comp in student.competitions]
        }
        return profile_info