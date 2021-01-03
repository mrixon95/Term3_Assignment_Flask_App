from flask import (
    Blueprint, render_template, redirect, url_for, flash, abort)
from flask_login import current_user, login_required
from controllers.web_users_controller import load_user
from models.StudyHistory import StudyHistory
from schemas.StudyHistorySchema import study_history_schema
from schemas.StudyHistorySchema import study_history_schemas

from forms import (
    CreateStudyHistory, UpdateStudyHistory, DeleteButton,
    UnrecommendButton, RemoveButton)
from main import db

web_studyhistory = Blueprint("web_studyhistory", __name__, url_prefix="/web/web_studyhistory")


@web_studyhistory.route("/", methods=["GET"])
@login_required
def show_studyhistories():
    user = load_user(current_user.get_id())
    studyhistories = StudyHistory.query.filter_by(username=user.username)

    form = DeleteButton()
    return render_template("studyhistory.html", studyhistories=studyhistories, form=form)


@web_studyhistory.route("/create", methods=["GET", "POST"])
@login_required
def create_studyhistory():
    user = load_user(current_user.get_id())

    if not user:
        return abort(401, description="Unauthorised to view this page")

    form = CreateStudyHistory()

    if form.validate_on_submit():
        new_studyhistory = StudyHistory()
        new_studyhistory.username = user.username
        new_studyhistory.qualification_title = form.qualification_title.data
        new_studyhistory.institution = form.institution.data
        new_studyhistory.city = form.city.data
        new_studyhistory.country = form.country.data
        new_studyhistory.date_start = form.date_start.data
        new_studyhistory.date_end = form.date_end.data

        db.session.add(new_studyhistory)
        db.session.commit()
        flash("studyhistory added!")
        return redirect(url_for("web_studyhistory.show_studyhistories"))

    return render_template("create_studyhistory.html", form=form)


@web_studyhistory.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_studyhistory(id):
    user = load_user(current_user.get_id())
    studyhistory = StudyHistory.query.filter_by(id=id, username=user.username)

    if studyhistory.count() != 1:
        flash("Can't find studyhistory")
        return redirect(url_for("web_studyhistory.show_studyhistories"))

    form = UpdateStudyHistory(obj=studyhistory.first())
    if form.validate_on_submit():
        data = {
            "job_title": form.job_title.data,
            "company": form.company.data,
            "city": form.city.data,
            "country": form.country.data,
            "date_start": form.date_start.data,
            "date_end": form.date_end.data,

        }
        fields = study_history_schema.load(data, partial=True)
        studyhistory.update(fields)
        db.session.commit()
        flash("studyhistory updated!")
        return redirect(url_for("web_studyhistory.show_studyhistories"))

    return render_template("update_studyhistory.html", form=form, id=id)


@web_studyhistory.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_studyhistory(id):
    form = DeleteButton()
    if form.submit.data:
        user = load_user(current_user.get_id())
        studyhistory = StudyHistory.query.filter_by(id=id).first()

        if not studyhistory:
            flash("No studyhistory found")
            return redirect(url_for("web_studyhistory.show_studyhistories"))

        db.session.delete(studyhistory)
        db.session.commit()

        flash("studyhistory deleted")
        return redirect(url_for("web_studyhistory.show_studyhistories"))


@web_studyhistory.route("/<int:id>", methods=["GET"])
@login_required
def view_studyhistory(id):
    user = load_user(current_user.get_id())

    studyhistory = StudyHistory.query.filter_by(id=id).first()

    if not studyhistory:
        flash("studyhistory not found")
        return redirect(
            url_for("web_studyhistory.view_studyhistory", id=studyhistory.id))

    form1 = UnrecommendButton()
    form2 = RemoveButton()

    return render_template(
        "view_studyhistory.html",
        studyhistory=studyhistory, form1=form1, form2=form2)
