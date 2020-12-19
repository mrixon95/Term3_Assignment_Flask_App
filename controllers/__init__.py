from controllers.auth_controller import auth
from controllers.UserStudyHistory_controller import userstudyhistory
from controllers.UserWorkHistory_controller import userworkhistory
from controllers.User_controller import user

registerable_controllers = [
    auth,
    userstudyhistory,
    userworkhistory,
    user
]