from rest_framework.test import APITestCase
from datetime import date
from rest_framework import status

from .models import Bond


class BondsTestCase(APITestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200

    def test_insert_valid_bond_succeeds(self):
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'ABC12345'
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bond.objects.count(), 1)
        my_bond = Bond.objects.get()
        self.assertEqual(my_bond.isin, data['isin'])
        self.assertEqual(my_bond.size, data['size'])
        self.assertEqual(my_bond.currency, data['currency'])
        self.assertEqual(
            my_bond.maturity,
            date.fromisoformat(data['maturity'])
        )
        self.assertEqual(my_bond.lei, data['lei'])

    def test_get_a_bond_works(self):
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'ABC12345'
        }
        post_resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(post_resp.status_code, status.HTTP_201_CREATED)

        get_resp = self.client.get("/bonds/{}/".format(post_resp.data['id']))
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)

        my_bond = get_resp.data
        self.assertEqual(my_bond['isin'], data['isin'])
        self.assertEqual(my_bond['size'], data['size'])
        self.assertEqual(my_bond['currency'], data['currency'])
        self.assertEqual(my_bond['maturity'], data['maturity'])
        self.assertEqual(my_bond['lei'], data['lei'])

    def test_get_multiple_bonds_works(self):
        # This will be inserted twice.
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'ABC12345'
        }
        post_resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(post_resp.status_code, status.HTTP_201_CREATED)
        post_resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(post_resp.status_code, status.HTTP_201_CREATED)

        get_resp = self.client.get("/bonds/")
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_resp.data), 2)

        # Checking only the first item.
        my_bond = get_resp.data[0]
        self.assertEqual(my_bond['isin'], data['isin'])
        self.assertEqual(my_bond['size'], data['size'])
        self.assertEqual(my_bond['currency'], data['currency'])
        self.assertEqual(my_bond['maturity'], data['maturity'])
        self.assertEqual(my_bond['lei'], data['lei'])
