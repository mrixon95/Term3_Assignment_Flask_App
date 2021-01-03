from flask import (
    Blueprint, render_template, redirect, url_for, flash, abort)
from flask_login import current_user, login_required
from controllers.web_users_controller import load_user
from models.WorkHistory import WorkHistory
from schemas.WorkHistorySchema import work_history_schema
from schemas.WorkHistorySchema import work_history_schemas

from forms import (
    CreateWorkHistory, UpdateWorkHistory, DeleteButton,
    UnrecommendButton, RemoveButton)
from main import db

web_workhistory = Blueprint("web_workhistory", __name__, url_prefix="/web/web_workhistory")


@web_workhistory.route("/", methods=["GET"])
@login_required
def show_workhistories():
    user = load_user(current_user.get_id())
    workhistories = WorkHistory.query.filter_by(username=user.username)

    form = DeleteButton()
    return render_template("workhistory.html", workhistories=workhistories, form=form)


@web_workhistory.route("/create", methods=["GET", "POST"])
@login_required
def create_workhistory():
    user = load_user(current_user.get_id())

    if not user:
        return abort(401, description="Unauthorised to view this page")

    form = CreateWorkHistory()
    print(form.job_title)
    print(form.city)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        new_workhistory = WorkHistory()
        new_workhistory.username = user.username
        new_workhistory.job_title = form.job_title.data
        new_workhistory.company = form.company.data
        new_workhistory.city = form.city.data
        new_workhistory.country = form.country.data
        new_workhistory.date_start = form.date_start.data
        new_workhistory.date_end = form.date_end.data

        db.session.add(new_workhistory)
        db.session.commit()
        flash("workhistory added!")
        return redirect(url_for("web_workhistory.show_workhistories"))

    return render_template("create_workhistory.html", form=form)


@web_workhistory.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_workhistory(id):
    user = load_user(current_user.get_id())
    workhistory = WorkHistory.query.filter_by(id=id, username=user.username)

    if workhistory.count() != 1:
        flash("Can't find workhistory")
        return redirect(url_for("web_workhistory.show_workhistories"))

    form = UpdateWorkHistory(obj=workhistory.first())
    if form.validate_on_submit():
        data = {
            "job_title": form.job_title.data,
            "company": form.company.data,
            "city": form.city.data,
            "country": form.country.data,
            "date_start": form.date_start.data,
            "date_end": form.date_end.data,

        }
        fields = work_history_schema.load(data, partial=True)
        workhistory.update(fields)
        db.session.commit()
        flash("workhistory updated!")
        return redirect(url_for("web_workhistory.show_workhistories"))

    return render_template("update_workhistory.html", form=form, id=id)


@web_workhistory.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_workhistory(id):
    form = DeleteButton()
    if form.submit.data:
        user = load_user(current_user.get_id())
        workhistory = WorkHistory.query.filter_by(id=id).first()

        if not workhistory:
            flash("No workhistory found")
            return redirect(url_for("web_workhistory.show_workhistories"))

        db.session.delete(workhistory)
        db.session.commit()

        flash("workhistory deleted")
        return redirect(url_for("web_workhistory.show_workhistories"))


@web_workhistory.route("/<int:id>", methods=["GET"])
@login_required
def view_workhistory(id):
    user = load_user(current_user.get_id())

    workhistory = WorkHistory.query.filter_by(id=id).first()

    if not workhistory:
        flash("workhistory not found")
        return redirect(
            url_for("web_workhistory.view_workhistory", id=workhistory.id))

    form1 = UnrecommendButton()
    form2 = RemoveButton()

    return render_template(
        "view_workhistory.html",
        workhistory=workhistory, form1=form1, form2=form2)
