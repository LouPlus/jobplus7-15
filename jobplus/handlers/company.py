from flask import Blueprint,flash,redirect,url_for,render_template, current_app, request
from flask_login import login_required,current_user
from jobplus.forms import CompanyProfileForm
from jobplus.models import Company, Job,User

company = Blueprint('company',__name__,url_prefix='/company')

#企业用户登录后，信息完善
@company.route('/profile',methods=['GET','POST'])
@login_required  
def profile():
    if not current_user.is_company:
        flash('您不是企业用户','warning')
        return redirect(url_for('front.index'))
    form = CompanyProfileForm(obj=current_user.company,
                              username=current_user.username,
                              email=current_user.email)
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('企业信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html',form=form)

@company.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Company.query.order_by(Company.created_at.desc()).paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('company/index.html', pagination=pagination, active='company')

@company.route('/<int:company_id>')
def detail(company_id):
    panel = request.args.get('panel','about')
    company = User.query.get_or_404(company_id)
    if not company.is_company:
        about(404)
    return render_template('company/detail.html',company=company,panel=panel)
