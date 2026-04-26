# -*- coding: utf-8 -*-
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String, Unicode, DateTime
from sqlalchemy.orm import relationship, backref
from models import dbsession
from models.BaseModels import DatabaseObject
from datetime import datetime

# Table de liaison pour les acheteurs
information_trade_to_team = Table(
    "information_trade_to_team",
    DatabaseObject.metadata,
    Column("information_trade_id", Integer, ForeignKey("information_trade.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("team.id"), primary_key=True),
)

class InformationTrade(DatabaseObject):
    """
    Represents an information/hint sold by a team to other teams.
    """
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    seller_team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    box_id = Column(Integer, ForeignKey("box.id"), nullable=False)
    
    title = Column(Unicode(255), nullable=False)
    content = Column(Unicode(4096), nullable=False)
    price = Column(Integer, nullable=False, default=100)
    created = Column(DateTime, default=datetime.utcnow)

    # Relationships
    seller_team = relationship("Team", backref=backref("sales", lazy="select"))
    box = relationship("Box", backref=backref("trades", lazy="select"))
    buyers = relationship("Team", secondary=information_trade_to_team, backref=backref("purchased_trades", lazy="select"))

    @classmethod
    def all(cls):
        return dbsession.query(cls).all()

    @classmethod
    def by_uuid(cls, _uuid):
        return dbsession.query(cls).filter_by(uuid=str(_uuid)).first()

    @classmethod
    def by_box(cls, box_id):
        return dbsession.query(cls).filter_by(box_id=box_id).all()

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "seller": self.seller_team.name,
            "box": self.box.name,
            "title": self.title,
            "price": self.price,
            "created": self.created.strftime("%Y-%m-%d %H:%M"),
        }
