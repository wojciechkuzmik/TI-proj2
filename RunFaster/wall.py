from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from RunFaster.auth import login_required
from RunFaster.db import get_db
import json

bp = Blueprint('wall', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    runs = db.execute(
        'SELECT id, user_id, created, dist, h, m, s, speed'
        ' FROM runs WHERE user_id = ?'
        ' ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()

    speedArray = []
    dateArray = []
    totalDist = 0
    for run in runs:
        speedArray.append(round(run['speed'], 1))
        dateArray.append(f"{run['created'].year}/{run['created'].month}/{run['created'].day}")
        totalDist += float(run['dist'])

    speedArray.reverse()
    dateArray.reverse()

    return render_template('wall/index.html', runs=runs, speedArray=speedArray, dateArray=dateArray, totalDist=totalDist)

    
@bp.route('/synchronize', methods=('POST',))
@login_required
def synchronize():
    data = json.loads(request.form['javascript_data'])
    h = int(data['h'])
    m = int(data['m'])
    s = int(data['s'])
    distance = float(data['dist'])
    error = None

    if h < 0 or m < 0 or s < 0 or h + m + s is 0 or m >= 60 or s >= 60:
        error = 'Time error.'

    if distance <= 0:
        error = 'Distance error.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
        'INSERT INTO runs (user_id, dist, h, m, s)'
        ' VALUES (?, ?, ?, ?, ?)',
        (g.user['id'], distance, h, m, s)
        )
        db.commit()
    flash("Możesz teraz odświeżyć stronę")
    return redirect(url_for('wall.index'))




@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        h = int(request.form['hours'])
        m = int(request.form['minutes'])
        s = int(request.form['seconds'])
        distance = float(request.form['distance'])
        error = None


        if h < 0 or m < 0 or s < 0 or h + m + s is 0 or m >= 60 or s >= 60:
            error = 'Time error.'

        if distance <= 0:
            error = 'Distance error.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO runs (user_id, dist, h, m, s)'
                ' VALUES (?, ?, ?, ?, ?)',
                (g.user['id'], distance, h, m, s)
            )
            db.commit()
            return redirect(url_for('wall.index'))

    return render_template('wall/create.html')


def get_run(id):
    run = get_db().execute(
        'SELECT id, user_id, dist, h, m, s'
        ' FROM runs'
        ' WHERE id = ? AND user_id = ?',
        (id, g.user['id'],)
    ).fetchone()

    if run is None:
        abort(404, "Run id {0} doesn't exist.".format(id))

    if run['user_id'] != g.user['id']:
        abort(403)

    return run


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    run = get_run(id)

    if request.method == 'POST':
        h = int(request.form['hours'])
        m = int(request.form['minutes'])
        s = int(request.form['seconds'])
        distance = float(request.form['distance'])
        error = None


        if h < 0 or m < 0 or s < 0 or h + m + s is 0 or m >= 60 or s >= 60:
            error = 'Time error.'

        if distance <= 0:
            error = 'Distance error.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE runs SET dist = ?, h = ?, m = ?, s = ?'
                ' WHERE id = ?',
                (distance, h, m, s, id)
            )
            db.commit()
            return redirect(url_for('wall.index'))

    return render_template('wall/update.html', run=run)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_run(id)
    db = get_db()
    db.execute('DELETE FROM runs WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('wall.index'))