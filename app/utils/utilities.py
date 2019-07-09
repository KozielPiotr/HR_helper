# pylint: disable=inconsistent-return-statements

"""Utilities used in whole project"""

from flask import redirect, url_for, flash


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
