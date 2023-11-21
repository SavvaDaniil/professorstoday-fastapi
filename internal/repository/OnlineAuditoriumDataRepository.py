
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import OnlineAuditoriumData
from typing import List, Union
from sqlalchemy import or_

class OnlineAuditoriumDataRepository():

    def find_by_id(self, id: int) -> OnlineAuditoriumData:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(OnlineAuditoriumData).filter(OnlineAuditoriumData.id == id).order_by(OnlineAuditoriumData.id).first()
        finally:
            session.close()
            
        return obj
    
    def find_by_name(self, name: str) -> OnlineAuditoriumData:
        obj = None
        ...
            
        return obj

    def list_all(self) -> List[OnlineAuditoriumData]:
        objs: List[OnlineAuditoriumData] = []
        ...
        return objs
    

    def update(self, onlineAuditoriumData: OnlineAuditoriumData) -> bool:
        session = ApplicationDbContext.create_session()
        #print("user.id: ", user.id)
        try: 
            session.query(OnlineAuditoriumData)\
                .filter(OnlineAuditoriumData.id == onlineAuditoriumData.id)\
                .update({
                    OnlineAuditoriumData.name : onlineAuditoriumData.name,
                    ...
                }, synchronize_session = False)
            session.commit()
        except Exception:
            ...
        finally:
            session.close()
            
        return True
