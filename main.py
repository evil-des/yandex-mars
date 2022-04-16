from flask import Flask, render_template
from data import db_session
from data.__all_models import Jobs
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

session = None


def create_job():
    job = Jobs(team_leader=1, job='deployment of residential modules 1 and 2', work_size=15, collaborators='2, 3',
               start_date=datetime.datetime.now(), is_finished=False)
    session.add(job)
    session.commit()


def main():
    global session
    db_session.global_init("db/mars.db")
    session = db_session.create_session()
    create_job()
    app.run()


@app.route('/')
@app.route('/index')
def index():
    return render_template('journal.html', title='Works Log',
                           jobs=session.query(Jobs).all())


if __name__ == '__main__':
    main()
