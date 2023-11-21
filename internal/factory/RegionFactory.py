
from internal.Entities import Region
from internal.viewmodel.RegionViewModel import RegionMicroViewModel

class RegionFactory:

    def create_micro(self, region: Region) -> RegionMicroViewModel:
        return RegionMicroViewModel(
            id=region.id,
            name=region.name
        )