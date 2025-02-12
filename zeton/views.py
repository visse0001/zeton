from flask import Blueprint, render_template, abort, g, get_flashed_messages

from . import auth
from zeton.data_access import users, prizes, tasks, points

bp = Blueprint('views', __name__)


@bp.route('/')
@auth.login_required
def index():
    role = g.user_data['role']
    logged_user_id = g.user_data['id']

    template = None
    context = {}

    if role == 'caregiver':
        children = users.get_caregivers_children(logged_user_id)
        template = 'index_caregiver.html'

        context.update({"firstname": g.user_data['firstname'],
                        "role": role,
                        "children": children})

    elif role == 'child':

        template = 'index_child.html'
        child = users.get_child_data(logged_user_id)
        child_points = points.get_child_points(child['id'])
        childs_tasks = tasks.get_tasks(logged_user_id)
        childs_prizes = prizes.get_prizes(logged_user_id)
        context = {'child': child, 'child_points': child_points, 'childs_tasks': childs_tasks,
                   'childs_prizes': childs_prizes}

    messages = get_flashed_messages()

    return render_template(template, **context, messages=messages)


@bp.route('/child/<child_id>')
@auth.login_required
@auth.caregiver_only
def child(child_id):
    child = users.get_child_data(child_id)
    childs_tasks = tasks.get_tasks(child_id)
    childs_prizes = prizes.get_prizes(child_id)
    role = g.user_data['role']
    child_points = points.get_child_points(child['id'])

    context = {'child': child,
               'childs_tasks': childs_tasks,
               'childs_prizes': childs_prizes,
               'role': role,
               'child_points': child_points}

    messages = get_flashed_messages()

    return render_template('caregiver_panel.html', **context, messages=messages)


@bp.route('/task_detail/<child_id>')
@auth.login_required
@auth.logged_child_or_caregiver_only
def task_detail(child_id):
    child = users.get_child_data(child_id)
    childs_tasks = tasks.get_tasks(child_id)
    childs_points_history = points.get_points_history(child_id)
    role = g.user_data['role']
    child_points = points.get_child_points(child['id'])

    context = {'child': child,
               'childs_tasks': childs_tasks,
               'childs_points_history': childs_points_history,
               'role': role,
               'child_points': child_points
               }

    return render_template('task_detail.html', **context)


@bp.route('/settings/')
@auth.login_required
def user_settings():
    return render_template('user_settings.html')


@bp.route('/settings/password')
@auth.login_required
def password_change():
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)

    context = {'user_data': user_data}
    messages = get_flashed_messages()

    return render_template('password_change.html', **context, messages=messages)


@bp.route('/settings/firstname')
@auth.login_required
def firstname_change():
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)

    context = {'user_data': user_data}
    messages = get_flashed_messages()

    return render_template('firstname_change.html', **context, messages=messages)


@bp.route('/prizes_detail/<child_id>')
@auth.login_required
@auth.logged_child_or_caregiver_only
def prizes_detail(child_id):
    role = g.user_data['role']

    try:
        child = users.get_child_data(child_id)
    except TypeError:
        return abort(403)

    childs_prizes = prizes.get_prizes(child_id)
    child_points = points.get_child_points(child['id'])

    context = {'child': child,
               'childs_prizes': childs_prizes,
               'role': role,
               'child_points': child_points}

    return render_template('prizes_detail.html', **context)


@bp.route('/school_points_detail/<child_id>')
@auth.login_required
@auth.logged_child_or_caregiver_only
def school_points_detail(child_id):
    role = g.user_data['role']

    try:
        child = users.get_child_data(child_id)
    except TypeError:
        return abort(403)
    child_points = points.get_child_points(child['id'])

    context = {'child': child,
               'role': role,
               'child_points': child_points}

    return render_template('school_points_detail.html', **context)


@bp.route('/bans_detail/<child_id>')
@auth.login_required
@auth.logged_child_or_caregiver_only
def bans_detail(child_id):
    role = g.user_data['role']

    try:
        child = users.get_child_data(child_id)
    except TypeError:
        return abort(403)
    child_points = points.get_child_points(child['id'])

    context = {'child': child,
               'role': role,
               'child_points': child_points}

    return render_template('bans_detail.html', **context)
