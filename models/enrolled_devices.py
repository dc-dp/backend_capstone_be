from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from db import db
import marshmallow as ma


class EnrolledDevices(db.Model):
    __tablename__ = "EnrolledDevices"
    device_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        # default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    serial_number = db.Column(
        db.String(),
        # db.ForeignKey("Assets.serial_number"),
        nullable=False,
        unique=True,
    )
    enrollment_status = db.Column(db.Boolean())
    last_seen = db.Column(db.String())
    dep_profile_status = db.Column(db.String())

    def __init__(
        self, device_id, serial_number, enrollment_status, last_seen, dep_profile_status
    ):
        self.device_id = device_id
        self.serial_number = serial_number
        self.enrollment_status = enrollment_status
        self.last_seen = last_seen
        self.dep_profile_status = dep_profile_status


class EnrolledDevicesSchema(ma.Schema):
    class Meta:
        fields = [
            "device_id",
            "serial_number",
            "enrollment_status",
            "last_seen",
            "dep_profile_status",
        ]


enrolled_device_schema = EnrolledDevicesSchema()
enrolled_devices_schema = EnrolledDevicesSchema(many=True)
