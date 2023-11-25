import click, pytest, sys
from flask import Flask
from datetime import datetime

from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    #create_student('bob', 'bobpass')
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
student_cli = AppGroup('student', help='Student object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@student_cli.command("create", help="Creates a student")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass")
def create_student_command(username, password):
    student = create_student(username, password)

@student_cli.command("update", help="Updates a student's username")
@click.argument("id", default="1")
@click.argument("username", default="rob")
def update_student_command(id, username):
    student = update_student(id, username)

# this command will be : flask user create bob bobpass

@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_students_command(format):
    if format == 'string':
        print(get_all_students())
    else:
        print(get_all_students_json())

app.cli.add_command(student_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))





@test.command("competition", help = 'Testing Competition commands')
@click.argument("type", default="all")
def competition_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "CompUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "CompIntegrationTests"]))
    else:
        print("deafult input, no test ran")




app.cli.add_command(test)


'''
Competition commands
'''

comps = AppGroup('comp', help = 'commands for competition')   

@comps.command("add", help = 'add new competition')
@click.argument("name", default = "Coding Comp")
@click.argument("location", default = "Port of Spain")
def add_comp(name, location):
    response = create_competition(name, location)
    if response:
        print("Competition Created Successfully")
    else:
        print("error adding comp")





@comps.command("get", help = "list all competitions")
def get_comps():
    print(get_all_competitions())

@comps.command("get_json", help = "list all competitions")
def get_comps():
    print(get_all_competitions_json())


@comps.command("add_user")
@click.argument("user_id")
@click.argument("comp_id")
@click.argument("rank")
def add_to_comp(user_id, comp_id, rank):
    add_user_to_comp(user_id, comp_id, rank)
    print("Done!")


@comps.command("getUserComps")
@click.argument("user_id")
def getUserCompetitions(user_id):
    competitions = get_user_competitions(user_id)
    print("these are the competitions")
    # print(competitions)

@comps.command("findcompuser")
@click.argument("user_id")
@click.argument("comp_id")
def find_comp_user(user_id, comp_id):
    findCompUser(user_id, comp_id)

@comps.command("getCompUsers")
@click.argument("comp_id")
def get_comp_users(comp_id):
    get_competition_users(comp_id)




app.cli.add_command(comps)