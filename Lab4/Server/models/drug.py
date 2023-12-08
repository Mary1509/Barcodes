from sqlalchemy import *
from sqlalchemy.orm import relationship

from models.base import Base


class Drug(Base):
    """drugs"""
    __tablename__ = 'drugs'
    uid = Column(Integer,
                 Sequence('drugs_uid_seq'),
                 primary_key=True,
                 server_default=Sequence('drugs_uid_seq').next_value(),
                 autoincrement=True)
    name = Column(Text, nullable=False)
    barcode = Column(VARCHAR, nullable=False)
    exp_date = Column(Date, nullable=False)
    serial_no = Column(Text, nullable=False)
    prescription = Column(Boolean, nullable=False, default=False)
    type_id = Column(Integer, ForeignKey('types.uid', onupdate='CASCADE'))
    type = relationship("Type", back_populates='drugs')
    main_subs_id = Column(Integer, ForeignKey('substances.uid', onupdate='CASCADE'))
    subs = relationship("Substance", back_populates='drugs')
    trademark_id = Column(Integer, ForeignKey('trademarks.uid', onupdate='CASCADE'))
    mark = relationship("Mark", back_populates='drugs')

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
