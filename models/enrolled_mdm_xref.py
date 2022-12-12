from sqlalchemy.dialects.postgresql import UUID
import uuid
from db import db

# import marshmallow as ma


class EnrolledDevicesMdmSiteXRef(db.Model):
    __tablename__ = "EnrolledDevicesMdmSiteXRef"
    device_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("EnrolledDevices.device_id"),
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

    def __init__(self, device_id, mdm_site_id):
        self.device_id = device_id
        self.mdm_site_id = mdm_site_id


# class EnrolledDevicesMdmSiteXRefSchema(ma.Schema):
#     class Meta:
#         fields = ["device_id", "mdm_site_id"]


# enrolled_device_schema = EnrolledDevicesMdmSiteXRefSchema()
# enrolled_devices_schema = EnrolledDevicesMdmSiteXRefSchema(many=True)
