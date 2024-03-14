from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    sobrenome = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    instituicao = StringField('Informe a sua Instituição de ensino:', validators=[DataRequired()])
    disciplina = SelectField('Informe a sua disciplina:', choices=['DSWA5','DSWA4', 'Gestão de Projetos'],validators=[DataRequired()])
    submit = SubmitField('Enviar')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  user = request.headers.get('User-Agent')
  ip = request.remote_addr
  host = request.host
  if form.validate_on_submit():
    old_name = session.get('name')
    session['name'] = form.name.data
    session['sobrenome'] = form.sobrenome.data
    session['instituicao'] = form.instituicao.data
    session['disciplina'] = form.disciplina.data
    if old_name != session['name']:
      flash('Você alterou o seu nome!')
    return redirect(url_for('index'))
  return render_template('index.html',
                         form=form,
                         name=session.get('name'),
                         sobrenome=session.get('sobrenome'),
                         instituicao=session.get('instituicao'),
                         disciplina=session.get('disciplina'), user=user,ip=ip,host=host, current_time=datetime.utcnow())

