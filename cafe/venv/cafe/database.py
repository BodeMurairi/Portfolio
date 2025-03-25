from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = os.urandom(24) # Secret key
db = SQLAlchemy(model_class=Base)
db.init_app(app)
# CREATE TABLE IN DB

# Coffee Table

class CoffeeTable(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    CoffeeName: Mapped[str] = mapped_column(String(500), unique=True)
    Location: Mapped[str] = mapped_column(String(500))
    Availability_details: Mapped[str] = mapped_column(String(2000))


with app.app_context():
    db.create_all()

