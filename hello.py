from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

class LoginForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    last_name = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    institution = StringField('Informe a sua Insituição de ensino:', validators=[DataRequired()])
    subject = SelectField(
        'Informe a sua disciplina:', 
        choices=[
            ('DSWA5', 'DSWA5'), 
            ('DSWA4', 'DSWA4'), 
            ('Gestão de projetos', 'Gestão de projetos')
        ], 
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user/<name>/<pront>/<inst>')
def user(name, pront, inst):
    return render_template('user.html', name=name, pront=pront, inst=inst)


@app.route('/contextorequisicao/<name>')
def contexto(name):
    return render_template(
        'contexto.html',
        name=name,
        user_agent=request.headers.get('User-Agent'),
        ip=request.remote_addr,
        host=request.host
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['last_name'] = form.last_name.data
        session['institution'] = form.institution.data
        session['subject'] = form.subject.data
        session['agent'] = request.headers.get('User-Agent')
        session['ip'] = request.remote_addr
        session['host'] = request.host
        return redirect(url_for('login'))
    return render_template('login.html', form=form, name=session.get('name'), last_name=session.get('last_name'), institution=session.get('institution'), subject=session.get('subject'), agent=session.get('agent'), ip=session.get('ip'), host=session.get('host'), current_time=datetime.utcnow())