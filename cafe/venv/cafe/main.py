#!/usr/bin/env python3
import secrets
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from forms import AddCafeForm


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
Bootstrap(app)

class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Coffee Table

class CoffeeTable(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    CoffeeName: Mapped[str] = mapped_column(String(500), unique=True)
    Location: Mapped[str] = mapped_column(String(500))
    Availability_details: Mapped[str] = mapped_column(String(2000))


with app.app_context():
    db.create_all()



# Running the app
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafe/all-cafe')
def view_cafe():
    all_cafes = CoffeeTable.query.all()
    return render_template('cafes.html', cafes=all_cafes)


@app.route("/cafe/add-cafe", methods=["GET", "POST"])
def add_cafe():
    add_form = AddCafeForm()
    if add_form.validate_on_submit():
        coffee_name = add_form.name.data
        coffee_location = add_form.Location.data
        availability = add_form.Availability.data
        coffee_table = CoffeeTable(
            CoffeeName=coffee_name,
            Location=coffee_location,
            Availability_details=availability
        )
        db.session.add(coffee_table)
        db.session.commit()
        return redirect(url_for('view_cafe'))

    return render_template('add-cafe.html', form=add_form)


if __name__ == "__main__":
    app.run(debug=True)