
from typing import List

from internal.Entities import Nomination
from internal.repository.NominationRepository import NominationRepository
from internal.viewmodel.NominationViewModel import NominationMicroViewModel

class NominationFacade:

    def __init__(self) -> None:
        self.nominationRepository: NominationRepository = NominationRepository()

    def list_micro(self) -> List[NominationMicroViewModel]:

        nominations: List[Nomination] = self.nominationRepository.list_all()
        nominationMicroViewModels: List[NominationMicroViewModel] = []

        for nomination in nominations:
            nominationMicroViewModels.append(
                NominationMicroViewModel(
                    id=nomination.id,
                    name=nomination.name
                )
            )

        return nominationMicroViewModels