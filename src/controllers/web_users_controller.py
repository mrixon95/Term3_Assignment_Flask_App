from models.User import User
from main import db, login_manager
from schemas.UserSchema import user_schema, user_schemas
from flask import (
    Blueprint, render_template, flash, redirect, url_for, abort, request)
from forms import RegistrationForm, LoginForm, DeleteButton, UpdateUserForm
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from main import bcrypt

web_users = Blueprint("web_users", __name__, url_prefix="/web")


@login_manager.user_loader
def load_user(username):
    if username is not None:
        return User.query.filter_by(username=username).first()
    return None


@login_manager.unauthorized_handler
def unauthorised():
    flash("You must be logged in to view this page")
    return redirect(url_for('web_users.web_users_login'))


@web_users.route("/register", methods=["GET", "POST"])
def web_users_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.dob.data)
        print(form.email.data)
        existing_user = User.query.filter_by(username=form.username.data).first()
        if not existing_user:
            new_user = User(username = form.username.data, first_name = form.first_name.data, last_name = form.last_name.data, dob = form.dob.data, email = form.email.data, mobile = form.mobile.data, city = form.city.data, country = form.country.data)

            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            # return redirect(url_for("web_profiles.show_profiles"))
        flash("Email already registered")
        return redirect(url_for("web_users.web_users_login"))
    return render_template("user_register.html", form=form)


@web_users.route("/login", methods=["GET", "POST"])
def web_users_login():
    if current_user.is_authenticated:
        return redirect(url_for("web_workhistory.show_workhistories"))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for("web_workhistory.show_workhistories"))
        flash("Invalid email and password")
        return redirect(url_for("web_users.web_users_login"))
    return render_template("user_login.html", form=form)


@web_users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("web_users.web_users_login"))


@web_users.route("/account", methods=["GET"])
@login_required
def get_user():

    user = load_user(current_user.get_id())

    if not user:
        return abort(401, description="Unauthorised to view this page")

    return render_template(
        "account_details.html",
        user=user)


@web_users.route("/account/update", methods=["GET", "POST"])
@login_required
def update_user():
    username = current_user.get_id()
    user = User.query.filter_by(username=username)

    form = UpdateUserForm(obj=user.first())
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if form.email.data != user.first().email and existing_user:
            return abort(401, description="Email already registered")
        else:
            data = {
                "first_name": form.first_name.data,
                "last_name": form.last_name.data,
                "dob": form.dob.data,
                "mobile": form.mobile.data,
                "city": form.city.data,
                "country": form.country.data
            }
            fields = user_schema.load(data, partial=True)
            user.update(fields)
            db.session.commit()
            flash("Account updated!")
            return redirect(url_for("web_users.get_user"))
    return render_template("user_update.html", form=form, user=user)


# @web_users.route("/account/delete", methods=["POST"])
# @login_required
# def delete_user():
#     form = DeleteButton()
#     if form.submit.data:
#         username = current_user.get_id()
#         user = User.query.filter_by(username=username)

#         profiles = Profile.query.filter_by(user_id=user.user_id)
#         for profile in profiles:
#             while len(profile.unrecommend) > 0:
#                 for item in profile.unrecommend:
#                     profile.unrecommend.remove(item)
#                 db.session.commit()

#         db.session.delete(user)
#         db.session.commit()
#         logout_user()
#         flash("Account deleted")
#         return redirect(url_for("web_users.web_users_login"))
#     return redirect(url_for("web_users.get_user"))