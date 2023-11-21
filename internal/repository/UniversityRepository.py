
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import University
from typing import List

class UniversityRepository():

    def find_by_id(self, id: int) -> University:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(University).filter(University.id == id).order_by(University.id).first()
        finally:
            session.close()
            
        return obj

    def list_all(self) -> List[University]:
        objs = None
        ...
        return objs

    
    def add(self, obj: University) -> University:
        ...
        return obj
    

    def update(self, university: University) -> bool:
        session = ApplicationDbContext.create_session()
        #print("University.id: ", university.id)
        try: 
            session.query(University)\
                .filter(University.id == university.id)\
                .update({
                    University.name : university.name,
                    ...
                }, synchronize_session = False)
            session.commit()
        except Exception:
            ...
        finally:
            session.close()
            
        return True