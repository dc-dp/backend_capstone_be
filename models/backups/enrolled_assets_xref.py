from sqlalchemy.dialects.postgresql import UUID
import uuid
from db import db

# import marshmallow as ma


class EnrolledDevicesAssetsXRef(db.Model):
    __tablename__ = "EnrolledDevicesAssetsXRef"
    device_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("EnrolledDevices.device_id"),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    asset_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("Assets.asset_id"),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    def __init__(self, device_id, asset_id):
        self.device_id = device_id
        self.asset_id = asset_id


# class EnrolledDevicesAssetsXRefSchema(ma.Schema):
#     class Meta:
#         fields = ["device_id", "asset_id"]


# enrolled_device_schema = EnrolledDevicesAssetsXRefSchema()
# enrolled_devices_schema = EnrolledDevicesAssetsXRefSchema(many=True)
