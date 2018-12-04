from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
#from wtforms import DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired,Optional

class LoginForm(FlaskForm):
    #Variables for /index form
    lat_long = StringField('Latitude,Longitude', validators=[DataRequired()])
    radius = StringField('Radius (meters)', validators=[DataRequired()])
    live_only = BooleanField('Live Videos Only',false_values=(False, 'false', 0, '0'))
    pub_after = DateField('Published After',format='%Y-%m-%d',validators=[Optional()])  #2018-09-26
    pub_before = DateField('Published Before',format='%Y-%m-%d', validators=[Optional()])
    keyword = StringField('Keyword(s)',validators=[Optional()])
    submit = SubmitField('Submit')

class SearchDateForm(FlaskForm):
    #Variables for /index2 form
    pub_after = DateField('Published After',format='%Y-%m-%d', validators=[DataRequired()])  #2018-09-26
    pub_before = DateField('Published Before',format='%Y-%m-%d', validators=[DataRequired()])
    keyword = StringField('Keyword(s)', validators=[DataRequired()])
    live_only = BooleanField('Live Videos Only',false_values=(False, 'false', 0, '0'))
    submit = SubmitField('Submit')

class SearchLiveForm(FlaskForm):
    #Variables for /index3 form
    keyword = StringField('Keyword(s)',validators=[DataRequired()])
    submit = SubmitField('Submit')