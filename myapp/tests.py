import json
from datetime import datetime

from django.test import TestCase, Client
from myapp.models import Courier, Order


def create_couriers():
    c = Client()
    response = c.post('/myapp/couriers', {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "foot",
                "regions": [1, 15],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            },
            {
                "courier_id": 2,
                "courier_type": "bike",
                "regions": [22],
                "working_hours": ["09:00-18:00"]
            },
            {
                "courier_id": 3,
                "courier_type": "car",
                "regions": [22, 23, 33],
                "working_hours": ["07:00-20:00"]
            }
        ]
    })
    return response


def create_orders():
    c = Client()
    response = c.post('/myapp/orders', {
        "data": [
            {
                "order_id": 1,
                "weight": 0.23,
                "region": 33,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 2,
                "weight": 15,
                "region": 1,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 3,
                "weight": 0.01,
                "region": 22,
                "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }
        ]
    })
    return response


class Tests(TestCase):
    def test_post_couriers(self):
        response = create_couriers()
        self.assertIs(response.status_code, 201)
        data = json.loads(response.content)
        couriers = data["couriers"]
        self.assertIs(len(couriers), 3)
        self.assertIs(couriers[0]["id"], 1)
        courier = Courier.objects.get(id=1)
        self.assertEqual(courier.type, "foot")
        self.assertIsNotNone(courier.working_hours)

    def test_bad_request(self):
        c = Client()
        response = c.post('/myapp/orders', {
            "data": [
                {
                    "order_id": 1,
                    "weight": 0.2,
                    "delivery_hours": ["09:00-18:00"]
                }
            ]
        })
        self.assertEqual(response.status_code, 400)

    def test_post_orders(self):
        response = create_orders()
        self.assertIs(response.status_code, 201)
        data = json.loads(response.content)
        orders = data["orders"]
        self.assertIs(len(orders), 3)
        self.assertIs(orders[2]["id"], 3)
        order = Order.objects.get(id=2)
        self.assertEqual(order.region, 1)
        self.assertIsNotNone(order.weight)
        self.assertIsNotNone(order.delivery_hours)

    def test_edit_courier(self):
        c = Client()
        id = 1
        create_couriers()
        courier = Courier.objects.get(id=id)
        self.assertEqual(courier.type, "foot")
        self.assertEqual(courier.working_hours, ["11:35-14:05", "09:00-11:00"])
        self.assertEqual(courier.regions, [1, 15])
        c.patch('/myapp/couriers/'+str(id), {"courier_type": "bike"})
        c.patch('/myapp/couriers/' + str(id), {"working_hours": ["11:35-14:05"]})
        c.patch('/myapp/couriers/' + str(id), {"regions": [2, 11]})
        courier = Courier.objects.get(id=id)
        self.assertEqual(courier.type, "bike")
        self.assertEqual(courier.working_hours, ["11:35-14:05"])
        self.assertEqual(courier.regions, [2, 11])
        response = c.patch('/myapp/couriers/'+str(id), {"how_are_you": "ok"})
        self.assertEqual(response.status_code, 400)

    def test_assign(self):
        c = Client()
        create_orders()
        create_couriers()
        response = c.get('/myapp/orders/assign', {"courier_id": 3})
        data = json.loads(response.content)
        self.assertEqual(data["orders"], [{'id': 3}, {"id": 1}])
        self.assertIsNotNone(data["assign_time"])

    def test_complete(self):
        c = Client()
        create_orders()
        create_couriers()
        c.get('/myapp/orders/assign', {"courier_id": 3})
        response = c.get('/myapp/orders/complete', {
            "courier_id": 3,
            "order_id": 1,
            "complete_time": "2021-01-10T10:33:01.42Z"
        })
        data = json.loads(response.content)
        self.assertEqual(data["order_id"], 1)
        order = Order.objects.get(id=1)
        self.assertEqual(str(order.complete_time.date()), "2021-01-10")
        self.assertEqual(str(order.complete_time.time()), "10:33:01.420000")
