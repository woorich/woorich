from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class BoardForm(FlaskForm):
    b_title = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    b_content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class ReplyForm(FlaskForm):
    r_content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    user_id = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    username = StringField('실명', validators=[DataRequired(), Length(max=25)])
    user_pw1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('user_pw2', '비밀번호가 일치하지 않습니다')])
    user_pw2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    phone = StringField('전화번호', validators=[DataRequired()])
    address = StringField('주소', validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    user_id = StringField('사용자이름', validators=[DataRequired(), Length(min=5, max=25)])
    user_pw = PasswordField('비밀번호', validators=[DataRequired()])

class UserUpdateForm(FlaskForm):
    user_id = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    username = StringField('실명', validators=[DataRequired(), Length(max=25)])
    user_pw1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('user_pw2', '비밀번호가 일치하지 않습니다')])
    user_pw2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    phone = StringField('전화번호', validators=[DataRequired()])
    address = StringField('주소', validators=[DataRequired()])

class UserDeleteForm(FlaskForm):
    pass