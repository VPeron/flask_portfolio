import hashlib

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required #, current_user


from app.password_profiler import password_profiler_bp
#from app.models import User
from app.password_profiler.models import StrengthChecker


@password_profiler_bp.route('/')
@login_required
def pass_profiler_dashboard():

    return render_template('pass_profiler_index.html', title="Password Profiler")

@password_profiler_bp.route('/check', methods=['GET', 'POST'])
@login_required
def check_password_strength():
    if request.method == 'POST':
        password = request.form.get('password')
        if not password:
            #TODO: error template with back button not displaying
            flash('Invalid username or password')
            return redirect(url_for('password_profiler.check_password_strength'))

        checker = StrengthChecker(password)
        report = checker.run()
    
        return render_template(
            'check_password.html', 
            title="Password Profiler", 
            password=hashlib.sha256(password.encode()).hexdigest(), 
            strength=report
            )
    return render_template('check_password.html', title="Password Profiler")