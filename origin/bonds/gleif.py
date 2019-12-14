"""
Abstraction of the GLEIF API to get information about the
LEI numbers.
"""

import requests


class InvalidLeiError(Exception):
    pass


class LeiRequestError(Exception):
    pass


def get_entity_name(lei):
    if lei is None or lei == '':
        raise InvalidLeiError()
    resp = requests.get(
        'https://leilookup.gleif.org/api/v2/leirecords?lei={}'.format(lei)
    )

    if resp.status_code != 200:
        raise LeiRequestError()

    return resp.json()[0]['Entity']['LegalName']['$']
