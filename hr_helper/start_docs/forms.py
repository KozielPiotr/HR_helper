"""Forms for start documents section"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NewStartDocTypeForm(FlaskForm):
    """Form for creating new type of starting document"""

    name = StringField("Nazwa dokumentu", validators=[DataRequired()])
    submit = SubmitField("Zatwierdź")
