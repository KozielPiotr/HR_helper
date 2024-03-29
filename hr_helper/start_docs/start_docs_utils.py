"""Utilities for 'start_docs' routes"""

from hr_helper.app import db
from hr_helper.models import StartDocType
from hr_helper.utils.utilities import try_add_db_records, try_del_db_records


def add_start_doc_type(form):
    """
    Adds new type of start document to database
    :param form: filled form with name of new document type
    :return: True if record added successfully and False if not
    """
    doctype_name = form.name.data
    if doctype_name in [doc.name for doc in StartDocType.query.all()]:
        return False
    new_doc_type = StartDocType(name=doctype_name)
    db.session.add(new_doc_type)
    db.session.commit()
    return True


def change_start_doc_type_name(data):
    """
    Changes name of start document type
    :param data: dict with type's name before change and after change
    :return: True if successful and False if not
    """
    doc_type = StartDocType.query.filter_by(name=data["name"]).first()
    doc_type.name = data["changed"]

    return try_add_db_records([doc_type])


def remove_start_doctype(doctype_id):
    """
    Deletes given type of start document from database.
    Also removes every related StartDoc db objects
    :param doctype_id: id of doc type to be removed
    :return: True if successful and False if not
    """
    doctypes = StartDocType.query.filter_by(id=doctype_id).first()

    return try_del_db_records([doctypes])
