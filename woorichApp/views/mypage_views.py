from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from flask_login import login_required, current_user
#from .\models import Note, User
from .. import db

bp = Blueprint('mypage', __name__)

# 나의 정보 페이지
@bp.route('/mypage', methods=['GET','POST'])
def mypage():
    return render_template('mypage/mypage.html')


# 나의 정보 수정 페이지
# @mypage_views.route('/mypage/update', methods=['GET','POST'])
# @login_required
# def mypage_update():
#     return render_template('mypage_update.html')