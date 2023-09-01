from flask import Blueprint, redirect, render_template, request, session, flash, url_for, jsonify, g
from flask_login import login_required, current_user
from woorichApp import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..forms import UserUpdateForm

bp = Blueprint('mypage', __name__)

# 나의 정보 페이지
@bp.route('/mypage', methods=['GET','POST'])
def mypage():
    user = g.user
    return render_template('mypage/mypage.html', user=user)

# https://github.com/YeonjiKim0316/flask_0711_1/blob/main/app/views/question_views.py 의 modify(question_id) 함수 참조  
@bp.route('/update_user_info/<string:user_id>', methods=['GET', 'POST'])
@login_required
def update_user_info(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    print(user)
    if g.user != user.user_id:
        flash('로그인 해주세요.')
        return redirect(url_for('mypage/mypage.html', user_id=user_id))
    if request.method == 'POST':
        form = UserUpdateForm()
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            return redirect(url_for('mypage/mypage.html', user_id=user_id))
    else: # GET 요청
        form = UserUpdateForm(obj=user)
    return render_template('mypage/mypage.html', form=form)

    # data = request.json
    # user = g.user
    # if not user:
    #     return jsonify({"message": "User not found"}), 404

    # if data.get('password'):
    #     user.user_pw = generate_password_hash(data['password'])
    # user.email = data.get('email', user.email)
    # user.phone = data.get('phone', user.phone)
    # user.address = data.get('address', user.address)

    # db.session.commit()
    # return jsonify({"message": "계정 정보가 수정되었습니다."})