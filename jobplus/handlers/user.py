from flask import Blueprint,redirect,render_template,url_for,flash
from jobplus.forms import UserProfileForm
from flask_login import login_required,current_user

user = Blueprint('user',__name__,url_prefix='/user')

@user.route('/profile',methods=['GET','POST'])
@login_required #引入flask_login，login_required装饰器保护路由
def profile():
    form = UserProfileForm(obj=current_user)
    #UserProfileForm 传入一个User对象,Form中显示相应数据
    #login_user后，创建了current_user,是一个User对象

    if form.validate_on_submit():
        form.updata_profile(current_user)
        #form.updata_profile，传入一个User对象，修改参数，上传给数据库
        flash('个人信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html',form=form)
