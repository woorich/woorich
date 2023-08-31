from flask import Blueprint, redirect, render_template, request, session, flash, url_for, jsonify, g
from flask_login import login_required, current_user
from woorichApp import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('mypage', __name__)

# 나의 정보 페이지
@bp.route('/mypage', methods=['GET','POST'])
def mypage():
    user = g.user
    return render_template('mypage/mypage.html', user=user)

@bp.route('/update_user_info', methods=['POST'])
@login_required
def update_user_info():
    data = request.json
    user = g.user
    if not user:
        return jsonify({"message": "User not found"}), 404

    if data.get('password'):
        user.user_pw = generate_password_hash(data['password'])
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)

    db.session.commit()
    return jsonify({"message": "계정 정보가 수정되었습니다."})
