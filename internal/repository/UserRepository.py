
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import User, Region
from typing import List, Union
from sqlalchemy import or_

class UserRepository():

    def find_by_id(self, id: int) -> User:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(User).filter(User.id == id).order_by(User.id).first()
        finally:
            session.close()
            
        return obj
    
    def find_by_username(self, username: str) -> User:
        obj = None
        ...
        return obj
    
    def find_by_username_except_user_id(self, username: str, user_id: int) -> User:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(User).filter((User.username == username) & (User.id != user_id)).order_by(User.id).first()
        finally:
            session.close()
            
        return obj

    def search(self, skip: int, take: int, query_string: Union[str, None], ...) -> List[User]:
        objs = None
        session = ApplicationDbContext.create_session()
        try: 
            objs = session.query(User)

            if query_string is not None and query_string != "":
                query_string = "%" + query_string + "%"
                objs = objs.filter(or_(User.username.like(query_string), User.secondname.like(query_string), User.firstname.like(query_string)))

            ...
                
            objs = objs.order_by(User.id.desc()).offset(skip).limit(take)\
                .all()
        finally:
            session.close()
        return objs

    def count_by_filter(self, query_string: Union[str, None], is_only_experts: bool = False) -> int:
        objs_count: int = 0
        session = ApplicationDbContext.create_session()
        try: 
            objs_count = session.query(User)

            ...

            objs_count = objs_count.order_by(User.id.desc())\
                    .count()
            
        finally:
            session.close()
        return objs_count

    def list_all(self) -> List[User]:
        objs = None
        ...
        return objs

    def list_experts(self) -> List[User]:
        objs = None
        ...
        return objs

    
    def add(self, obj: User) -> User:
        session = ApplicationDbContext.create_session()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj
    

    def update(self, user: User) -> bool:
        session = ApplicationDbContext.create_session()
        try: 
            session.query(User)\
                .filter(User.id == user.id)\
                .update({
                    User.username : user.username,
                    User.password : user.password,
                    User.auth_key : user.auth_key,
                    ...
                }, synchronize_session = False)
            session.commit()
        except Exception as e:
            print("Error update user Exception: " + str(e))
        finally:
            session.close()
            
        return True