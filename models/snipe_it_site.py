from sqlalchemy.dialects.postgresql import UUID
import uuid
from db import db
import marshmallow as ma


class SnipeItSite(db.Model):
    __tablename__ = "SnipeItSite"
    site_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    api_token = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False, unique=True)
    org_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("Organizations.org_id"),
        nullable=False,
    )

    def __init__(self, api_token, url, name, org_id):
        self.api_token = api_token
        self.url = url
        self.name = name
        self.org_id = org_id


class SnipeItSiteSchema(ma.Schema):
    class Meta:
        fields = ["site_id", "api_token", "url", "name", "org_id"]


snipeit_site_schema = SnipeItSiteSchema()
snipeit_sites_schema = SnipeItSiteSchema(many=True)
