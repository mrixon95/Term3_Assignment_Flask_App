from controllers.UserStudyHistory_controller import userstudyhistory
from controllers.UserWorkHistory_controller import userworkhistory
from controllers.UserCertification_controller import usercertification
from controllers.UserResumeProject_controller import userresumeproject
from controllers.UserMeeting_controller import usermeeting
from controllers.Message_controller import message
from controllers.User_controller import user

registerable_controllers = [
    user,
    userstudyhistory,
    userworkhistory,
    usercertification,
    userresumeproject,
    usermeeting,
    message
]