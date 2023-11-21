from typing import List

from internal.Entities import Region
from internal.repository.RegionRepository import RegionRepository
from internal.viewmodel.RegionViewModel import RegionMicroViewModel


class RegionFacade:

    def __init__(self) -> None:
        self.regionRepository: RegionRepository = RegionRepository()

    def list_all_micro(self) -> List[RegionMicroViewModel]:
        regions: List[Region] = self.regionRepository.list_all()
        regionMicroViewModels: List[RegionMicroViewModel] = []

        for region in regions:
            regionMicroViewModels.append(
                RegionMicroViewModel(
                    id=region.id,
                    name=region.name
                )
            )
        
        return regionMicroViewModels