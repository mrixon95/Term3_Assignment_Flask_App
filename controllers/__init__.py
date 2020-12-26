from controllers.auth_controller import auth
from controllers.UserStudyHistory_controller import userstudyhistory
from controllers.UserWorkHistory_controller import userworkhistory
from controllers.UserCertification_controller import usercertification
from controllers.UserResumeProject_controller import userresumeproject
from controllers.UserMeeting_controller import usermeeting
from controllers.User_controller import user

registerable_controllers = [
    auth,
    userstudyhistory,
    userworkhistory,
    usercertification,
    userresumeproject,
    usermeeting
]