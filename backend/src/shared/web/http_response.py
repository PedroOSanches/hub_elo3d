from src.shared.web.interface.response_interface import IResponse


class HttpResponse(IResponse):
    status_code: int
    body: dict
    headers: dict

    data: dict

    def __init__(self, status_code: int, body: dict = {}, headers: dict = {}, data: dict = {}):
        self.status_code = status_code
        self.body = body or data
        self.headers = headers

        data_dict = {}

        if type(body) is dict:
            data_dict.update(body)
        if type(body) is str:
            data_dict.update({'body': body})

        data_dict.update(headers)
        self.data = data_dict

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, value: dict):
        self._data = value

    @property
    def status_code(self) -> dict:
        return self._status_code

    @status_code.setter
    def status_code(self, value: dict):
        self._status_code = value

    def __repr__(self):
        return (
            f"HttpResponse (status_code={self.status_code}, body={self.body}, headers={self.headers})"
        )



