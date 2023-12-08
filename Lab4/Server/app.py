from flask import Flask
from models import base, drug, type, subst, mark, store, city, chain, user, address

db = base.db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    return app


app = create_app()


@app.route("/")
def hello_world():
    drugs = db.session.query(drug.Drug).all()
    drugstores = db.session.query(store.Store).filter(store.Store.chain == None)
    users =  db.session.query(user.User).all()
    res = []
    for user_res in users:
        res.append(user_res.as_dict())
    return res

