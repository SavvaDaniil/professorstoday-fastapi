
import os, hashlib
from typing import List, Union

class StatementUtil:

    def get_statement_file_src(statement_id: int) -> Union[str, None]:
        current_directory: str = os.getcwd()
        folder_path: str = StatementUtil.get_statement_folder_src(statement_id=statement_id)
        statement_file_names: List[str] = [
            "statement.jpg",
            "statement.jpeg",
            ...
        ]
        file_path: str = ""
        for statement_file_name in statement_file_names:
            file_path = folder_path + "/" + statement_file_name
            if os.path.isfile(current_directory + "/" + file_path):
                return file_path
        return None

    def get_statement_folder_src(statement_id: int) -> str:
        directory_current = os.getcwd()
        directory_path: str = directory_current + "/static/uploads"
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        directory_path = directory_current + "/static/uploads/statement"
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

        folder_path: str = "static/uploads/statement/" + str(statement_id) + "_" + hashlib.md5((str(statement_id) + "XXXXXXXXXXXXXXXXXXXXX").encode('000')).hexdigest()
        directory_path = directory_current + "/" + folder_path
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        return folder_path
