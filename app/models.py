#-*- coding: utf-8 -*-
# pylint: disable=missing-docstring, too-few-public-methods, no-member, invalid-name

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db, login


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship("Role", secondary="user_roles")
    events = db.relationship("Event", backref="user", cascade="all")

    def __repr__(self):
        return "{}".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def assign_role(self, role):
        self.roles.append(role)

    def assign_event(self, event):
        self.events.append(event)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "{}".format(self.name)


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id", ondelete="CASCADE"))


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer(), primary_key=True)
    begin = db.Column(db.DateTime, index=True, nullable=False, default=datetime.now())
    end = db.Column(db.DateTime, default=datetime.now())
    delivered = db.Column(db.Boolean, default=False)
    event_kind_id = db.Column(db.Integer, db.ForeignKey("event_kind.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "{}\t{}\t{}\t{}".format(self.event_kind, self.begin, self.end,
                                       User.query.filter_by(id=self.user_id).first())


class EventKind(db.Model):
    __tablename__ = "event_kind"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False, unique=True)
    events = db.relationship("Event", backref="event_kind", cascade="all")

    def __repr__(self):
        return "{}".format(self.name)

    def set_kind(self, event):
        self.events.append(event)
