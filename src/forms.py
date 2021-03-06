from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, SubmitField,
    PasswordField, SelectField, IntegerField, DateField)
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):


    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    dob = DateField('dob', validators=[DataRequired()])
    mobile = StringField('mobile', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    password = PasswordField(
        'password', validators=[DataRequired(), Length(min=2)])
    confirm = PasswordField(
        'confirm password', validators=[DataRequired(), EqualTo(
            'password', message='Passwords must match')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class UpdateUserForm(FlaskForm):
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    email = StringField('email')
    dob = DateField('dob')
    mobile = StringField('mobile')
    city = StringField('city')
    country = StringField('country')
    submit = SubmitField("Update Details")


class DeleteButton(FlaskForm):
    submit = SubmitField("Delete")


class CreateWorkHistory(FlaskForm):
    job_title = StringField("job_title", validators=[DataRequired(), Length(min=1)])
    company = StringField("company", validators=[DataRequired(), Length(min=1)])
    city = StringField("city", validators=[DataRequired(), Length(min=1)])
    country = StringField("country", validators=[DataRequired(), Length(min=1)])
    date_start = DateField("date_start", validators=[DataRequired()])
    date_end = DateField("date_end", validators=[DataRequired()])

    submit = SubmitField("Create Work History")

class CreateStudyHistory(FlaskForm):
    qualification_title = StringField("qualification_title", validators=[DataRequired(), Length(min=1)])
    institution = StringField("institution", validators=[DataRequired(), Length(min=1)])
    city = StringField("city", validators=[DataRequired(), Length(min=1)])
    country = StringField("country", validators=[DataRequired(), Length(min=1)])
    date_start = DateField("date_start", validators=[DataRequired()])
    date_end = DateField("date_end", validators=[DataRequired()])

    submit = SubmitField("Create Study History")


class UpdateWorkHistory(CreateWorkHistory):
    submit = SubmitField("Update Work History")

class UpdateStudyHistory(CreateWorkHistory):
    submit = SubmitField("Update Study History")


class UnrecommendButton(FlaskForm):
    submit = SubmitField("Unrecommend")


class RemoveButton(FlaskForm):
    submit = SubmitField("Remove")


