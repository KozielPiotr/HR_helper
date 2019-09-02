"""Routes for start documents (main documents) section of main page"""

from flask import render_template, flash
from flask_login import login_required, current_user

from app.start_docs import bp
from app.utils.utilities import required_role
from app.start_docs.forms import NewStartDocTypeForm
from app.start_docs import start_docs_utils


@bp.route("/new-start-doc-type", methods=["GET", "POST"])
@login_required
def new_start_doc_type():
    """
    Allows to create new type of main document (eg. job contract)
    :return: renders template with form for new start doc type
    """
    required_role(current_user, "user")

    title = "HR - nowy rodzaj dokumentu"

    form = NewStartDocTypeForm()
    if form.validate_on_submit():
        if start_docs_utils.add_start_doc_type(form) is False:
            flash("Taki dokument już istnieje")
        else:
            flash("{} - nowy rodzaj dokumentu utworzony pomyślnie".format(form.name.data))

    return render_template("start_docs/new_start_doc_type.html", title=title, form=form)
