from flask import Flask, render_template, redirect
from data import db_session
from data.__all_models import Jobs, User
import datetime
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def create_job():
    db_sess = db_session.create_session()
    job = Jobs(team_leader=1, job='deployment of residential modules 1 and 2', work_size=15, collaborators='2, 3',
               start_date=datetime.datetime.now(), is_finished=False)
    db_sess.add(job)
    db_sess.commit()


def main():
    db_session.global_init("db/mars.db")
    create_job()
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


if __name__ == '__main__':
    main()
