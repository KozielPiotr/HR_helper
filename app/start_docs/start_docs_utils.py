"""Utilities for 'start_docs' routes"""

from app import db
from app.models import StartDocType


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
