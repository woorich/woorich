from datetime import datetime
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect
from .auth_views import login_required
from app import db
from ..forms import ReplyForm
from app.models import Board, Reply

bp = Blueprint('reply', __name__, url_prefix='/reply')


@bp.route('/create/<int:board_no>', methods=('POST',))
@login_required
def create(board_no):  # URL 파라미터 명 변경
    form = ReplyForm()
    board = Board.query.get_or_404(board_no)  # 모델명 변경
    if form.validate_on_submit():
        content = request.form['r_content']
        reply = Reply(r_content=content, created_at=datetime.now(), user=g.user, board=board)  # 모델명 변경
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('board.detail', board_no=board_no))  # 라우트명 변경
    return render_template('board/board_detail.html', board=board, form=form)  # 템플릿 파일 경로 변경

@bp.route('/modify/<int:reply_id>', methods=('GET', 'POST'))
@login_required
def modify(reply_id):
    reply = Reply.query.get_or_404(reply_id)  # 모델명 변경
    if g.user != reply.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('board.detail', board_no=reply.board.no))  # 라우트명 변경
    if request.method == "POST":
        form = ReplyForm()
        if form.validate_on_submit():
            form.populate_obj(reply)
            reply.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('board.detail', board_no=reply.board.no))  # 라우트명 변경
    else:
        form = ReplyForm(obj=reply)
    return render_template('answer/answer_form.html', form=form)

@bp.route('/delete/<int:reply_id>')
@login_required
def delete(reply_id):
    reply = Reply.query.get_or_404(reply_id)  # 모델명 변경
    board_no = reply.board.no  # 모델명 변경
    if g.user != reply.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(reply)
        db.session.commit()
    return redirect(url_for('board.detail', board_no=board_no))  # 라우트명 변경