import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sqlalchemy import create_engine,Table,MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8', echo=True)
Base = declarative_base() #
class Stock_list(Base):
	__tablename__ = 'stock list'
	uid = Column(Integer, primary_key)
	code = Column(String)

	def __repr__(self):
		return '<Stock_list(code='%s')>' % self.code
Base.metadata.create_all(engine)




st_li = Table(
'stock_list', metadata,
Column('uid', Integer, primary_key=True),
Column('code', String(20),nullable=False)
)
metadata.create_all(engine)
class Stock_list(object):
	pass
mapper(Stock_list, st_li)

sl = Stock_list()
sl.code = '600000'
session.add(sl)
session.flush()
session.commit()

def writeinto():
	engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8', echo=True)
	metadata = MetaData()
	Session = sessionmaker(bind=engine)
	session = Session()
	session.add(sl)
	session.flush()
	session.commit()

query = session.query(Stock_list)
print list(query)
print query.get(1)
print query.filter_by(code='600000').first()
session.commit()








