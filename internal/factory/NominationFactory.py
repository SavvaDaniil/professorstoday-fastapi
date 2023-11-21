from internal.Entities import Nomination
from internal.viewmodel.NominationViewModel import NominationMicroViewModel

class NominationFactory:

    def create_micro(self, nomination: Nomination) -> NominationMicroViewModel:
        
        return NominationMicroViewModel(
            id=nomination.id,
            name=nomination.name
        )