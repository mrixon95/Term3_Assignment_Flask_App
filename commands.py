from main import db
from flask import Blueprint

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("wisdom")
def wisdom():
    print("Hello World")

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():

    from models.User import User
    from models.UserStudyHistory import UserStudyHistory
    from models.UserWorkHistory import UserWorkHistory
    from models.UserCertification import UserCertification
    from models.UserResumeProject import UserResumeProject
    from models.UserMeeting import UserMeeting
    from models.Message import Message
    from models.Connection import Connection
    from main import bcrypt
    from faker import Faker
    from random import randrange, choice

    from datetime import datetime

    now = datetime.now()

    faker = Faker()
    user_list = []

    # Create fake users

    for i in range(5):
        user = User()
        user.username = faker.word()
        user.first_name = faker.first_name()
        user.last_name = faker.last_name()
        user.created_at = now.strftime('%Y-%m-%d %H:%M:%S')
        user.email = faker.free_email()
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        user.mobile = faker.phone_number()
        user.city = faker.city()
        user.country = faker.country()
        user.dob = faker.date_of_birth()

        db.session.add(user)
        user_list.append(user)
    
    

    db.session.commit()

    userstudyhistory_list = []
    
    qualifications = ['bachelor', 'master', 'honours']
    institutions = ['rmit', 'latrobe', 'monash']
    for i in range(20):

        userstudyhistory = UserStudyHistory()
        userstudyhistory.username = choice(user_list).username

        userstudyhistory.qualification_title = choice(qualifications)
        userstudyhistory.institution = choice(institutions)
        userstudyhistory.city = faker.city()
        userstudyhistory.country = faker.country()
        userstudyhistory.date_start = faker.date_of_birth()
        userstudyhistory.date_end = faker.date_of_birth()

        db.session.add(userstudyhistory)
        userstudyhistory_list.append(userstudyhistory)


    db.session.commit()

    company = ['nab', 'aws', 'microsoft']
    job_title = ['engineer', 'developer', 'architect']
    for i in range(20):

        userworkhistory = UserWorkHistory()

        userworkhistory.username = choice(user_list).username

        userworkhistory.job_title = choice(job_title)
        userworkhistory.company = choice(company)
        userworkhistory.city = faker.city()
        userworkhistory.country = faker.country()
        userworkhistory.date_start = faker.date_of_birth()
        userworkhistory.date_end = faker.date_of_birth()

        db.session.add(userworkhistory)


    cert_names = ['aws cloud practitioner', 'microsoft azure administrator', 'microsoft excel']
    descriptions = ['Expert', 'Advanced', 'Beginner']
    issuers = ['Microsoft', 'AWS', 'Google']

    for i in range(20):

        usercertification = UserCertification()

        usercertification.username = choice(user_list).username

        usercertification.cert_name = choice(cert_names)
        usercertification.description = choice(descriptions)
        usercertification.issuer = choice(issuers)
        usercertification.date_obtained = faker.date_of_birth()

        db.session.add(usercertification)


    resume_paths_list = ['file1', 'file2', 'file3']
    github_account_list = ['https://github.com/mrixon95', 'https://github.com/HarryTranAU/', 'https://github.com/ashley190']


    for i in range(20):

        userresumeproject = UserResumeProject()

        userresumeproject.username = choice(user_list).username

        userresumeproject.resume_path = choice(resume_paths_list)
        userresumeproject.github_account = choice(github_account_list)

        db.session.add(userresumeproject)


    qualifications = ['bachelor', 'master', 'honours']
    institutions = ['rmit', 'latrobe', 'monash']


    for i in range(20):

        usermeeting = UserMeeting()
        usermeeting.username = choice(user_list).username

        usermeeting.time_start = faker.date_of_birth()
        usermeeting.time_end = faker.date_of_birth()
        usermeeting.location = faker.city()
        usermeeting.subject = faker.word()
        usermeeting.description = faker.word()
        usermeeting.last_updated = faker.date_of_birth()

        db.session.add(usermeeting)

    db.session.commit()


    for i in range(5):

        message = Message()
        message.username_of_sender = user_list[i].username
        message.username_of_receiver = user_list[(i + 1) % 5].username
        message.content = faker.text()

        db.session.add(message)

    
    for i in range(5):

        connection = Connection()
        connection.username_of_requester = user_list[i % 5].username
        connection.username_of_confirmer = user_list[(i + 3) % 5].username
        connection.user_1_approved = True
        connection.user_2_approved = True
        connection.status = "confirmed"

        db.session.add(connection)


    db.session.commit()