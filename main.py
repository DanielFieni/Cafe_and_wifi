from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

app = Flask(__name__)

# CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "aaaccc"
bootstrap = Bootstrap(app)
app.app_context().push()

class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Cafe location in Google maps (URL)', validators=[DataRequired()])
    img_url = StringField('Image location (URL)', validators=[DataRequired()])
    location = StringField('Cafe location (City or State)', validators=[DataRequired()])
    seats = StringField('Number of seats', validators=[DataRequired()])
    has_toilet = BooleanField("Has toilet?")
    has_wifi = BooleanField("Has wifi?")
    has_sockets = BooleanField("Has sockets?")
    can_take_calls = BooleanField("Can take calls?")
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


# CREATE TABLE
class Cafe(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

# db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all")
def all_cafes():
    cafes = db.session.query(Cafe).all()
    list_title = ["Name", "Map URL", "Img URL", "Location", "Seats", "Has toilet?", "Has wifi?", "Has socket?", "Can take calls?", "Coffee Price"]

    return render_template("all_cafes.html", cafes=cafes, titles=list_title)

@app.route("/add", methods=["GET", "POST"])
def addCafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            seats = form.seats.data,
            has_toilet = form.has_toilet.data,
            has_wifi = form.has_wifi.data,
            has_sockets = form.has_sockets.data,
            can_take_calls = form.can_take_calls.data,
            coffee_price = form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("all_cafes"))


    return render_template("add.html", form=form)

@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):

    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("all_cafes"))

if __name__ == "__main__":
    app.run(debug=True)