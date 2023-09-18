from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from .. import db 
from app.views.auth_views import login_required
from app.models import Board
from app.forms import BoardForm, ReplyForm

bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    board_list = Board.query.order_by(Board.created_at.desc())
    board_list = board_list.paginate(page=page, per_page=10)
    return render_template('board/board_list.html', board_list=board_list)

@bp.route('/detail/<int:board_no>/')
def detail(board_no):
    form = ReplyForm()
    board = Board.query.get_or_404(board_no)
    return render_template('board/board_detail.html', board=board, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = BoardForm()
    if request.method == 'POST' and form.validate_on_submit():
        board = Board(b_title=form.b_title.data, b_content=form.b_content.data, created_at=datetime.now(), user=g.user)
        db.session.add(board)
        db.session.commit()
        return redirect(url_for('board._list'))
    return render_template('board/board_form.html', form=form)

@bp.route('/modify/<int:board_no>', methods=('GET', 'POST'))
@login_required
def modify(board_no):
    board = Board.query.get_or_404(board_no)
    if g.user != board.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('board.detail', board_no=board_no))
    if request.method == 'POST':
        form = BoardForm()
        if form.validate_on_submit():
            form.populate_obj(board)
            db.session.commit()
            return redirect(url_for('board.detail', board_no=board_no))
    else:
        form = BoardForm(obj=board)
    return render_template('board/board_form.html', form=form)

@bp.route('/delete/<int:board_no>')
@login_required
def delete(board_no):
    board = Board.query.get_or_404(board_no)
    if g.user != board.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('board.detail', board_no=board_no))
    db.session.delete(board)
    db.session.commit()
    return redirect(url_for('board._list'))
