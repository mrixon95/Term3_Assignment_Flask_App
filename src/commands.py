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
    from models.StudyHistory import StudyHistory
    from models.WorkHistory import WorkHistory
    from models.Certification import Certification
    from models.ResumeProject import ResumeProject
    from models.Meeting import Meeting
    from models.Message import Message
    from models.Connection import Connection
    from models.Post import Post
    from models.JobSalary import JobSalary
    from models.ITNews import ITNews
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
        user.username = f"test{i}"
        user.first_name = faker.first_name()
        user.last_name = faker.last_name()
        user.created_at = now.strftime('%Y-%m-%d %H:%M:%S')
        user.email = f"test{i}@gmail.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        user.mobile = faker.phone_number()
        user.city = faker.city()
        user.country = faker.country()
        user.dob = faker.date_of_birth()

        db.session.add(user)
        user_list.append(user)
    
    

    db.session.commit()

    studyhistory_list = []
    
    qualifications = ['bachelor', 'master', 'honours']
    institutions = ['rmit', 'latrobe', 'monash']
    for i in range(20):

        studyhistory = StudyHistory()
        studyhistory.username = choice(user_list).username

        studyhistory.qualification_title = choice(qualifications)
        studyhistory.institution = choice(institutions)
        studyhistory.city = faker.city()
        studyhistory.country = faker.country()
        studyhistory.date_start = faker.date_of_birth()
        studyhistory.date_end = faker.date_of_birth()

        db.session.add(studyhistory)
        studyhistory_list.append(studyhistory)


    db.session.commit()

    company = ['nab', 'aws', 'microsoft']
    job_title = ['engineer', 'developer', 'architect']
    for i in range(20):

        workhistory = WorkHistory()

        workhistory.username = choice(user_list).username

        workhistory.job_title = faker.job()
        workhistory.company = choice(company)
        workhistory.city = faker.city()
        workhistory.country = faker.country()
        workhistory.date_start = faker.date_of_birth()
        workhistory.date_end = faker.date_of_birth()

        db.session.add(workhistory)


    cert_names = ['aws cloud practitioner', 'microsoft azure administrator', 'microsoft excel']
    descriptions = ['Expert', 'Advanced', 'Beginner']
    issuers = ['Microsoft', 'AWS', 'Google']

    for i in range(20):

        certification = Certification()

        certification.username = choice(user_list).username

        certification.cert_name = choice(cert_names)
        certification.description = choice(descriptions)
        certification.issuer = choice(issuers)
        certification.date_obtained = faker.date_of_birth()

        db.session.add(certification)


    resume_paths_list = ['file1', 'file2', 'file3']
    github_account_list = ['https://github.com/mrixon95', 'https://github.com/HarryTranAU/', 'https://github.com/ashley190']


    for i in range(20):

        resumeproject = ResumeProject()

        resumeproject.username = choice(user_list).username

        resumeproject.resume_path = choice(resume_paths_list)
        resumeproject.github_account = choice(github_account_list)

        db.session.add(resumeproject)


    qualifications = ['bachelor', 'master', 'honours']
    institutions = ['rmit', 'latrobe', 'monash']


    for i in range(20):

        meeting = Meeting()
        meeting.username = choice(user_list).username

        meeting.time_start = faker.date_of_birth()
        meeting.time_end = faker.date_of_birth()
        meeting.location = faker.city()
        meeting.subject = faker.word()
        meeting.description = faker.word()
        meeting.last_updated = faker.date_of_birth()

        db.session.add(meeting)

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



    for i in range(5):

        post = Post()
        post.username = user_list[i % 5].username
        post.content = faker.text()
        post.last_updated = faker.date_of_birth()
        
        db.session.add(post)

    
    for i in range(5):

        jobsalary = JobSalary()
        jobsalary.title = faker.job()
        jobsalary.lower_quartile = faker.random_int(30, 50)
        jobsalary.median_salary = faker.random_int(70, 120)
        jobsalary.upper_quartile = faker.random_int(150, 500)
        jobsalary.average_years_experience = faker.random_int(1, 10)

        db.session.add(jobsalary)

    for i in range(5):

        ITnews = ITNews()
        ITnews.article_link = faker.url()
        ITnews.photo_link = faker.image_url()
        ITnews.published_time = faker.past_date()

        db.session.add(ITnews)



    db.session.commit()