from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_socketio import SocketIO, emit
import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from piano import Piano, BuildScale, BuildChord


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=1)
socketio = SocketIO(app)

db = SQLAlchemy(app)


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


"""@socketio.on('keydown')
def handle_keydown(data):
    emit('keydown', data, broadcast=True, include_self=False)"""


"""@socketio.on('keyup')
def handle_keyup(data):
    emit('keyup', data, broadcast=True, include_self=False)"""


"""@app.route('/')
def index():
    return render_template('index.html', static_url_path='/static')
    # return render_template('index.html', keys=keys, static_url_path='/static')"""


@app.route('/')
def index():
    return render_template('home.html', static_url_path='/static')
    # return render_template('index.html', keys=keys, static_url_path='/static')


@app.route('/test')
def test():
    return render_template('test.html', static_url_path='/static')
    # return render_template('index.html', keys=keys, static_url_path='/static')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Successfully logged in.", "info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in.", "info")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email was saved.")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", user=user, email=email)
    else:
        flash("You are not logged in!", "info")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"See you next time, {user}!", "info")
    else:
        flash(f"You were not logged in.", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@socketio.on('request-note')
def handle_note_played(data):
    print(f"handle_note_played {data}")
    emit('play note', data, broadcast=True)


@app.route("/classes")
def classes():
    return render_template('classes.html', static_url_path='/static')


#@socketio.on('request-chord')
#def handle_chord_played(chord):
#    print(f"handle_chord_played {chord}")
#    chord = BuildScale.build(piano, piano["C4"], chord_name="7+5")
#    emit('play chord', chord, broadcast=True)


@socketio.on('request-chord-sequence')
def handle_chord_sequence_played(chord):
    print(f"handle_chord_sequence_played {chord}")
    chord_sequence = BuildChord.build(piano, piano["C3"], chord_name="add2")
    print(chord_sequence)
    emit('play chord sequence', {"sequence": chord_sequence, "speed": 45}, broadcast=True)


@socketio.on('request-sequence')
def handle_sequence_played(sequence, bpm=180):
    sequence = BuildScale.build(piano, piano["F3"], scale_name="harmonic_minor")
    print(f"handle_sequence_played {sequence} at {bpm} BPM")
    emit('play sequence', {"sequence": sequence, "speed": bpm}, broadcast=True)


if __name__ == '__main__':
    # socketio.run(app, host="0.0.0.0", debug=True)
    piano = Piano()
    socketio.run(app, debug=True)
    db.create_all()

# play_chord_sequence?
