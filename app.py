import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/820 G3/OneDrive/Desktop/Twitter/engage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.template_filter('time_since')
def time_since(delta):
    seconds = delta.total_seconds()

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        return '%dd' %  (days)
    elif hours > 0:
        return '%dh' % (hours)
    elif minutes > 0:
        return '%dm' % (minutes)
    else:
        return 'just now'

from views import  *

if __name__ == '__main__':
    # Create all database tables if the script is being executed directly
    db.create_all()
    app.run(debug=True)
