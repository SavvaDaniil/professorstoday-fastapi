
from fastapi import Response, UploadFile, HTTPException
from datetime import datetime
from typing import List
import os, hashlib
import logging
from passlib.context import CryptContext
from internal.Entities import Admin
from internal.repository.AdminRepository import AdminRepository
from internal.middleware.AdminMiddleware import AdminMiddleware
from internal.dto.AdminDTO import AdminLoginDTO, AdminProfileEditDTO
from internal.custom_exception.AdminCustomException import AdminNotFoundException, AdminLoginFailedException
from internal.viewmodel.AdminViewModel import AdminProfileLiteViewModel
from internal.viewmodel.JsonAnswerStatus import JsonAnswerStatus
from internal.util.RandomUtil import RandomUtil

class AdminFacade:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self) -> None:
        self.adminRepository: AdminRepository = AdminRepository()
    
    def profile_update(self, response: Response, admin_id: int, adminProfileEditDTO: AdminProfileEditDTO) -> JsonAnswerStatus:
        admin: Admin = self.adminRepository.find_by_id(id=admin_id)
        if admin is None:
            raise AdminNotFoundException()
        
        if admin.username != adminProfileEditDTO.username and admin.username != "" and admin.username is not None:
            adminAlreadyExists: Admin = self.adminRepository.find_by_username_except_user_id(username=adminProfileEditDTO.username, admin_id=admin.id)
            if adminAlreadyExists is not None:
                return JsonAnswerStatus(status="error", errors="username_already_exists")
            
            admin.username = adminProfileEditDTO.username
        
        admin.position = adminProfileEditDTO.position

        access_token: str = None
        if adminProfileEditDTO.password_new is not None and adminProfileEditDTO.password_new != "":
            ...
        
        admin.date_of_last_update_profile = datetime.now()
        self.adminRepository.update(admin=admin)
        return JsonAnswerStatus(status="success", access_token=access_token)


    def login(self, response:Response, adminLoginDTO: AdminLoginDTO) -> str:
        
        admin: Admin = self.adminRepository.find_by_username(username=adminLoginDTO.username)
        if admin is None:
            
            raise AdminLoginFailedException()

        if self.pwd_context.verify(adminLoginDTO.password, admin.password):
            adminMiddleware: AdminMiddleware = AdminMiddleware()

            return adminMiddleware.create_access_token(response, admin.id)

        raise AdminLoginFailedException()

    def get_profile_by_id(self, admin_id: int) -> AdminProfileLiteViewModel:
        admin: Admin = self.adminRepository.find_by_id(id=admin_id)
        if admin is None:
            raise AdminNotFoundException()
        
        return self.get_profile_lite(admin=admin)
    
    def get_profile_lite(self, admin: Admin) -> AdminProfileLiteViewModel:

        return AdminProfileLiteViewModel(
            username=admin.username,
            position=admin.position,
        )