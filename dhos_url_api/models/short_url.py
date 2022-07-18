from typing import Dict

from flask_batteries_included.sqldb import ModelIdentifier, db


class ShortUrl(ModelIdentifier, db.Model):

    original_url = db.Column(db.String, unique=False, nullable=False)
    short_form = db.Column(db.String, unique=True, nullable=False)
    remaining_uses = db.Column(db.Integer, nullable=True)

    def to_dict(self) -> Dict:
        return {"short_form": self.short_form}
