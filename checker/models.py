import datetime
import time
import uuid

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg_types
from sqlalchemy.ext.declarative import declarative_base

from db import pg_engine

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())


class BaseModified:
    def __init__(self, **kwargs):
        keys_ok = set(self.__table__.columns.keys())
        for k in kwargs:
            if k in keys_ok:
                setattr(self, k, kwargs[k])
        return

class MHData(BaseModified, Base):
    __tablename__ = 'mhdata'
    __table_args__ = {'extend_existing': True}
    id = sa.Column(pg_types.UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    sensorname = sa.Column(sa.String(50))
    temperature = sa.Column(sa.Numeric(precision=4, scale=1))
    humidity = sa.Column(sa.Integer)
    voltage = sa.Column(sa.Numeric(precision=5, scale=3))
    timestamp = sa.Column(sa.DateTime(timezone=False), default=datetime.datetime.utcnow)


def create_all():
    # Base.metadata.drop_all(pg_engine)
    Base.metadata.create_all(pg_engine)
    return
