from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from .. import db 
# from flask import current_app as app
from woorichApp.views.auth_views import login_required
from woorichApp.models import Board  # 모델명 변경
from woorichApp.forms import BoardForm, ReplyForm  # 폼명 변경

bp = Blueprint('board', __name__, url_prefix='/board')  # 블루프린트명 변경

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    board_list = Board.query.order_by(Board.created_at.desc())  # 모델명 변경
    board_list = board_list.paginate(page=page, per_page=10)
    return render_template('board/board_list.html', board_list=board_list)  # 템플릿 파일명 변경

@bp.route('/detail/<int:board_no>/')
def detail(board_no):  # 변수명 변경
    form = ReplyForm()  # 폼명 변경
    board = Board.query.get_or_404(board_no)  # 모델명 변경
    return render_template('board/board_detail.html', board=board, form=form)  # 템플릿 파일명 변경

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = BoardForm()  # 폼명 변경
    if request.method == 'POST' and form.validate_on_submit():
        board = Board(b_title=form.b_title.data, b_content=form.b_content.data, created_at=datetime.now(), user=g.user)  # 모델명 변경
        db.session.add(board)
        db.session.commit()
        return redirect(url_for('board._list'))  # 블루프린트명 변경
    return render_template('board/board_form.html', form=form)  # 템플릿 파일명 변경

@bp.route('/modify/<int:board_no>', methods=('GET', 'POST'))
@login_required
def modify(board_no):  # 변수명 변경
    board = Board.query.get_or_404(board_no)  # 모델명 변경
    if g.user != board.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('board.detail', board_no=board_no))  # 블루프린트명 변경
    if request.method == 'POST':
        form = BoardForm()  # 폼명 변경
        if form.validate_on_submit():
            form.populate_obj(board)
            db.session.commit()
            return redirect(url_for('board.detail', board_no=board_no))  # 블루프린트명 변경
    else:
        form = BoardForm(obj=board)  # 폼명 변경
    return render_template('board/board_form.html', form=form)  # 템플릿 파일명 변경

@bp.route('/delete/<int:board_no>')
@login_required
def delete(board_no):  # 변수명 변경
    board = Board.query.get_or_404(board_no)  # 모델명 변경
    if g.user != board.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('board.detail', board_no=board_no))  # 블루프린트명 변경
    db.session.delete(board)
    db.session.commit()
    return redirect(url_for('board._list'))  # 블루프린트명 변경
