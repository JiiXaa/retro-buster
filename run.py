from app import create_app
from app import db
from app.models.videocassettes import Videocassette

app = create_app()

### Create the database tables (dirty for testing purposes only)
# with app.app_context():
#     db.create_all()
#     vhs1 = Videocassette(
#         title="The Lord of the Rings", director="Peter Jackson", genre="Fantasy"
#     )
#     vhs2 = Videocassette(
#         title="The Matrix", director="The Wachowskis", genre="Science Fiction"
#     )
#     db.session.add(vhs1)
#     db.session.add(vhs2)
#     db.session.commit()

if __name__ == "__main__":
    app.run()
