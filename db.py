from flask_sqlalchemy import SQLAlchemy
from lib.loaders import load_models
from flask import Flask

__all__ = ("db", "init_db")

# our global DB ojbect (imported by models and views)
db = SQLAlchemy()

# support importing a functioning session query
query = db.session.query


def init_db(app=None, db=None):
    """Initializes the global database object used by the app."""
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        load_models()
        db.init_app(app)
    else:
        raise ValueError("Cannot init DB without db and app objects.")


def populate_object(obj, data_dictionary):
    fields = data_dictionary.keys()
    updated_fields = []
    for field in fields:
        if getattr(obj, field):  # If the user object has the field 'field'...
            setattr(obj, field, data_dictionary[field])
            updated_fields.append(field)
    return updated_fields
