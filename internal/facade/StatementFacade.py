from datetime import datetime
import os, hashlib
from fastapi import HTTPException, UploadFile
from typing import Union, List
import pandas as pd
from pandas import DataFrame, ExcelWriter
import io
from io import BytesIO
from dataclasses import asdict

from internal.Entities import Contest, User, Statement, Nomination, Region, UserExpertStatementGrade, University, LeagueParticipationMembershipStatus
from internal.dto.StatementDTO import UserStatementEditDTO, StatementSearchDTO
from internal.repository.StatementRepository import StatementRepository
from internal.repository.ContestRepository import ContestRepository
from internal.repository.UserRepository import UserRepository
from internal.repository.NominationRepository import NominationRepository
from internal.repository.RegionRepository import RegionRepository
from internal.repository.UserExpertStatementGradeRepository import UserExpertStatementGradeRepository
from internal.repository.LeagueParticipationMembershipStatusRepository import LeagueParticipationMembershipStatusRepository
from internal.facade.UserFacade import UserFacade
from internal.facade.NominationFacade import NominationFacade
from internal.facade.LeagueParticipationMembershipStatusFacade import LeagueParticipationMembershipStatusFacade
from internal.facade.RegionFacade import RegionFacade
from internal.facade.UniversityFacade import UniversityFacade
from internal.factory.UserFactory import UserFactory
from internal.factory.StatementFactory import StatementFactory
from internal.factory.NominationFactory import NominationFactory
from internal.factory.UserExpertStatementGradeFactory import UserExpertStatementGradeFactory
from internal.custom_exception.UserCustomException import UserNotFoundException
from internal.custom_exception.ContestCustomException import ContestNotFoundException
from internal.custom_exception.StatementCustomException import StatementNotFoundException
from internal.custom_exception.NominationCustomException import NominationNotFoundException
from internal.custom_exception.RegionCustomException import RegionNotFoundException
from internal.custom_exception.UserExpertStatementGradeException import UserExpertStatementGradeNotFoundException
from internal.viewmodel.StatementViewModel import UserStatementViewModel, UserStatementApplicationsAndCharacteristicsFileViewModel, UserStatementOtherFileViewModel, StatementPreviewViewModel, UserStatementExcelRowViewModel
from internal.viewmodel.UserExpertStatementGradeViewModel import UserExpertStatementGradeEditViewModel
from internal.viewmodel.NominationViewModel import NominationMicroViewModel
from internal.viewmodel.UserViewModel import UserProfileLiteViewModel
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus

class StatementFacade:

    def __init__(self) -> None:
        self.userRepository: UserRepository = UserRepository()
        self.contestRepository: ContestRepository = ContestRepository()
        self.statementRepository: StatementRepository = StatementRepository()
        self.nominationRepository: NominationRepository = NominationRepository()
        self.regionRepository: RegionRepository = RegionRepository()
        self.AVAILABLE_FILE_TYPES: List[str] = ["jpg", "jpeg", "png", "webp", "pdf"]

    
    def search(self, statementSearchDTO: StatementSearchDTO) -> JsonAnswerStatus:
        statementPreviewViewModels: List[StatementPreviewViewModel] = []

        jsonAnswerStatus: JsonAnswerStatus = JsonAnswerStatus(status="success")

        take: int = 20
        if statementSearchDTO.page <= 0:
            statementSearchDTO.page = 1
        statements: List[Statement] = self.statementRepository.search(
            skip=20 * (statementSearchDTO.page - 1),
            take=take,
            query_string=statementSearchDTO.query_string,
            status=statementSearchDTO.status,
            nomination_id=statementSearchDTO.nomination_id,
            region_id=statementSearchDTO.region_id,
            university_id=statementSearchDTO.university_id
        )
        if statements is None:
            jsonAnswerStatus.statementPreviewViewModels = statementPreviewViewModels
            return jsonAnswerStatus
        
        statementFactory: StatementFactory = StatementFactory()
        for statement in statements:
            statementPreviewViewModels.append(statementFactory.create_preview(statement=statement))
        
        jsonAnswerStatus.statementPreviewViewModels = statementPreviewViewModels

        if statementSearchDTO.is_need_count:
            jsonAnswerStatus.count_statement_search_query = self.statementRepository.count_by_filter(
                query_string=statementSearchDTO.query_string,
                status=statementSearchDTO.status,
                nomination_id=statementSearchDTO.nomination_id,
                region_id=statementSearchDTO.region_id,
                university_id=statementSearchDTO.university_id
            )

        if statementSearchDTO.is_need_statistic:
            jsonAnswerStatus.count_statement_status_0 = self.statementRepository.count_by_filter(
                query_string=None,
                status=1
            )
            jsonAnswerStatus.count_statement_status_1 = self.statementRepository.count_by_filter(
                query_string=None,
                status=2
            )
            
            nominationFacade: NominationFacade = NominationFacade()
            regionFacade: RegionFacade = RegionFacade()
            universityFacade: UniversityFacade = UniversityFacade()

            jsonAnswerStatus.nominationMicroViewModels = nominationFacade.list_micro()
            jsonAnswerStatus.regionMicroViewModels=regionFacade.list_all_micro()
            jsonAnswerStatus.universityMicroViewModels = universityFacade.list_all_micro()

        return jsonAnswerStatus
    

    def expert_get_grade_by_id(self, user_expert_id: int, user_expert_statement_grade_id: int) -> UserExpertStatementGradeEditViewModel:
        userExpertStatementGradeRepository: UserExpertStatementGradeRepository = UserExpertStatementGradeRepository()
        userExpertStatementGrade: UserExpertStatementGrade = userExpertStatementGradeRepository.find_by_id(id=user_expert_statement_grade_id)
        if userExpertStatementGrade is None or userExpertStatementGrade.user_expert_id != user_expert_id:
            raise UserExpertStatementGradeNotFoundException()
        
        return self.expert_get_grade(userExpertStatementGrade=userExpertStatementGrade)
        
    def expert_get_grade(self, userExpertStatementGrade: UserExpertStatementGrade) -> UserExpertStatementGradeEditViewModel:
        statement: Statement = userExpertStatementGrade.statement
        if statement is None:
            raise StatementNotFoundException()
        
        nomination: Nomination = statement.nomination
        if nomination is None:
            raise NominationNotFoundException()

        user: User = statement.user
        if user is None:
            raise UserNotFoundException()
        userFactory: UserFactory = UserFactory()
        
        contest: Contest = statement.contest
        
        nominationFactory: NominationFactory = NominationFactory()
        nominationMicroViewModel: NominationMicroViewModel = nominationFactory.create_micro(nomination=nomination)
        userProfileLiteViewModel: UserProfileLiteViewModel = userFactory.create_profile_lite(user=user)
        userStatementViewModel: UserStatementViewModel = self.get(user=user, contest=contest, statement=statement)

        userExpertStatementGradeFactory: UserExpertStatementGradeFactory = UserExpertStatementGradeFactory()

        return userExpertStatementGradeFactory.create_edit(
            userExpertStatementGrade=userExpertStatementGrade,
            nominationMicroViewModel=nominationMicroViewModel,
            userProfileLiteViewModel=userProfileLiteViewModel,
            userStatementViewModel=userStatementViewModel
        )

    def confirm_by_user(self, user_id: int, statement_id: int) -> JsonAnswerStatus:
        
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        statement: Statement = self.statementRepository.find_by_id(id=statement_id)
        if statement is None or statement.user_id != user_id:
            raise StatementNotFoundException()
        
        ...
        
        statement.status = 1
        statement.date_of_update = datetime.now()
        self.statementRepository.update(statement=statement)
        return JsonAnswerStatus(status="success")


    def withdraw_by_user(self, user_id: int, contest_id: int) -> JsonAnswerStatus:
        
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        ...
        
        statement.status = 0
        statement.date_of_update = datetime.now()
        self.statementRepository.update(statement=statement)
        return JsonAnswerStatus(status="success")




    def update(self, user_id: int, userStatementEditDTO: UserStatementEditDTO) -> JsonAnswerStatus:
        
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        statement: Statement = self.statementRepository.find_by_id(id=userStatementEditDTO.id)
        if statement is None:
            raise StatementNotFoundException()
        
        if userStatementEditDTO.nomination_id != 0 and statement.nomination_id != userStatementEditDTO.nomination_id:
            nomination: Nomination = self.nominationRepository.find_by_id(id=userStatementEditDTO.nomination_id)
            if nomination is None:
                raise NominationNotFoundException()
            statement.nomination_id = userStatementEditDTO.nomination_id

        if userStatementEditDTO.statement_file is not None:
            directory_path: str = self.get_statement_folder_src(statement_id=statement.id)
            self.delete_statement_file(statement_id=statement.id)

            try:

                file_type: str = ""
                if userStatementEditDTO.statement_file.content_type == "image/png":
                    file_type = "png"
                elif userStatementEditDTO.statement_file.content_type == "image/jpg":
                    file_type = "jpg"
                    ...
                else:
                    raise HTTPException(400, detail="Invalid document type")
                contents = userStatementEditDTO.statement_file.file.read()
                with open(directory_path + "/statement." + file_type, 'wb') as f:
                    f.write(contents)
            except HTTPException:
                return JsonAnswerStatus(status="error", errors="Неверный формат файла")
            except Exception:
                return {"message": "There was an error uploading the file"}
            finally:
                userStatementEditDTO.statement_file.file.close()
            
        #загрузка фото
        if userStatementEditDTO.photo_file is not None:
            userFacade: UserFacade = UserFacade()
            userFacade.upload_photo_file(user_id=user.id, photo_file=userStatementEditDTO.photo_file)

        if userStatementEditDTO.applications_and_characteristics_file is not None:
            self.upload_single_statement_applications_and_characteristic(
                statement_id=statement.id,
                applications_and_characteristics_file=userStatementEditDTO.applications_and_characteristics_file
            )

        if userStatementEditDTO.other_file is not None:
            self.upload_single_other_file(
                statement_id=statement.id,
                other_file=userStatementEditDTO.other_file
            )

        #загрузка заявления на разрешение обработки персональных данных
        if userStatementEditDTO.process_data_application_file is not None:
            self.upload_process_data_application(
                statement_id=statement.id,
                process_data_application_file=userStatementEditDTO.process_data_application_file
            )

        #page 2
        statement.education = userStatementEditDTO.education
        ...

        return JsonAnswerStatus(status="success")
        

    def get_for_admin_by_id(self, statement_id: int) -> UserStatementViewModel:
        statement: Statement = self.statementRepository.find_by_id(id=statement_id)
        if statement is None:
            raise StatementNotFoundException()
        
        return self.get(
            user=None,
            contest=None,
            statement=statement
        )

    def get_for_user(self, user_id: int, contest_id: int) -> UserStatementViewModel:
        
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        contest: Contest = self.contestRepository.find_by_id(id=contest_id)
        if contest is None:
            raise ContestNotFoundException()
        
        statement: Statement = self.statementRepository.find_by_user_id_and_contest_id(user_id=user.id, contest_id=contest.id)
        if statement is None:
            statement = Statement()
            statement.user_id = user_id
            statement.contest_id = contest_id

            ...

            statement = self.statementRepository.add(obj=statement)

        return self.get(user=user, contest=contest, statement=statement)
        
    def get(self, user: Union[User, None], contest: Union[Contest, None], statement: Statement) -> UserStatementViewModel:

        if user is None:
            user = statement.user
        
        if contest is None:
            contest = statement.contest

        nomination: Union[Nomination, None] = None
        if statement.nomination_id != 0 and statement.nomination is not None:
            nomination = statement.nomination

        userFacade: UserFacade = UserFacade()

        userFactory: UserFactory = UserFactory()
        nominationFactory: NominationFactory = NominationFactory()

        userStatementViewModel: UserStatementViewModel = UserStatementViewModel(
            id=statement.id,
            user_id=user.id,
            userProfileLiteViewModel=(userFactory.create_profile_lite(user=user) if user is not None else None),
            contest_id=contest.id,

            status=statement.status,

            statement_file_src=self.get_statement_file_src(statement_id=statement.id),
            photo_file_src=userFacade.get_photo_file(user_id=user.id),
            nomination_id=(statement.nomination_id if statement.nomination_id is not None else 0),
            nominationMicroViewModel=(nominationFactory.create_micro(nomination=nomination) if nomination is not None else None),

            #page 2
            ...
        )

        return userStatementViewModel
    
    def get_statement_file_src(self, statement_id: int) -> str:
        current_directory: str = os.getcwd()
        folder_path: str = self.get_statement_folder_src(statement_id=statement_id)
        statement_file_names: List[str] = [
            "statement.jpg",
            ...
        ]
        file_path: str = ""
        for statement_file_name in statement_file_names:
            file_path = folder_path + "/" + statement_file_name
            if os.path.isfile(current_directory + "/" + file_path):
                return file_path
        return None
    
    def upload_single_statement_applications_and_characteristic(self, statement_id: int, applications_and_characteristics_file: UploadFile) -> None:
        if applications_and_characteristics_file is None:
            return
        
        list_of_already_uploaded_files: List[UserStatementApplicationsAndCharacteristicsFileViewModel] = self.list_of_statement_applications_and_characteristics(statement_id=statement_id)
        if len(list_of_already_uploaded_files) >= 40:
            return
        
        directory_current: str = os.getcwd()
        statement_applications_and_characteristics_folder_src: str = self.get_statement_applications_and_characteristics_folder_src(statement_id=statement_id)
        next_file_name: str = ""
        file_type: str = ""
        
        file_type = self.__get_file_type_by_content_type(content_type=applications_and_characteristics_file.content_type)
        #print("file_type: " + file_type)
        if file_type is None:
            raise HTTPException(400, detail="Invalid document type")
        next_file_name = self.__get_available_number_filename_of_applications_and_characteristics_for_saving_max_40(statement_id=statement_id)
        if next_file_name is None:
            #print("next_file_name IS NONE")
            return

        try:
            contents = applications_and_characteristics_file.file.read()
            ...
        except Exception as e:
            print(e)
            return {"message": "There was an error uploading the file"}
        finally:
            applications_and_characteristics_file.file.close()


    def upload_statement_applications_and_characteristics(self, statement_id: int, applications_and_characteristics_files: List[UploadFile]) -> None:
        if applications_and_characteristics_files is None:
            return
        
        list_of_already_uploaded_files: List[UserStatementApplicationsAndCharacteristicsFileViewModel] = self.list_of_statement_applications_and_characteristics(statement_id=statement_id)
        if len(list_of_already_uploaded_files) >= 40:
            #print("upload_statement_applications_and_characteristics len(list_of_already_uploaded_files) >= 10")
            return
        
        directory_current: str = os.getcwd()
        statement_applications_and_characteristics_folder_src: str = self.get_statement_applications_and_characteristics_folder_src(statement_id=statement_id)
        next_file_name: str = ""
        file_type: str = ""
        for applications_and_characteristics_file in applications_and_characteristics_files:
            file_type = self.__get_file_type_by_content_type(content_type=applications_and_characteristics_file.content_type)
            if file_type is None:
                raise HTTPException(400, detail="Invalid document type")
            next_file_name = self.__get_available_number_filename_of_applications_and_characteristics_for_saving_max_40(statement_id=statement_id)
            if next_file_name is None:
                break

            try:
                contents = applications_and_characteristics_file.file.read()
                ...
            except Exception as e:
                print(e)
                return {"message": "There was an error uploading the file"}
            finally:
                applications_and_characteristics_file.file.close()
            

    def list_of_statement_applications_and_characteristics(self, statement_id: int) -> List[UserStatementApplicationsAndCharacteristicsFileViewModel]:
        ...

        return list_of_files
    
    def __get_available_number_filename_of_applications_and_characteristics_for_saving_max_40(self, statement_id: int) -> Union[str, None]:
        ...


    #For other files BEGIN
    
    def upload_single_other_file(self, statement_id: int, other_file: UploadFile) -> None:
        ...
    
    def upload_other_files(self, statement_id: int, other_files: List[UploadFile]) -> None:
       ...

    def list_of_other_files(self, statement_id: int) -> List[UserStatementOtherFileViewModel]:
        ...
    
    def __get_available_number_filename_of_others_for_saving_max_40(self, statement_id: int) -> Union[str, None]:
        ...
        
    
    def delete_other_file_by_index(self, user_id: int, statement_id: int, file_index: str) -> bool:
        
        user: User = self.userRepository.find_by_id(id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        statement: Statement = self.statementRepository.find_by_id(id=statement_id)
        if statement is None or statement.user_id != user_id:
            raise StatementNotFoundException()
        
        statement_other_files_folder_src: str = self.get_statement_other_files_folder_src(statement_id=statement_id)
        directory_current: str = os.getcwd()
        file_path: str = ""
        for available_file_type in self.AVAILABLE_FILE_TYPES:
            file_path = statement_other_files_folder_src + "/" + file_index + "." + available_file_type
            if os.path.isfile(directory_current + "/" + file_path):
                os.remove(directory_current + "/" + file_path)
                return True
        return False

    #For other files END
    
    def upload_process_data_application(self, statement_id: int, process_data_application_file: UploadFile) -> None:
        ...
    
    def get_process_data_application_file_src(self, statement_id: int) -> str:
        ...


    def get_statement_folder_src(self, statement_id: int) -> str:
        directory_current = os.getcwd()
        #print("directory: " + str(directory_current))
        #path = os.path.join(parent_dir, directory)
        directory_path: str = directory_current + "/static/uploads"
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        directory_path = directory_current + "/static/uploads/statement"
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

        folder_path: str = "static/uploads/statement/" + str(statement_id) + "_" + hashlib.md5(...).encode('utf-8')).hexdigest()
        directory_path = directory_current + "/" + folder_path
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        return folder_path
    
    def get_statement_applications_and_characteristics_folder_src(self, statement_id: int) -> str:
        statement_folder_src: str = self.get_statement_folder_src(statement_id=statement_id)
        directory_current = os.getcwd()
        statement_applications_and_characteristics_folder_src: str = statement_folder_src + "/applications_and_characteristics"
        directory_path: str = directory_current + "/" + statement_applications_and_characteristics_folder_src
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        return statement_applications_and_characteristics_folder_src
    
    def get_statement_other_files_folder_src(self, statement_id: int) -> str:
        ...
    
    def __rename_statement_folder_to_crypt_if_prev_exists(self, statement_id: int) -> None:
        ...


    def __is_file_type_granted(self, file_type: str) -> bool:
        return file_type == "image/png" or file_type == "image/jpg" or file_type == "image/jpeg" or file_type == "image/webp" or file_type == "application/pdf"

    def __get_file_type_by_content_type(self, content_type: str) -> Union[str, None]:
        if content_type == "image/jpg" or content_type == "image/jpeg":
            return "jpg"
        elif content_type == "image/png":
            return "png"
        elif content_type == "image/webp":
            return "webp"
        elif content_type == "application/pdf":
            return "pdf"
        else:
            return None
        
    
    def delete_statement_file(self, statement_id: int) -> None:
        ...
    
    def delete_statement_applications_and_characteristics_by_index(self, user_id: int, statement_id: int, file_index: str) -> bool:
        ...



    def generate_excel_by_filter(self) -> BytesIO:

        statements: List[Statement] = self.statementRepository.search(
            skip=0,
            take=1400,
            query_string=None,
            status=2
        )

        userStatementExcelRowViewModels: List[UserStatementExcelRowViewModel] = []
        user: User = None
        nomination: Nomination = None
        university: University = None
        leagueParticipationMembershipStatus: LeagueParticipationMembershipStatus = None
        region: Region = None
        league_participation_is_membership: Union[str, None] = None


        userExpertStatementGradeRepository: UserExpertStatementGradeRepository = UserExpertStatementGradeRepository()
        userExpertStatementGrades: List[UserExpertStatementGrade] = []

        userExpertStatementGrades_data: List[tuple(Union[str, None], Union[str, None])] = []
        userExpertStatementGradesCount: int = 0
        userExpertStatementGradePointsSum: int = 0
        userExpertStatementGradePointsAverage: float = 0.0

        user_gender: Union[str, None] = None

        for statement in statements:

            user = statement.user if statement.user is not None else None
            region = user.region if user is not None else None
            university = user.university if user is not None else None
            leagueParticipationMembershipStatus = user.league_participation_membership_status if user is not None else None
            nomination = statement.nomination if statement.nomination is not None else None

            userExpertStatementGrades = userExpertStatementGradeRepository.list_appreciated_by_statement_id(statement_id=statement.id)

            userExpertStatementGrades_data = []
            userExpertStatementGradesCount = 0
            userExpertStatementGradePointsSum = 0
            userExpertStatementGradePointsAverage = 0.0

            for userExpertStatementGrade in userExpertStatementGrades:
                userExpertStatementGradesCount += 1
                userExpertStatementGradePointsSum += userExpertStatementGrade.points
                userExpertStatementGrades_data.append(
                    (
                        userExpertStatementGrade.comment,
                        str(userExpertStatementGrade.points)
                    )
                )
            
            if userExpertStatementGradesCount > 0:
                userExpertStatementGradePointsAverage = userExpertStatementGradePointsSum / userExpertStatementGradesCount

            if user.gender == 1:
                user_gender = "Женский"
            elif user.gender == 2:
                user_gender = "Мужской"
            else:
                user_gender = ""

            if user.league_participation_is_membership == 2:
                league_participation_is_membership = "Являюсь участником Лиги Преподавателей Высшей Школы"
            elif user.league_participation_is_membership == 1:
                league_participation_is_membership = "Не являюсь участником Лиги Преподавателей Высшей Школы"
            else:
                league_participation_is_membership = ""

            userStatementExcelRowViewModels.append(
                UserStatementExcelRowViewModel(
                    id=statement.id,
                    #user_id_fio=(str(user.id) + " " + user.secondname + " " + user.firstname + " " + user.patronymic if user is not None else "<Не определено>"),
                    username=user.username,
                    secondname=user.secondname,
                    firstname=user.firstname,
                    patronymic=user.patronymic,

                    gender=user_gender,
                    birthday=(user.birthday.strftime("%Y-%m-%d") if user.birthday is not None else None),
                    telephone=user.telephone,
                    region=region.name if region is not None else None,
                    address=user.address,
                    university=university.name if university is not None else None,
                    position_not_university=user.position_not_university,

                    league_participation_is_membership=league_participation_is_membership,
                    league_participation_membership_status=leagueParticipationMembershipStatus.name if leagueParticipationMembershipStatus is not None else None,


                    status="Отправлено" if statement.status == 1 else "Не отправлено",

                    nomination_name=(nomination.name if nomination is not None else "<Не определено>"),
                    
                    #page 2
                    ...
                )
            )

        df: DataFrame = pd.DataFrame.from_records(
            data=[asdict(s) for s in userStatementExcelRowViewModels]
        )
        
        df.columns=[
            "ID",

            "Login",
            ...
        ]
        #df = df.set_index("ID")

        output: BytesIO = io.BytesIO()
        writer: ExcelWriter = pd.ExcelWriter(output, engine='xlsxwriter')
            
        result = df.to_excel(writer)
        writer.close()
        xlsx_data = output.getvalue()

        return io.BytesIO(xlsx_data)