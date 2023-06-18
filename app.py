from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///times.sqlite'

db = SQLAlchemy(app)


class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    fundacao = db.Column(db.String(10))

    def __init__(self, nome, cidade, fundacao):
        self.nome = nome
        self.cidade = cidade
        self.fundacao = fundacao

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/adicionar", methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        cidade = request.form['cidade']
        fundacao = request.form['fundacao']

        novo_time = Time(nome, cidade, fundacao)
        db.session.add(novo_time)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('adicionar.html')

@app.route("/listar")
def listar():
    times = Time.query.all()
    return render_template('listar.html', times=times)

@app.route("/editar/<int:time_id>", methods=['GET', 'POST'])
def editar(time_id):
    time = Time.query.get(time_id)

    if request.method == 'POST':
        time.nome = request.form['nome']
        time.cidade = request.form['cidade']
        time.fundacao = request.form['fundacao']

        db.session.commit()
        return redirect(url_for('listar'))

    return render_template('editar.html', time=time)

@app.route("/excluir/<int:time_id>")
def excluir(time_id):
    time = Time.query.get(time_id)
    db.session.delete(time)
    db.session.commit()
    return redirect(url_for('listar'))

if __name__ == '__main__':
    app.run(debug=True)