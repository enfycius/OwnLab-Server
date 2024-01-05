from datetime import timedelta
from flask import (
    Flask,
    jsonify,
    render_template,
    redirect,
    flash,
    send_from_directory,
    url_for,
    session,
    request,
    Response
)

from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError
from werkzeug.utils import secure_filename

from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User
from forms import login_form,register_form
import os

from flaskext.mysql import MySQL

############################################################################################## import all the necessary modules
app = create_app()
mysql = MySQL()

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "1234"
app.config["MYSQL_DATABASE_DB"] = "file"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.secret_key = 'secret-key'
mysql.init_app(app)

##############################################################################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html",title="Home")

@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    payload = request.get_json()
    if payload:
        try:
            user = User.query.filter_by(email=payload['email']).first()
            if check_password_hash(user.pwd, payload['pwd']):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return payload

    # form = login_form()

    # if form.validate_on_submit():
    #     try:
    #         user = User.query.filter_by(email=form.email.data).first()
    #         if check_password_hash(user.pwd, form.pwd.data):
    #             login_user(user)
    #             return redirect(url_for('index'))
    #         else:
    #             flash("Invalid Username or password!", "danger")
    #     except Exception as e:
    #         flash(e, "danger")

    # return render_template("auth.html",
    #     form=form,
    #     text="Login",
    #     title="Login",
    #     btn_action="Login"
    #     )

# Register route
@app.route("/register", methods=("GET", "POST"), strict_slashes=False)
def register():
    payload = request.get_json()
    if payload:
        try:
            email = payload['email']
            pwd = payload['pwd']
            username = payload['username']
            tel = payload['tel']
            newuser = User(
                username=username,
                email=email,
                tel=tel,
                pwd=bcrypt.generate_password_hash(pwd),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")

    return payload

    # form = register_form()
    # if form.validate_on_submit():
    #     try:
    #         email = form.email.data
    #         pwd = form.pwd.data
    #         username = form.username.data
    #         tel = form.tel.data
    #         newuser = User(
    #             username=username,
    #             email=email,
    #             tel=tel,
    #             pwd=bcrypt.generate_password_hash(pwd),
    #         )
    
    #         db.session.add(newuser)
    #         db.session.commit()
    #         flash(f"Account Succesfully created", "success")
    #         return redirect(url_for("login"))

    #     except InvalidRequestError:
    #         db.session.rollback()
    #         flash(f"Something went wrong!", "danger")
    #     except IntegrityError:
    #         db.session.rollback()
    #         flash(f"User already exists!.", "warning")
    #     except DataError:
    #         db.session.rollback()
    #         flash(f"Invalid Entry", "warning")
    #     except InterfaceError:
    #         db.session.rollback()
    #         flash(f"Error connecting to the database", "danger")
    #     except DatabaseError:
    #         db.session.rollback()
    #         flash(f"Error connecting to the database", "danger")
    #     except BuildError:
    #         db.session.rollback()
    #         flash(f"An error occured !", "danger")
    # return render_template("auth.html",
    #     form=form,
    #     text="Create account",
    #     title="Register",
    #     btn_action="Register account"
    #     )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

############################################################################################## login, register and logout routes
UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods = ['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == "__main__":
    app.run(debug=True)
