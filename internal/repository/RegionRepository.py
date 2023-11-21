
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import Region
from typing import List

class RegionRepository():

    def find_by_id(self, id: int) -> Region:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(Region).filter(Region.id == id).order_by(Region.id).first()
        finally:
            session.close()
            
        return obj

    def list_all(self) -> List[Region]:
        objs = None
        ...
        return objs

    
    def add(self, obj: Region) -> Region:
        ...
        return obj
    

    def update(self, region: Region) -> bool:
        session = ApplicationDbContext.create_session()
        #print("region.id: ", region.id)
        try: 
            session.query(Region)\
                .filter(Region.id == region.id)\
                .update({
                    Region.name : region.name,
                    ...
                }, synchronize_session = False)
            session.commit()
        except Exception:
            ...
        finally:
            session.close()
            
        return True