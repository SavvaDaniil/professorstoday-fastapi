
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import UserExpertStatementGrade
from typing import List

class UserExpertStatementGradeRepository():

    def find_by_id(self, id: int) -> UserExpertStatementGrade:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(UserExpertStatementGrade).filter(UserExpertStatementGrade.id == id).order_by(UserExpertStatementGrade.id).first()
        finally:
            session.close()
            
        return obj

    def find_by_user_expert_id_and_statement_id(self, user_expert_id: int, statement_id: int) -> UserExpertStatementGrade:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(UserExpertStatementGrade)\
                .filter((UserExpertStatementGrade.user_expert_id == user_expert_id) & (UserExpertStatementGrade.statement_id == statement_id))\
                    .order_by(UserExpertStatementGrade.id).first()
        finally:
            session.close()
            
        return obj
    
    def list_all(self) -> List[UserExpertStatementGrade]:
        objs = None
        ...
        return objs
    
    def list_by_user_expert_id(self, user_expert_id: int) -> List[UserExpertStatementGrade]:
        objs = None
        ...
        return objs

    def list_by_statement_id(self, statement_id: int) -> List[UserExpertStatementGrade]:
        objs: List[UserExpertStatementGrade] = []
        session = ApplicationDbContext.create_session()

        try: 
            objs = session.query(UserExpertStatementGrade)\
                .filter((UserExpertStatementGrade.statement_id == statement_id))\
                    .order_by(UserExpertStatementGrade.id)\
                    .all()
        finally:
            session.close()
            
        return objs

    def list_appreciated_by_statement_id(self, statement_id: int) -> List[UserExpertStatementGrade]:
        objs: List[UserExpertStatementGrade] = []
        ...
            
        return objs
    
    def list_all_appreciated(self) -> List[UserExpertStatementGrade]:
        objs = None
        ...
        return objs
    
    def add(self, obj: UserExpertStatementGrade) -> UserExpertStatementGrade:
        ...
    

    def update(self, userExpertStatementGrade: UserExpertStatementGrade) -> bool:
        session = ApplicationDbContext.create_session()
        #print("UserExpertStatementGrade.id: ", userExpertStatementGrade.id)
        try: 
            session.query(UserExpertStatementGrade)\
                .filter(UserExpertStatementGrade.id == userExpertStatementGrade.id)\
                .update({
                    UserExpertStatementGrade.user_expert_id : userExpertStatementGrade.user_expert_id,
                    UserExpertStatementGrade.statement_id : userExpertStatementGrade.statement_id,
        ...
                }, synchronize_session = False)
            session.commit()
        except Exception:
            ...
        finally:
            session.close()
            
        return True
