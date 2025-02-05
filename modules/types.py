from enum import Enum, unique

@unique
class Filter(Enum):
    RentType = "rent-type"
    EarliestMove = "earliest-move"
    Searched = "searched"
    MyAge = "my-age"
    WithPhotos = "with-photos"

@unique
class LogStatus(Enum):
    Success = "Success"
    Warning = "Warning"
    Error = "Error"
