from flask import request, redirect, flash, render_template, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from main import db, app
from main.models import Phonebook, User
from main.validation import validate_name, validate_number, validate_email


@app.route('/data/phonebook/post_record', methods=['POST'])
@login_required
def post_record():
    name = request.form.get('name')
    number = request.form.get('number')
    email = request.form.get('email')
    info = request.form.get('info')

    if validate_name(name) and validate_number(number) and validate_email(email):
        current_user.records.append(Phonebook(name, number, email, info))
        db.session.commit()

    return redirect(url_for('phonebook'))


@app.route('/data/phonebook/get_record', methods=['POST'])
@login_required
def get_record():
    id = request.form.get('record_id')
    if not id:
        return redirect(url_for('phonebook'))

    phonebook = Phonebook.query.get(id)

    if phonebook.user_id != current_user.id:
        flash('You are not allowed to edit this record')
        return redirect(url_for('phonebook'))

    return render_template('phonebook.html',
                           records=[phonebook, None])


@app.route('/data/phonebook/put_record', methods=['POST'])
@login_required
def put_record():
    id = request.form.get('record_id')
    if not id:
        return redirect(url_for('phonebook'))

    phonebook = Phonebook.query.get(id)

    if phonebook.user_id != current_user.id:
        flash('You are not allowed to edit this record')
        return redirect(url_for('phonebook'))

    name = request.form.get('name')
    number = request.form.get('number')
    email = request.form.get('email')
    info = request.form.get('info')

    if validate_name(name) and validate_number(number) and validate_email(email):
        phonebook.name = name
        phonebook.number = number
        phonebook.email = email
        phonebook.info = info
        db.session.commit()

    return redirect(url_for('phonebook'))


@app.route('/data/phonebook/delete_record', methods=['POST'])
@login_required
def delete_record():
    id = request.form.get('record_id')
    if not id:
        return redirect(url_for('phonebook'))

    phonebook = Phonebook.query.get(id)

    if phonebook.user_id != current_user.id:
        flash('You are not allowed to delete this record')
        return redirect(url_for('phonebook'))

    db.session.delete(phonebook)
    db.session.commit()
    return redirect(url_for('phonebook'))


@app.route('/phonebook', methods=['GET'])
@login_required
def phonebook():
    return render_template('phonebook.html', records=current_user.records)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login_ = request.form['login']
        password = request.form['password']
        password_retype = request.form['password-retype']

        if not (login_ and password and password_retype):
            flash('All fields are required')
        elif password != password_retype:
            flash('Passwords do not match')
        else:
            hash_pwd = generate_password_hash(password)
            db.session.add(User(login_, hash_pwd))
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_ = request.form['login']
        password = request.form['password']

        if login_ and password:
            user = User.query.filter_by(login=login_).first()

            if user and check_password_hash(user.password, password):
                login_user(user)

                if 'next' in request.args:
                    return redirect(request.args['next'])

                return redirect(url_for('phonebook'))
            else:
                flash('Login or password is incorrect')
        else:
            flash('Fill login and password fields')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response
