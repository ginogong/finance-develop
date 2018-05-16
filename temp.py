
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sqlalchemy import create_engine, Column, String, Table, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8', echo=True)
Base   = declarative_base()
class Stock_list(Base):
	__tablename__ = 'stock list'
	uid  = Column(Integer, primary_key=True)
	code = Column(String(20))

	def __repr__(self):
		return "<Stock_list(code='%s')>" % self.code

print Stock_list.__table__
Base.metadata.create_all(engine)

