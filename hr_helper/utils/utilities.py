"""Utilities used in whole project"""

from sqlalchemy.exc import SQLAlchemyError
from flask import redirect, url_for, flash
from flask_script import Command

from hr_helper.app import db
from hr_helper.models import User, Role


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


class SuperUser(Command):
    """
    Creates user with administrator role
    """
    def run(self):
        try:
            admin = User(username="admin")
            admin.set_password("a")
            admin_role = Role(name="role")
            user_role = Role(name="user")
            admin.assign_role(admin_role)
            admin.assign_role(user_role)
            db.session.add_all([admin, admin_role, user_role])
            db.session.commit()
        except:
            print("admin user already exist")


def try_add_db_record(record):
    """
    Tries to add record to database
    :param record: given record
    :return: True if successful and False if not
    """
    try:
        db.session.add(record)
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False


def try_del_db_record(record):
    """
    Tries to delete record from database
    :param record: given record
    :return: True if successful and False if not
    """
    try:
        db.session.delete(record)
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False

