from flask import Flask, request, session, redirect, url_for, render_template, flash
from models import User
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = 'static/uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(username) < 1:
            flash('Username must be at least one character.')
        elif len(password) < 5:
            flash('Password must be at least 5 characters.')
        elif not User(username).register(password):
            flash('Username already exists.')
        else:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            flash('Please provide required details')
        elif not User(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['username'] = username
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        date_posted = datetime.now().strftime('%Y-%m-%d')
        if not title:
            flash('You must give your post a title.')
        elif not content:
            flash('You must give your post at least one tag.')
        else:
            if image:
            	image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            User(session['username']).add_post(
                title, content, image.filename, date_posted)
        return redirect(url_for('index'))
    return render_template('add_post.html')


@app.route('/index', methods=['GET'])
def index():
	posts = User.get_posts()
	return render_template('home.html', posts=posts)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('login'))

@app.route('/images/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)
