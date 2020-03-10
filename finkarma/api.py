import requests


class FinkarmaError(requests.HTTPError):
    pass


class FinkarmaApi:
    def __init__(self, key):
        self.key = key
        self.REQUEST_URL = f'https://finkarma.com.ua/api/v1/blacklists/?key={self.key}'

    def _make_request(self, data):
        response = requests.post(self.REQUEST_URL, data=data)
        if response.status_code == 200:
            return response.json()
        raise FinkarmaError(response=response)

    def check_person_exists(self,
                            mobile_phone=None,
                            passport_series=None,
                            passport_number=None,
                            okpo=None,
                            number_id_card=None,
                            ):
        """
        :param mobile_phone:
        :param passport_series:
        :param passport_number:
        :param okpo:
        :param number_id_card:
        :return: Boolean - does person exists in Finkarma blacklist
        """
        if not any([mobile_phone, passport_series, passport_number, okpo, number_id_card]):
            raise ValueError('At least one argument is required.')
        data = dict(
            mobile_phone=mobile_phone,
            passport_series=passport_series,
            passport_number=passport_number,
            okpo=okpo,
            number_id_card=number_id_card
        )

        cleaned_data = {k: v for k, v in data.items() if v is not None}

        if None in [passport_series, passport_number]:
            cleaned_data.pop(passport_series, '')
            cleaned_data.pop(passport_number, '')

        """
            result example
            {
            "available": true / false
            }
        """
        result = self._make_request(cleaned_data)
        available = result.get('available')
        if type(available) is str:
            available = available in ['True', 'true']
        return bool(available)

