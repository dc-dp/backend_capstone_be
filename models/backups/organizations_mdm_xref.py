from sqlalchemy.dialects.postgresql import UUID
import uuid
from db import db

# import marshmallow as ma


class OrganizationsMdmSiteXRef(db.Model):
    __tablename__ = "OrganizationsMdmSiteXRef"
    org_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("Organizations.org_id"),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    mdm_site_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("MdmSite.mdm_site_id"),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    def __init__(self, org_id, mdm_site_id):
        self.org_id = org_id
        self.mdm_site_id = mdm_site_id


# class OrganizationsMdmSiteXRefSchema(ma.Schema):
#     class Meta:
#         fields = ["org_id", "mdm_site_id"]


# enrolled_device_schema = OrganizationsMdmSiteXRefSchema()
# enrolled_devices_schema = OrganizationsMdmSiteXRefSchema(many=True)
