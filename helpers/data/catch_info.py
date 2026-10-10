import enum


class CatchType(enum.Enum):
    COMMON = 0
    REGIONAL = 1
    LEGENDARY = 2
    MYTHICAL = 3
    ULTRABEAST = 4


class CatchInfo:
    def __init__(self) -> None:
        self.pokemon: str = ""
        self.level: int = 0
        self.ivs: float = 0
        self.user: str = ""
        self.is_shiny: bool = False
        self.is_hunt: bool = False
        self.is_gmax: bool = False
        self.is_rare: bool = False
        self.type: CatchType = CatchType.COMMON
        self.streak: int = 0
