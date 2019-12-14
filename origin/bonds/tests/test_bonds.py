from rest_framework.test import APITestCase
from datetime import date
from rest_framework import status

from bonds.models import Bond
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
            'lei': 'R0MUWSFPU8MPRO8K5P83'
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
        self.assertEqual(my_bond.author, self.bob)
        self.assertEqual(my_bond.legal_name.name, 'BNP PARIBAS')

    def test_get_a_bond_works(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'R0MUWSFPU8MPRO8K5P83'
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
        self.assertEqual(my_bond['author'], 'bob')
        self.assertEqual(my_bond['legal_name'], 'BNP PARIBAS')

    def test_get_multiple_bonds_works(self):
        self.client.force_authenticate(self.bob)
        # This will be inserted twice.
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'R0MUWSFPU8MPRO8K5P83'
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
        self.assertEqual(my_bond['author'], 'bob')
        self.assertEqual(my_bond['legal_name'], 'BNP PARIBAS')

    def test_user_cant_get_other_user_bond(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'R0MUWSFPU8MPRO8K5P83'
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(self.john)
        get_resp = self.client.get("/bonds/")
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)

        self.assertEqual(len(get_resp.data), 0)

# Not happy path tests below
    def test_user_cant_save_a_bond_with_inexistent_lei(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'ahahidontexist'
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_user_cant_save_a_bond_without_a_lei(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': None
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_user_cant_save_a_bond_without_a_valid_lei(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'foobar'
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_user_cant_override_the_author_field(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'R0MUWSFPU8MPRO8K5P83',
            'author': self.john.id
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bond.objects.count(), 1)
        self.assertEqual(Bond.objects.get().author, self.bob)

    def test_user_cant_save_bond_that_matures_in_the_past(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'EUR',
            'maturity': '2018-01-01',
            'lei': 'R0MUWSFPU8MPRO8K5P83'
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_save_bond_with_invalid_currency(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 1000,
            'currency': 'ZZZ',
            'maturity': '2030-01-01',
            'lei': 'R0MUWSFPU8MPRO8K5P83'
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_save_bond_with_negative_size(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': -20,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'R0MUWSFPU8MPRO8K5P83'
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_save_bond_with_zero_size(self):
        self.client.force_authenticate(self.bob)
        data = {
            'isin': 'US0378331005',
            'size': 0,
            'currency': 'EUR',
            'maturity': '2030-01-01',
            'lei': 'R0MUWSFPU8MPRO8K5P83'
        }
        resp = self.client.post("/bonds/", data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
