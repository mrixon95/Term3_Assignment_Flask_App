from controllers.StudyHistory_controller import studyhistory
from controllers.WorkHistory_controller import workhistory
from controllers.Certification_controller import certification
from controllers.ResumeProject_controller import resumeproject
from controllers.Meeting_controller import meeting
from controllers.Message_controller import message
from controllers.User_controller import user
from controllers.Connection_controller import connection
from controllers.Post_controller import post
from controllers.ITNews_controller import itnews
from controllers.JobSalary_controller import jobsalary
from controllers.Image_controller import image
from controllers.web_users_controller import web_users
from controllers.web_workhistory_controller import web_workhistory
from controllers.web_studyhistory_controller import web_studyhistory

registerable_controllers = [
    user,
    studyhistory,
    workhistory,
    certification,
    resumeproject,
    meeting,
    message,
    connection,
    post,
    jobsalary,
    itnews,
    web_users,
    web_workhistory,
    web_studyhistory,
    image
]