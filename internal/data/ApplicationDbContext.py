
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ApplicationDbContext(object):

    def create_session():
        engine = create_engine("XXXXXXXXXXXXX://XXXXXXXXXXXXX:XXXXXXXXXXXXX@XXXXXXXXXXXXX:000/XXXXXXXXXXXXX", echo = False, pool_size=10, max_overflow=20)
        Session = sessionmaker(bind = engine)
        session = Session()
        return session