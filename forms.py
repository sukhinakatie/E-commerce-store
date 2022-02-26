from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email


# форма для валидации данных при чекауте
# все поля, кроме other, должны быть заполнены (InputRequired)
# а в поле для email должна быть строка, напоминающая email
class CheckoutForm(FlaskForm):
    first_name = StringField(validators=[InputRequired()])
    surname = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired(), Email()])
    address = StringField(validators=[InputRequired()])
    other = StringField()
