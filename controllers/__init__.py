from controllers.StudyHistory_controller import studyhistory
from controllers.WorkHistory_controller import workhistory
from controllers.Certification_controller import certification
from controllers.ResumeProject_controller import resumeproject
from controllers.Meeting_controller import meeting
from controllers.Message_controller import message
from controllers.User_controller import user
from controllers.Connection_controller import connection
from controllers.Post_controller import post

registerable_controllers = [
    user,
    studyhistory,
    workhistory,
    certification,
    resumeproject,
    meeting,
    message,
    connection,
    post
]