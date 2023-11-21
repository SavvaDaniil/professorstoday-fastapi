
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import OnlineAuditoriumMessage
from typing import List, Union
from sqlalchemy import or_


class OnlineAuditoriumMessageRepository():

    def find_by_id(self, id: int) -> OnlineAuditoriumMessage:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(OnlineAuditoriumMessage).filter(OnlineAuditoriumMessage.id == id).first()
        finally:
            session.close()
            
        return obj

    def list_all_for_user(self) -> List[OnlineAuditoriumMessage]:
        objs: List[OnlineAuditoriumMessage] = []
        ...
        return objs

    def list_all(self) -> List[OnlineAuditoriumMessage]:
        objs: List[OnlineAuditoriumMessage] = []
        ...
        return objs

    def add(self, obj: OnlineAuditoriumMessage) -> OnlineAuditoriumMessage:
        ...
        return obj
    

    def update(self, onlineAuditoriumMessage: OnlineAuditoriumMessage) -> bool:
        session = ApplicationDbContext.create_session()
        #print("user.id: ", user.id)
        try: 
            session.query(OnlineAuditoriumMessage)\
                .filter(OnlineAuditoriumMessage.id == onlineAuditoriumMessage.id)\
                .update({
                    OnlineAuditoriumMessage.user_id : onlineAuditoriumMessage.user_id,
                    ...
                }, synchronize_session = False)
            session.commit()
        except Exception as e:
            ...
        finally:
            session.close()
            
        return True