from sqlalchemy.dialects.postgresql import UUID
import uuid
from db import db
import marshmallow as ma

# from models.enrolled_devices import EnrolledDevicesSchema


class Assets(db.Model):
    __tablename__ = "Assets"
    asset_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    site_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("SnipeItSite.site_id"),
        nullable=False,
    )
    serial_number = db.Column(db.String(), nullable=False, unique=True)
    make = db.Column(db.String())
    model_num = db.Column(db.String())
    model_name = db.Column(db.String())
    deployed = db.Column(db.Boolean())
    assigned_to = db.Column(db.String())
    asset_tag = db.Column(db.Integer())
    enrolled = db.relationship(
        "EnrolledDevices",
        back_populates="asset",
        lazy=True
        # primaryjoin="EnrolledDevices.serial_number==Assets.serial_number",
    )

    def __init__(
        self,
        serial_number,
        site_id,
        make,
        model_num,
        model_name,
        deployed,
        assigned_to,
        asset_tag,
    ):
        self.serial_number = serial_number
        self.site_id = site_id
        self.make = make
        self.model_num = model_num
        self.model_name = model_name
        self.deployed = deployed
        self.assigned_to = assigned_to
        self.asset_tag = asset_tag


class AssetsSchema(ma.Schema):
    class Meta:
        fields = [
            "asset_id",
            "serial_number",
            "make",
            "model_num",
            "model_name",
            "deployed",
            "assigned_to",
            "asset_tag",
            "enrolled",
        ]

    # this isnt working. other direction works fine
    enrolled = ma.fields.Nested("EnrolledDevicesSchema", only=["enrollment_status"])


asset_schema = AssetsSchema()
assets_schema = AssetsSchema(many=True)
