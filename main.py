from flask import Flask, render_template, redirect
from data import db_session
from data.__all_models import Jobs, User
import datetime
from forms.user import RegisterForm, LoginForm
from forms.jobs import AddJobForm
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def create_job():
    db_sess = db_session.create_session()
    job = Jobs(team_leader=1, job='deployment of residential modules 1 and 2', work_size=15, collaborators='2, 3',
               start_date=datetime.datetime.now(), is_finished=False)
    db_sess.add(job)
    db_sess.commit()


def main():
    db_session.global_init("db/mars.db")
    # create_job()
    app.run()


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    return render_template('journal.html', title='Works Log',
                           jobs=db_sess.query(Jobs).all())


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            for password in [form.password, form.password_again]:
                password.errors.append("Passwords are not matched!")
            return render_template('register.html', title='Registration', form=form)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            form.email.errors.append("The user is already registered!")
            return render_template('register.html', title='Registration',
                                   form=form)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            age=form.age.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        form.password.errors.append("Password is not correct!")
        return render_template('login.html', form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob',  methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.job_title.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Adding a Job', form=form)


if __name__ == '__main__':
    main()
