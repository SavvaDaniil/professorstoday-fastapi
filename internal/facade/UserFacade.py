
from fastapi import Response, UploadFile, HTTPException
from datetime import datetime
from typing import List
import os, hashlib
from passlib.context import CryptContext
from logging import Logger
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError, SMTPException
import threading

from internal.facade.LeagueParticipationMembershipStatusFacade import LeagueParticipationMembershipStatusFacade
from internal.facade.NominationFacade import NominationFacade
from internal.repository.UserRepository import UserRepository
from internal.repository.LeagueParticipationMembershipStatusRepository import LeagueParticipationMembershipStatusRepository
from internal.repository.RegionRepository import RegionRepository
from internal.repository.UniversityRepository import UniversityRepository
from internal.repository.StatementRepository import StatementRepository
from internal.repository.UserExpertStatementGradeRepository import UserExpertStatementGradeRepository
from internal.repository.NominationRepository import NominationRepository
from internal.middleware.UserMiddleware import UserMiddleware
from internal.config.MailingConfiguration import MailingConfiguration
from internal.Entities import User, Region, University, LeagueParticipationMembershipStatus, Statement, UserExpertStatementGrade, Nomination
from internal.dto.UserDTO import UserLoginDTO, UserRegistrationDTO, UserProfileEditDTO, UserEditDTO, UserForgetDTO, UserSearchDTO, UserExpertSetupNewDTO
from internal.factory.UserFactory import UserFactory
from internal.factory.UserExpertStatementGradeFactory import UserExpertStatementGradeFactory
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus
from internal.viewmodel.UserViewModel import UserProfileLiteViewModel, UserPreviewViewModel
from internal.viewmodel.LeagueParticipationMembershipStatusViewModel import LeagueParticipationMembershipStatusMicroViewModel
from internal.viewmodel.UserExpertStatementViewModel import UserExpertStatementPreviewsSearchDataViewModel
from internal.viewmodel.NominationViewModel import NominationMicroViewModel
from internal.viewmodel.UserExpertStatementGradeViewModel import UserExpertStatementGradePreviewViewModel
from internal.custom_exception.UserCustomException import UserNotFoundException, UsernameAlreadyExistsException, UserProfileNotFilledException, UserNotExpertException, UserNotExpertSetupedException, UserExpertNoChoosenNominationsException, UserExpertFoundedTooMuchException
from internal.custom_exception.LeagueParticipationMembershipStatusException import LeagueParticipationMembershipStatusNotFoundException
from internal.custom_exception.RegionCustomException import RegionNotFoundException
from internal.custom_exception.UniversityCustomException import UniversityNotFoundException
from internal.util.RandomUtil import RandomUtil
from internal.util.LoggerUtil import LoggerUtil

class UserFacade:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    PASSWORD_MASTER_HASH: str = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    logger: Logger = LoggerUtil.get()

    def __init__(self) -> None:
        self.userRepository: UserRepository = UserRepository()
    
    def expert_setup(self, user_id: int, userExpertSetupNewDTO: UserExpertSetupNewDTO) -> None:
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        if not user.is_expert:
            raise UserNotExpertException()
        
        if userExpertSetupNewDTO.nomination_ids is None or len(userExpertSetupNewDTO.nomination_ids) == 0:
            raise UserExpertNoChoosenNominationsException()

        choosen_nomination_ids: List[Nomination] = []
        nominationRepository: NominationRepository = NominationRepository()
        nominations: List[Nomination] = nominationRepository.list_all()
        for nomination_id in userExpertSetupNewDTO.nomination_ids:
            for nomination in nominations:
                if nomination.id == nomination_id:
                    choosen_nomination_ids.append(nomination.id)
                    continue
        
        if len(choosen_nomination_ids) == 0:
            raise UserExpertNoChoosenNominationsException()


        statementRepository: StatementRepository = StatementRepository()
        statementsNotAppreciated: List[Statement] = statementRepository.list_sended_not_appreciated()

        userExpertStatementGradeRepository: UserExpertStatementGradeRepository = UserExpertStatementGradeRepository()
        userExpertStatementGrades: List[UserExpertStatementGrade] = userExpertStatementGradeRepository.list_all()

        number_of_statements_on_nomination: int = 0
        count_of_userExpertStatementGrades_on_statement: int = 0
        date_now: datetime = datetime.now()

        for choosen_nomination_id in choosen_nomination_ids:

            number_of_statements_on_nomination = 0

            for statementNotAppreciated in statementsNotAppreciated:

                if number_of_statements_on_nomination >= 5:
                    break
                if statementNotAppreciated.nomination_id != choosen_nomination_id:
                    continue
                if statementNotAppreciated.user is not None:
                    statement_user: User = statementNotAppreciated.user
                    if statement_user.university_id == user.university_id or statement_user.id == 1 or statement_user.id == 2:
                        continue

                count_of_userExpertStatementGrades_on_statement = 0

                #подсчет, сколько привязанных экспертов к заявлению
                for userExpertStatementGrade in userExpertStatementGrades:
                    if userExpertStatementGrade.statement_id == statementNotAppreciated.id:
                        count_of_userExpertStatementGrades_on_statement += 1
                
                if count_of_userExpertStatementGrades_on_statement >= 5:
                    continue
                
                #нужна проверка, что заявка уже есть в базе
                if userExpertStatementGradeRepository.find_by_user_expert_id_and_statement_id(
                    user_expert_id=user_id,
                    statement_id=statementNotAppreciated.id
                ) is not None:
                    continue

                ...
        
        user.is_expert_setuped = 1
        self.userRepository.update(user=user)
        

    
    def expert_list_of_statement_previews_for_user_expert(self, user_id: int) -> UserExpertStatementPreviewsSearchDataViewModel:
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        if user.username is None or user.username == "" \
            ...:
            raise UserProfileNotFilledException()
        
        if not user.is_expert:
            raise UserNotExpertException()
        
        nominationFacade: NominationFacade = NominationFacade()
        nominationMicroViewModel: List[NominationMicroViewModel] = nominationFacade.list_micro()
        if not user.is_expert_setuped:
            return UserExpertStatementPreviewsSearchDataViewModel(
                is_expert_setuped=False,
                nominationMicroViewModels=nominationMicroViewModel
            )
        
        userExpertStatementGradePreviewViewModels: List[UserExpertStatementGradePreviewViewModel] = []
        userExpertStatementGradeRepository: UserExpertStatementGradeRepository = UserExpertStatementGradeRepository()
        userExpertStatementGrades: List[UserExpertStatementGrade] = userExpertStatementGradeRepository.list_by_user_expert_id(user_expert_id=user.id)
        userExpertStatementGradeFactory: UserExpertStatementGradeFactory = UserExpertStatementGradeFactory()
        for userExpertStatementGrade in userExpertStatementGrades:
            userExpertStatementGradePreviewViewModels.append(
                userExpertStatementGradeFactory.create_preview(
                    userExpertStatementGrade=userExpertStatementGrade
                )
            )
        
        return UserExpertStatementPreviewsSearchDataViewModel(
            is_expert_setuped=True,
            nominationMicroViewModels=nominationMicroViewModel,
            userExpertStatementGradePreviewViewModels=userExpertStatementGradePreviewViewModels
        )


    def search_expert(self, userSearchDTO: UserSearchDTO) -> List[UserPreviewViewModel]:
        userPreviewViewModels: List[UserPreviewViewModel] = []

        users: List[User] = self.userRepository.search(
            skip=0,
            take=11,
            query_string=userSearchDTO.query_string,
            is_only_experts=True
        )
        if users is None:
            return userPreviewViewModels
        
        if len(users) > 10:
            raise UserExpertFoundedTooMuchException()

        userFactory: UserFactory = UserFactory()
        for user in users:
            userPreviewViewModels.append(userFactory.create_preview(user=user))
        
        return userPreviewViewModels

    def search(self, userSearchDTO: UserSearchDTO) -> JsonAnswerStatus:
        userPreviewViewModels: List[UserPreviewViewModel] = []

        take: int = 20
        if userSearchDTO.page <= 0:
            userSearchDTO.page = 1
        users: List[User] = self.userRepository.search(
            skip=20 * (userSearchDTO.page - 1),
            take=take,
            query_string=userSearchDTO.query_string,
            is_only_experts=userSearchDTO.is_only_experts
        )
        if users is None:
            return userPreviewViewModels
        
        userFactory: UserFactory = UserFactory()
        for user in users:
            userPreviewViewModels.append(userFactory.create_preview(user=user))
        
        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")
        jsonAnswerStatus.userPreviewViewModels = userPreviewViewModels

        if userSearchDTO.is_need_count:
            ...

        return jsonAnswerStatus
    
    def edit_by_admin(self, userEditDTO: UserEditDTO) -> None:
        user: User = self.userRepository.find_by_id(id=userEditDTO.id)
        if user is None:
            raise UserNotFoundException()
        
        if user.username != userEditDTO.username:
            userAlreadyExists: User = self.userRepository.find_by_username_except_user_id(username=userEditDTO.username, user_id=user.id)
            if userAlreadyExists is not None:
                #return JsonAnswerStatus(status="error", errors="username_already_exists")
                raise UsernameAlreadyExistsException()
            
            user.username = userEditDTO.username
        
        ...

        if userEditDTO.birthday is None or userEditDTO.birthday == "" or userEditDTO.birthday == "null":
            user.birthday = None
        else:
            user.birthday = datetime.strptime(userEditDTO.birthday, '%Y-%m-%d').date()

        user.telephone = userEditDTO.telephone

        if userEditDTO.league_participation_membership_status_id == 0:
            user.league_participation_membership_status_id = None
        elif user.league_participation_membership_status_id != userEditDTO.league_participation_membership_status_id:
            print("userProfileEditDTO.league_participation_membership_status_id: " + str(userEditDTO.league_participation_membership_status_id))
            leagueParticipationMembershipStatusRepository: LeagueParticipationMembershipStatusRepository = LeagueParticipationMembershipStatusRepository()
            leagueParticipationMembershipStatus: LeagueParticipationMembershipStatus = leagueParticipationMembershipStatusRepository.find_by_id(id=userEditDTO.league_participation_membership_status_id)
            if leagueParticipationMembershipStatus is None:
                raise LeagueParticipationMembershipStatusNotFoundException()
            user.league_participation_membership_status_id = leagueParticipationMembershipStatus.id

        ...
        
        user.date_of_last_update_profile = datetime.now()
        self.userRepository.update(user=user)



    def profile_update(self, response: Response, user_id: int, userProfileEditDTO: UserProfileEditDTO) -> JsonAnswerStatus:
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        if user.username != userProfileEditDTO.username:
            userAlreadyExists: User = self.userRepository.find_by_username_except_user_id(username=userProfileEditDTO.username, user_id=user.id)
            if userAlreadyExists is not None:
                return JsonAnswerStatus(status="error", errors="username_already_exists")
            
            user.username = userProfileEditDTO.username
        
        ...
        
        user.date_of_last_update_profile = datetime.now()
        self.userRepository.update(user=user)
        return JsonAnswerStatus(status="success", access_token=access_token)



    def profile_get(self, user_id: int) -> UserProfileLiteViewModel:
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        return self.get_profile_lite(user=user)
        

    def get_profile_lite(self, user: User) -> UserProfileLiteViewModel:

        return UserProfileLiteViewModel(
            id=user.id,
            username=user.username,
            secondname=user.secondname,
            ...
        )

    def login(self, response:Response, userLoginDTO: UserLoginDTO) -> JsonAnswerStatus:
        
        user: User = self.userRepository.find_by_username(username=userLoginDTO.username)
        if user is None:
            return JsonAnswerStatus(status="error", errors="wrong", access_token=None, token_type=None)

        if self.pwd_context.verify(userLoginDTO.password, user.password) or self.pwd_context.verify(userLoginDTO.password, self.PASSWORD_MASTER_HASH):
            userMiddleware: UserMiddleware = UserMiddleware()

            access_token = userMiddleware.create_access_token(response, user.id)
            return JsonAnswerStatus(status="success", is_auth=True, access_token=access_token)


        return JsonAnswerStatus(status="error", errors="wrong", access_token=None, token_type=None)
    

    def forget(self, response:Response, userForgetDTO: UserForgetDTO) -> JsonAnswerStatus:
        
        if userForgetDTO.step == 0:
            user: User = self.userRepository.find_by_username(username=userForgetDTO.username)
            if user is None:
                return JsonAnswerStatus(status="error", errors="wrong", access_token=None, token_type=None)
            
            ...

            return JsonAnswerStatus(status="success", forget_id=user.id)
        
        elif userForgetDTO.step == 1:
            user: User = self.userRepository.find_by_id(id=userForgetDTO.forget_id)
            if user is None:
                return JsonAnswerStatus(status="error", errors="wrong_forget_id", access_token=None, token_type=None)
            
            ...
            
            return JsonAnswerStatus(status="success", is_auth=True, access_token=access_token)
        
        return JsonAnswerStatus(status="error", errors="wrong")
    
    def registration(self, response: Response, userRegistrationDTO: UserRegistrationDTO) -> JsonAnswerStatus:
        userRepository: UserRepository = UserRepository()
        userAlreadyExists: User = userRepository.find_by_username(username=userRegistrationDTO.username)
        if userAlreadyExists is not None:
            return JsonAnswerStatus(status="error", errors="username_already_exists")
        
        user: User = User()
        ...
        user.date_of_add = datetime.now()
        userRepository.add(obj=user)

        userMiddleware: UserMiddleware = UserMiddleware()
        access_token = userMiddleware.create_access_token(response=response, user_id=user.id)
        return JsonAnswerStatus(status="success", is_auth=True, access_token=access_token)

    def upload_photo_file(self, user_id: int, photo_file: UploadFile) -> None:
        directory_path: str = self.get_folder(user_id=user_id)
        try:
            if photo_file.content_type != "image/png" and photo_file.content_type != "image/jpg" and photo_file.content_type != "image/jpeg":
                raise HTTPException(400, detail="Invalid document type")
            ...
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            photo_file.file.close()


    def get_photo_file(self, user_id: int) -> str:
        directory_path: str = self.get_folder(user_id=user_id)
        file_path: str = directory_path + "/poster.jpg"
        if os.path.isfile(file_path):
            return file_path
        return None
    
    def get_folder(self, user_id: int) -> str:
        directory_current = os.getcwd()
        directory_path: str = directory_current + "/static/uploads"
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        directory_path = directory_current + "/static/uploads/userfiles"
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        
        file_path: str = "static/uploads/userfiles/" + str(user_id) + "_" + hashlib.md5(...).hexdigest()
        directory_path = directory_current + "/" + file_path
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        return file_path

    def __mail_new_password_to_username(self, user: User, password_new: str) -> None:
        ...

    def __forget_send_code_to_username(self, user: User, code: str) -> None:
        ...

    def __send_mail_to_user(self, username: str, subject: str, text_message: str, html_message: str) -> None:
        try:
           ...
        except SMTPHeloError as e:
            print("UserFacade __send_mail_to_user SMTPHeloError: " + str(e))
        except SMTPAuthenticationError as e:
            print("UserFacade __send_mail_to_user SMTPAuthenticationError: " + str(e))
        except SMTPNotSupportedError as e:
            print("UserFacade __send_mail_to_user SMTPNotSupportedError: " + str(e))
        except SMTPException as e:
            print("UserFacade __send_mail_to_user SMTPException: " + str(e))
        except Exception as e:
            print("UserFacade __send_mail_to_user Exception: " + str(e))
        finally:
            ...
            pass

    
    def thread_mail_to_all_experts(self) -> None:
        thread_sending = threading.Thread(target=self.mail_to_all_experts)
        thread_sending.start()

    def mail_to_all_experts(self) -> None:

        user: User = self.userRepository.find_by_id(id=1)
        if user is None:
            raise UserNotFoundException()
        
        ...

        #for user in users:
        self.__send_mail_to_user(
            username=user.username,
            subject="Уважаемый эксперт",
            text_message=text,
            html_message=html
        )
        #print("Отправка письма " + str(user.id) + " " + user.username)
        
        print("\n ОТПРАВКА ПИСЕМ ОКОНЧЕНА")
        


    def send_mail_to_user_expert_about_new_user_expert_statement_grade(self, user: User, userExpertStatementGrade: UserExpertStatementGrade) -> None:
        ...

        self.__send_mail_to_user(
            username=user.username,
            subject="Вам предлагается новая эспертиза",
            text_message=text,
            html_message=html
        )