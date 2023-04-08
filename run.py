from app import create_app
from app import db
from app.models.movies import Movie, VhsTapeCopy
from app.models.rentals import VhsRental
from app.models.customers import Customer

app = create_app()

### Create the database tables (dirty for testing purposes only)
# with app.app_context():
#     db.create_all()
#     vhs1 = Movie(
#         title="The Lord of the Rings", director="Peter Jackson", genre="Fantasy"
#     )
#     vhs2 = Movie(
#         title="The Matrix", director="The Wachowskis", genre="Science Fiction"
#     )
#     db.session.add(vhs1)
#     db.session.add(vhs2)
#     db.session.commit()

### Customer routes tests
# with app.app_context():
#     db.create_all()
#     customer1 = Customer(
#         first_name="John", last_name="Smith", email="john1989@gmail.com"
#     )
#     customer2 = Customer(
#         first_name="Trinity", last_name="Red", email="triny18@gmail.com"
#     )
#     db.session.add(customer1)
#     db.session.add(customer2)
#     db.session.commit()

if __name__ == "__main__":
    app.run()
