from app import app, db
from models import User, Tweet, followers
from forms import RegistrationForm, LoginForm, TweetForm
from flask import render_template, redirect, url_for, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import  login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form, logged_in_user=current_user)

@app.route('/login', methods =['GET','POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()        
        
        if not user:
            return render_template('index.html', form=form, message='login failed', logged_in_user=current_user)
        
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            return redirect(url_for('profile'))
        
        return render_template('index.html', form=form, message='login failed')
    return render_template('index.html', form=form)

@app.route('/profile', defaults={'username' : None})
@app.route('/profile/<username>')
@login_required
def profile(username):
    
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
    else:
        user = current_user

    tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()

    current_time =  get_current_time()

    followed_by = user.followed_by.all()

    display_follow = True
    
    if current_user == user:
        display_follow = False
    elif current_user in followed_by:
        display_follow = False

    who_to_watch = who_to_watch_list(user)

    return render_template('profile.html', current_user=user, tweets=tweets, current_time=current_time, followed_by=followed_by, display_follow=display_follow, who_to_watch=who_to_watch, logged_in_user=current_user)

def who_to_watch_list(user):
    return User.query.filter(User.id != user.id).order_by(db.func.random()).limit(4).all()

def get_current_time():
    return datetime.now()

@app.route('/timeline', defaults={'username' : None})
@app.route('/timeline/<username>')
def timeline(username):
    form = TweetForm()

    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
        
        tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()
        total_tweets = len(tweets)
        
    else:
        user = current_user
        tweets = Tweet.query.join(followers, (followers.c.followee_id == Tweet.user_id)).filter(followers.c.follower_id == current_user.id).order_by(Tweet.date_created.desc()).all()
        total_tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).count()

    current_time =  get_current_time()

    followed_by_count = user.followed_by.count()

    who_to_watch = who_to_watch_list(user)

    return render_template('timeline.html', form=form, tweets=tweets, current_time=current_time, current_user=user, total_tweets=total_tweets, who_to_watch=who_to_watch, logged_in_user=current_user, followed_by_count=followed_by_count)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        image_filename = secure_filename(form.image.data.filename)
        image_path = os.path.join(app.root_path, 'static/images', image_filename)
        form.image.data.save(image_path)
        image_url = url_for('static', filename='images/' + image_filename)
        
        new_user = User(name=form.name.data, username=form.username.data, image=image_url, password=generate_password_hash(form.password.data), join_date=datetime.now())
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('profile'))
    
    return render_template('register.html', form=form,  logged_in_user=current_user)

@app.route('/post_tweet',  methods=['POST'])
@login_required
def post_tweet():

    form = TweetForm()

    if form.validate():
        tweet =  Tweet(user_id=current_user.id, text=form.text.data, date_created=datetime.now())
        db.session.add(tweet)
        db.session.commit()
        
        return redirect(url_for('timeline'))
        
    return 'someting is wrong'

@app.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    
    current_user.following.append(user_to_follow)
    
    db.session.commit()

    return redirect(url_for('profile'))