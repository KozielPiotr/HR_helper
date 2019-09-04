"""Utilities for 'start_docs' routes"""

from sqlalchemy.exc import SQLAlchemyError

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


def change_start_doc_type_name(data):
    """
    Changes name of start document type
    :param data: dict with type's name before change and after change
    :return: True if successful and False if not
    """
    doc_type = StartDocType.query.filter_by(name=data["name"]).first()
    doc_type.name = data["changed"]
    try:
        db.session.add(doc_type)
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False


def delete_doctype(doctype_id):
    """
    Deletes given type of start document from database.
    Also removes every related StartDoc db objects
    :param doctype_id: id of doc type to be removed
    :return: True if successful and False if not
    """
    doctype = StartDocType.query.filter_by(id=doctype_id).first()
    try:
        db.session.delete(doctype)
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False
