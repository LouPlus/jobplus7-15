from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from jobplus.decorators import admin_required, company_required
from jobplus.models import User, Company, Job, db
from jobplus.forms import RegisterForm, AddUserForm, AddCompanyForm

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

@admin.route('/users/adduser',methods=['GET','POST'])
@admin_required
def adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('求职者添加成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/adduser.html', form=form)

@admin.route('/users/addcompany',methods=['GET','POST'])
@admin_required
def addcompany():
    form = AddCompanyForm()
    if form.validate_on_submit():
        form.create_company()
        flash('公司添加成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/addcompany.html', form=form)

@admin.route('/users/edituser/<int:user_id>',methods=['GET','POST'])
@admin_required
def edituser(user_id):
    user = User.query.get_or_404(user_id)
    form = AddUserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户更新成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edituser.html',form=form,user=user)

@admin.route('/users/editcompany/<int:company_id>',methods=['GET','POST'])
@admin_required
def editcompany(company_id):
    company = Company.query.get_or_404(company_id)
    form = AddCompanyForm(obj=company)
    if form.validate_on_submit():
        form.update_company(company)
        flash('企业更新成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/editcompany.html',form=form,company=company)

@admin.route('/users/<int:user_id>/<action>')
@admin_required
def useraction(user_id,action):
    user = User.query.get_or_404(user_id)
    if str(action) == 'disable':
        user.is_disable=True
    if (action) == 'enable':
        user.is_disable=False
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users'))

@admin.route('/jobs')
@admin_required
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/jobs.html',pagination=pagination)
