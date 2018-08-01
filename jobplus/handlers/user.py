from flask import Blueprint,redirect,render_template,url_for,flash
from jobplus.forms import UserProfileForm
from flask_login import login_required,current_user

user = Blueprint('user',__name__,url_prefix='/user')

@user.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = UserProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.updata_profile(current_user)
        flash('个人信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html',form=form)
