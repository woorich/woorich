from flask import Blueprint, redirect, render_template, request, session, flash, url_for, jsonify, g
from app.views.auth_views import login_required
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..forms import UserUpdateForm

bp = Blueprint('mypage', __name__)

# 나의 정보 페이지
@bp.route('/mypage', methods=['GET','POST'])
def mypage():
    user = g.user
    form = UserUpdateForm(obj=user) # form 객체 생성
    return render_template('mypage/mypage.html', user=user, form=form)

# https://github.com/YeonjiKim0316/flask_0711_1/blob/main/app/views/question_views.py 의 modify(question_id) 함수 참조  
@bp.route('/update_user_info/<user_id>', methods=['GET', 'POST'])
@login_required
def update_user_info(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    form = UserUpdateForm(obj=user)
    
    if g.user.user_id != user.user_id:
        flash('로그인 해주세요.')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            return redirect(url_for('mypage.mypage', user_id=user.user_id, form=form))
    else: # GET 요청
        form = UserUpdateForm(obj=user)
    return render_template('mypage/mypage.html', user=user, form=form)

@bp.route('/scrap_list/<user_id>', methods=['GET','POST'])
def scrap_list(user_id):
    user = g.user
    return render_template('mypage/scrap_list.html', user=user)