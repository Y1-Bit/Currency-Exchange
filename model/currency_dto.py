class CurrencyDTO:
    def __init__(self, id: int | None, code: str, name: str, sign: str):
        self.id = id
        self.code = code
        self.name = name
        self.sign = sign

