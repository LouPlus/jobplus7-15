from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from jobplus.decorators import admin_required
from jobplus.models import User, Company, db
from jobplus.forms import RegisterForm

admin = Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/admin_base.html')

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html',pagination=pagination)