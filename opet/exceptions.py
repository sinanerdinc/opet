class BaseError(Exception):
    pass


class Http200Error(BaseError):
    pass


class ProvinceNotFoundError(BaseError):
    pass
