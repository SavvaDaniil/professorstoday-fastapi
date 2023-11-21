
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import Statement, UserExpertStatementGrade, User
from typing import List, Union
from sqlalchemy import or_

class StatementRepository():

    def find_by_id(self, id: int) -> Statement:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(Statement).filter(Statement.id == id).order_by(Statement.id).first()
        finally:
            session.close()
            
        return obj
    
    def find_by_user_id_and_contest_id(self, user_id: int, contest_id: int) -> Statement:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(Statement).filter((Statement.user_id == user_id) & (Statement.contest_id == contest_id)).order_by(Statement.id).first()
        finally:
            session.close()
            
        return obj

    def search(
            self, 
            skip: int, 
            take: int, 
            query_string: Union[str, None], 
            status: int = 0,
            nomination_id: int = 0,
            region_id: int = 0,
            university_id: int = 0
    ) -> List[Statement]:

        if status < 0 or status > 2:
            status = 0

        objs = None
        session = ApplicationDbContext.create_session()
        try: 
            objs = session.query(Statement)
            if status == 1:
                objs = objs.filter(Statement.status == 0)
            elif status == 2:
                objs = objs.filter(Statement.status == 1)

            if query_string is not None and query_string != "":
                ...
            
            if nomination_id != 0:
                ...

            if region_id != 0 and university_id != 0:
                ...
            elif region_id != 0:
                ...
            elif university_id != 0:
                ...
            
            objs = objs.order_by(Statement.id).offset(skip).limit(take)\
                    .all()
        finally:
            session.close()
        return objs

    def count_by_filter(
            self, 
            query_string: Union[str, None], 
            status: int = 0,
            nomination_id: int = 0,
            region_id: int = 0,
            university_id: int = 0
    ) -> int:
        
        if status < 0 or status > 2:
            status = 0

        objs_count = None
        session = ApplicationDbContext.create_session()
        try: 
            ...
        finally:
            session.close()
        return objs_count if objs_count is not None else 0

    def count_by_filter_for_statistic(self, is_any: bool = False) -> int:
        objs_count: int = 0
        session = ApplicationDbContext.create_session()
        try: 
            objs_count = session.query(Statement)\
                .filter(Statement.status == 1)\
                .join(UserExpertStatementGrade, (UserExpertStatementGrade.statement_id == Statement.id) & (UserExpertStatementGrade.is_appreciated))\
                .order_by(Statement.id.desc())\
                .group_by(Statement.id)\
                .count()
        finally:
            session.close()
        return objs_count
    

    def list_all(self) -> List[Statement]:
        objs = None
        ...
        return objs

    def list_by_user_id(self, user_id: int) -> List[Statement]:
        objs = None
        ...
        return objs
    
    def list_sended_not_appreciated(self) -> List[Statement]:
        objs = None
        ...
        return objs
    
    def add(self, obj: Statement) -> Statement:
        ...
        return obj
    

    def update(self, statement: Statement) -> bool:
        session = ApplicationDbContext.create_session()
        try: 
            session.query(Statement)\
                .filter(Statement.id == statement.id)\
                .update({
                    Statement.user_id : statement.user_id,
                    ...
                }, synchronize_session = False)
            session.commit()
        except Exception:
            ...
        finally:
            session.close()
            
        return True