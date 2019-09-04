"""Routes for start documents (main documents) section of main page"""

from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user

from app.models import StartDocType
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

    title = "HR - nowy rodzaj dokumentu głównego"

    form = NewStartDocTypeForm()
    if form.validate_on_submit():
        if start_docs_utils.add_start_doc_type(form) is False:
            flash("Taki dokument już istnieje")
        else:
            flash("{} - nowy rodzaj dokumentu utworzony pomyślnie".format(form.name.data))

    return render_template("start_docs/new_start_doc_type.html", title=title, form=form)


@bp.route("/list-start-doc-type", methods=["GET", "POST"])
@login_required
def list_start_doc_type():
    """
    Allows to change name of start document type
    :return: renders template with list of all start document types
    """
    required_role(current_user, "user")

    types = StartDocType.query.all()

    title = "HR - lista rodzajów dokumentóœ głównych"

    return render_template("start_docs/start_doc_types_list.html", title=title, types=types)


@bp.route("/edit-start-doc-type", methods=["GET", "POST"])
@login_required
def edit_start_doc_type():
    """
    Changes name of start document type
    :return: "OK" if successful and "ERROR" if not
    """
    required_role(current_user, "user")

    data = request.json

    if start_docs_utils.change_start_doc_type_name(data) is False:
        return "ERROR"
    return "OK"


@bp.route("/delete-start-doc-type/<doctype_id>", methods=["GET", "POST"])
@login_required
def delete_start_doc_type(doctype_id):
    """
    Deletes given type of start document
    :param doctype_id: id of doctype to be deleted
    :return: redirect back to list of start doc types (list_start_doc_type() function)
    """
    required_role(current_user, "user")

    if start_docs_utils.delete_doctype(doctype_id) is True:
        flash("Typ dokumentu usunięty")
    else:
        flash("Błąd. Upewnij się, że taki typ dokumentu istnieje. Ktoś mógł go usunąć w międzyczasie.")
    return redirect(url_for("start_docs.list_start_doc_type"))
