"""Utilities used in whole project"""

from sqlalchemy.exc import SQLAlchemyError
from flask import redirect, url_for, flash
from flask_script import Command

from hr_helper.app import db
from hr_helper.models import User, Role, Worker, Workplace, Function


def required_role(user, *roles):
    """
    Checks if user has proper role to get access to content
    :param user: current_user object
    :param roles: strings with names of roles demanded to access rest of route
    :return: redirects to main page if user has not assigned required role
    """
    common = list(set(roles).intersection([str(role) for role in user.roles]))
    if not common:
        flash("Brak dostępu")
        return redirect(url_for("main.index"))


class SamplePopulate(Command):
    """
    Creates user with administrator role and sample records from other tables
    """
    def run(self):
        try:
            admin = User(username="admin")
            admin.set_password("a")

            admin_role = Role(name="role")
            user_role = Role(name="user")

            admin.assign_role(admin_role)
            admin.assign_role(user_role)

            worker_1 = Worker(name="Sample Worker 1", working=True)
            worker_2 = Worker(name="Sample Worker 2", working=True)
            worker_3 = Worker(name="Sample Worker 3", working=False)

            workplace_1 = Workplace(name="Sample workplace 1")
            workplace_2 = Workplace(name="Sample workplace 2")
            
            workplace_1.set_workplace(worker_1)
            workplace_1.set_workplace(worker_2)
            workplace_2.set_workplace(worker_3)

            worker_3.workplace_id = workplace_2.id

            function_1 = Function(name="Sample function 1")
            function_2 = Function(name="Sample function 2")

            function_1.set_function(worker_1)
            function_1.set_function(worker_3)
            function_2.set_function(worker_2)

            db.session.add_all([admin, admin_role, user_role, worker_1, worker_2, worker_3, workplace_1, workplace_2,
                                function_1, function_2])
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            print("\nAdding sample records failed.\nProbably duplicated entries.\n")


def try_add_db_records(records):
    """
    Tries to add records to database
    :param records: list of given records
    :return: True if successful and False if not
    """
    try:
        for record in records:
            db.session.add(record)
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False


def try_del_db_records(records):
    """
    Tries to delete records from database
    :param records: list of given records
    :return: True if successful and False if not
    """
    try:
        for record in records:
            db.session.delete(record)
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False
