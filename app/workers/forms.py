"""Forms for Worker section"""

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired


class NewWorkerForm(FlaskForm):
    """Form for new worker"""

    name = StringField("Imię i nazwisko", validators=[DataRequired()])
    contract_begin = DateField("Początek umowy", validators=[DataRequired()], format="%d.%m.%Y",
                               render_kw={"placeholder": "dd.mm.rrrr"})
    contract_end = DateField("Koniec umowy", validators=[DataRequired()], format="%d.%m.%Y",
                             render_kw={"placeholder": "dd.mm.rrrr"})
    function = SelectField("Stanowisko")
    workplace = SelectField("Dział")
    submit = SubmitField("Wprowadź")
