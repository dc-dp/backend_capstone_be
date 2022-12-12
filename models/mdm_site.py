from sqlalchemy.dialects.postgresql import UUID
import uuid
from db import db
import marshmallow as ma


class MdmSite(db.Model):
    __tablename__ = "MdmSite"
    mdm_site_id = db.Column(
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
        unique=True,
    )

    def __init__(self, mdm_site_id, api_token, url, name):
        self.mdm_site_id = mdm_site_id
        self.api_token = api_token
        self.url = url
        self.name = name


class MdmSiteSchema(ma.Schema):
    class Meta:
        fields = ["mdm_site_id", "api_token", "url", "name"]


mdm_site_schema = MdmSiteSchema()
mdm_sites_schema = MdmSiteSchema(many=True)
