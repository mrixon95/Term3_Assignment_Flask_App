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
    from main import bcrypt
    from faker import Faker
    import random

    from datetime import datetime

    now = datetime.now()

    faker = Faker()
    users = []

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
        users.append(user)

    db.session.commit()
    
    qualifications = ['bachelor', 'master', 'honours']
    institutions = ['rmit', 'latrobe', 'monash']
    for i in range(20):

        userstudyhistory = UserStudyHistory()
        userstudyhistory.username = random.choice(users).username
        userstudyhistory.qualification_title = random.choice(qualifications)
        userstudyhistory.institution = random.choice(institutions)
        userstudyhistory.city = faker.city()
        userstudyhistory.country = faker.country()
        userstudyhistory.date_start = faker.date_of_birth()
        userstudyhistory.date_end = faker.date_of_birth()

        db.session.add(userstudyhistory)


    db.session.commit()

    company = ['nab', 'aws', 'microsoft']
    job_title = ['engineer', 'developer', 'architect']
    for i in range(20):

        userworkhistory = UserWorkHistory()

        userworkhistory.username = random.choice(users).username
        userworkhistory.job_title = random.choice(job_title)
        userworkhistory.company = random.choice(company)
        userworkhistory.city = faker.city()
        userworkhistory.country = faker.country()
        userworkhistory.date_start = faker.date_of_birth()
        userworkhistory.date_end = faker.date_of_birth()
    
        db.session.add(userworkhistory)


        
    db.session.commit()
    print("Tables seeded")