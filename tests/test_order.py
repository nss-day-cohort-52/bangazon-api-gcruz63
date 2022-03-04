from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product, PaymentType


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        # create a payment type
        self.payment_type = PaymentType.objects.create(
            merchant_name='visa',
            acct_number='1234567899876543',
            customer=self.user1
        )

        self.user2 = User.objects.filter(store=None).last()
        self.product = Product.objects.get(pk=1)

        # self.order1 = Order.objects.create(
        #     user=self.user1
        # )

        # self.order1.products.add(product)

        # self.order2 = Order.objects.create(
        #     user=self.user2
        # )

        # self.order2.products.add(product)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

    # def test_list_orders(self):
    #     """The orders list should return a list of orders for the logged in user"""
    #     response = self.client.get('/api/orders')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)

    # def test_delete_order(self):
    #     response = self.client.delete(f'/api/orders/{self.order1.id}')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # TODO: Complete Order test
    def test_payment_order_(self):
        """ensure acc complete order by adding payment type"""
        orderObject = self.client.get('/api/orders/current')
        orderObject.data["payment_type"] = self.payment_type.id
        print(orderObject.data)
        # initiate put request and capture the response
        response = self.client.put(
            f'/api/orders/{orderObject.data["id"]}/complete', orderObject.data, format="json")

        # assert that response status code is 204 (no content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # initate Get request and capture the responses
        responseOrder = Order.objects.get(pk=2)
        print(responseOrder.payment_type)

        self.assertEqual(responseOrder.payment_type, self.payment_type)
