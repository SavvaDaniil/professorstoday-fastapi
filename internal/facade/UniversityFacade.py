from typing import List

from internal.Entities import University
from internal.repository.UniversityRepository import UniversityRepository
from internal.viewmodel.UniversityViewModel import UniversityMicroViewModel

class UniversityFacade:

    def list_all_micro(self) -> List[UniversityMicroViewModel]:
        universityRepository: UniversityRepository = UniversityRepository()
        universities: List[University] = universityRepository.list_all()
        universityMicroViewModels: List[UniversityMicroViewModel] = []
        for university in universities:
            universityMicroViewModels.append(
                UniversityMicroViewModel(
                    id=university.id,
                    name=university.name
                )
            )
        return universityMicroViewModels