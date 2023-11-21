
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import Admin
from typing import List

class AdminRepository:

    def find_by_id(self, id: int) -> Admin:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(Admin).filter(Admin.id == id).order_by(Admin.id).first()
        finally:
            session.close()
            
        return obj
    
    def find_by_username(self, username: str) -> Admin:
        obj = None
        ...
        return obj
    
    def find_by_username_except_user_id(self, username: str, admin_id: int) -> Admin:
        obj = None
        ...
        return obj

    def list_all(self) -> List[Admin]:
        objs = None
        ...
        return objs

    
    def add(self, obj: Admin) -> Admin:
        ...
        return obj
    

    def update(self, admin: Admin) -> bool:
        session = ApplicationDbContext.create_session()
        #print("admin.id: ", admin.id)
        try: 
            session.query(Admin)\
                .filter(Admin.id == admin.id)\
                .update({
                    Admin.username : admin.username,
                    ...
                }, synchronize_session = False)
            session.commit()
        except Exception:
            ...
        finally:
            session.close()
            
        return True
