from flask import Blueprint, render_template, current_app, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from jobplus.decorators import company_required
from jobplus.models import Job, db, Delivery
from jobplus.forms import AddJobForm

job = Blueprint('job',__name__,url_prefix='/job')

@job.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    #filter_by过滤下架的职位
    pagination = Job.query.filter_by(up=True).order_by(Job.created_at.desc()).paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('job/index.html', pagination=pagination, active='job')


# 为职位详情添加路由
@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job, active='')


#为配置
#添加简历投递路由
@job.route('/<int:job_id>/apply') #按下路由时，URL 传入job_id
@login_required     # 登录状态下
def apply(job_id):   
    job = Job.query.get_or_404(job_id)  #从表Job中查找 Job
    if job.current_user_is_applied:   # 判断用户是否投递简历
        flash('已投递过该职位','warning')   
    else:
        d = Delivery(
                job_id=job.id,
                user_id=current_user.id
                )     # 创建Dilvery 表，记录投递简历记录
        db.session.add(d)    #数据 放入数据库
        db.session.commit()
        flash('投递成功','success')
    return redirect(url_for('job.detail',job_id=job.id)) #通过job.detail渲染，传入参数 

#职位上下线功能
@job.route('/<int:job_id>/<action>')
@company_required
def jobaction(job_id,action):
    #根据职位id创建job实例
    job = Job.query.get_or_404(job_id)
    #判别当前访问用户是否合法
    if current_user.is_company and not current_user.id == job.company_id:
        abort(404)
    #根据action修改job实例中的up状态
    if str(action) == 'disable':
        job.up=False
    if str(action) == 'enable':
        job.up=True
    db.session.add(job)
    db.session.commit()
    #当前访问用户为管理员时，返回管理员的职位管理页面
    if current_user.is_admin:
        return redirect(url_for('admin.jobs'))
    #当前访问用户为企业用户时，返回企业的职位管理页面
    if current_user.is_company:
        return redirect(url_for('job.admin'))

#企业职位管理
@job.route('/admin')
@company_required
def admin():
    if current_user.is_admin:
        flash('Please login with company account','info')
        return redirect(url_for('admin.index'))
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(company_id=current_user.id).paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )
    return render_template('job/admin.html', pagination=pagination)

#企业新增职位
@job.route('/new',methods=['GET','POST'])
@company_required
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        form.create_job(company=current_user)
        flash('职位添加成功','success')
        return redirect(url_for('job.admin'))
    return render_template('job/addjob.html', form=form)

#企业编辑职位
@job.route('/<int:job_id>/edit',methods=['GET','POST'])
@company_required
def editjob(job_id):
    job = Job.query.get_or_404(job_id)
    #判断当前用户是否合法
    if not current_user.id == job.company_id:
        abort(404)
    form = AddJobForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash('职位更新成功','success')
        return redirect(url_for('job.admin'))
    return render_template('job/editjob.html',form=form,job=job)

#企业删除职位
@job.route('/<int:job_id>/delete')
@company_required
def deletejob(job_id):
    job = Job.query.get_or_404(job_id)
    #判断当前用户是否合法
    if not current_user.id == job.company_id:
        abort(404)
    db.session.delete(job)
    db.session.commit()
    flash('职位删除成功','success')
    return redirect(url_for('job.admin'))

#企业简历管理-未审核列表
@job.route('/apply/todolist')
@company_required
def todolist():
    page = request.args.get('page', default=1, type=int)
    #筛选当前企业用户所属未审核简历
    pagination = Delivery.query.filter((Delivery.company_id == current_user.id) & (Delivery.status == 1)).paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )
    return render_template('job/todolist.html',pagination=pagination)

#企业建立管理-简历操作
@job.route('/apply/<int:deliv_id>/<action>')
@company_required
def delivaction(deliv_id,action):
    deliv = Delivery.query.get_or_404(deliv_id)
    #判断当前用户是否合法
    if deliv.job.company_id != current_user.id:
        abort(404)
    #根据action不同，进行不同操作
    if str(action) == 'reject':
        deliv.status = 2
        flash('简历拒绝成功','success')
    if str(action) == 'interview':
        deliv.status = 3
        flash('简历进入面试成功','success')
    db.session.add(deliv)
    db.session.commit()
    return redirect(url_for('job.todolist'))

#企业简历管理-面试列表
@job.route('/apply/interviewlist')
@company_required
def interviewlist():
    page = request.args.get('page', default=1, type=int)
    #筛选当前企业用户所属面试简历
    pagination = Delivery.query.filter((Delivery.company_id == current_user.id) & (Delivery.status == 3)).paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )
    return render_template('job/interviewlist.html',pagination=pagination)

#企业简历管理-不合适列表
@job.route('/apply/rejectlist')
@company_required
def rejectlist():
    page = request.args.get('page', default=1, type=int)
    #筛选当前企业用户所属未审核简历
    pagination = Delivery.query.filter((Delivery.company_id == current_user.id) & (Delivery.status == 2)).paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )
    return render_template('job/rejectlist.html',pagination=pagination)
