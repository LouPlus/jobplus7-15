from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for
from jobplus.models import Job,Dilivery,db
from flask_login import current_user,login_required


job = Blueprint('job',__name__,url_prefix='/job')

@job.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.order_by(Job.created_at.desc()).paginate(
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
        d = Dilivery(
                job_id=job.id,
                user_id=current_user.id
                )     # 创建Dilvery 表，记录投递简历记录
        db.session.add(d)    #数据 放入数据库
        db.session.commit()
        flash('投递成功','success')
    return redirect(url_for('job.detail',job_id=job.id)) #通过job.detail渲染，传入参数 
