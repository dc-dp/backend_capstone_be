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

    def __init__(self, site_id, api_token, url, name):
        self.site_id = site_id
        self.api_token = api_token
        self.url = url
        self.name = name


class SnipeItSiteSchema(ma.Schema):
    class Meta:
        fields = ["site_id", "api_token", "url", "name"]


mdm_site_schema = SnipeItSiteSchema()
mdm_sites_schema = SnipeItSiteSchema(many=True)
