
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import Contest
from typing import List

class ContestRepository():

    def find_by_id(self, id: int) -> Contest:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(Contest).filter(Contest.id == id).order_by(Contest.id).first()
        finally:
            session.close()
            
        return obj

    def list_all(self) -> List[Contest]:
        objs = None
        ...
        return objs

    def list_all_visible(self) -> List[Contest]:
        objs = None
        ...
        return objs

    
    def add(self, obj: Contest) -> Contest:
        ...
        return obj
    

    def update(self, contest: Contest) -> bool:
        session = ApplicationDbContext.create_session()
        try: 
            session.query(Contest)\
                .filter(Contest.id == contest.id)\
                .update({
                    Contest.name : contest.name,
                    ...
                }, synchronize_session = False)
            session.commit()
        except Exception:
            ...
        finally:
            session.close()
            
        return True