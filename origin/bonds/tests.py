from rest_framework.test import APITestCase
from datetime import date
from rest_framework import status

from .models import Bond
from django.contrib.auth.models import User


class BondsTestCase(APITestCase):
    def setUp(self):
        self.bob = User.objects.create_user(
            username='bob',
            email='bob@originmarkets.com',
            password='abc123'
        )
        self.john = User.objects.create_user(
            username='john',
            email='bob@originmarkets.com',
            password='abc123'
        )
        self.bob.save()
        self.john.save()

    def test_insert_valid_bond_succeeds(self):
        self.client.force_authenticate(self.bob)
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
        self.assertEqual(Bond.objects.get().author, self.bob)

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
        self.client.force_authenticate(self.bob)
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
        self.client.force_authenticate(self.bob)
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

    def test_user_cant_get_other_user_bond(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'ABC12345'
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(self.john)
        get_resp = self.client.get("/bonds/")
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)

        self.assertEqual(len(get_resp.data), 0)
