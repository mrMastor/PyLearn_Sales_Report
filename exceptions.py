from fastapi import HTTPException

class UniqueViolationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=422, detail=message)

class ForeignKeyViolationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)