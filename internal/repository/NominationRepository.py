
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import Nomination
from typing import List

class NominationRepository():

    def find_by_id(self, id: int) -> Nomination:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(Nomination).filter(Nomination.id == id).order_by(Nomination.id).first()
        finally:
            session.close()
            
        return obj

    def list_all(self) -> List[Nomination]:
        objs = None
        ...
        return objs

    
    def add(self, obj: Nomination) -> Nomination:
        ...
        return obj
    

    def update(self, nomination: Nomination) -> bool:
        session = ApplicationDbContext.create_session()
        #print("Nomination.id: ", nomination.id)
        try: 
            session.query(Nomination)\
                .filter(Nomination.id == nomination.id)\
                .update({
                    Nomination.name : nomination.name,
                    ...
                }, synchronize_session = False)
            session.commit()
        except Exception:
            ...
        finally:
            session.close()
            
        return True