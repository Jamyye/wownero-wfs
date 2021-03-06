from datetime import datetime
from flask import session, g

import settings
from wowfunding.bin.utils import Summary
from wowfunding.factory import app, db_session
from wowfunding.orm.orm import Proposal, User, Comment


@app.context_processor
def templating():
    from flask.ext.login import current_user
    recent_comments = db_session.query(Comment).filter(Comment.automated == False).order_by(Comment.date_added.desc()).limit(3).all()
    summary_data = Summary.fetch_stats()
    return dict(logged_in=current_user.is_authenticated,
                current_user=current_user,
                funding_categories=settings.FUNDING_CATEGORIES,
                funding_statuses=settings.FUNDING_STATUSES,
                summary_data=summary_data,
                recent_comments=recent_comments)


@app.before_request
def before_request():
    pass


@app.after_request
def after_request(res):
    if hasattr(g, 'wowfunding_prices'):
        delattr(g, 'wowfunding_prices')
    res.headers.add('Accept-Ranges', 'bytes')
    if settings.DEBUG:
        res.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        res.headers['Pragma'] = 'no-cache'
        res.headers['Expires'] = '0'
        res.headers['Cache-Control'] = 'public, max-age=0'
    return res


@app.teardown_appcontext
def shutdown_session(**kwargs):
    db_session.remove()


@app.errorhandler(404)
def error(err):
    return 'Error', 404
