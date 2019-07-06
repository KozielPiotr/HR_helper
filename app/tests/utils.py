import json

from app import db


def create(db_item):
    db.session.add(db_item)
    db.session.commit()
    return db_item


def delete(db_item):
    db.session.delete(db_item)
    db.session.commit()

