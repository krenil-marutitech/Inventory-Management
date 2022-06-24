import unittest
import requests

local_url = "http://127.0.0.1:5000/"

sample_get_response = {
    "manufacturing_time": "2020-12-30T09:13:34",
    "inventory_id": 7,
    "inventory_name": "item-6",
    "inventory_category": "cat-c",
    "expiry_time": "2022-12-30T09:13:34",
    "quantity": 2
}

sample_post_response = {
    "inventory_category": "cat-d",
    "quantity": 2,
    "manufacturing_time": "2020-12-30 09:13:34.0",
    "expiry_time": "2022-12-30 09:13:34.0"
}

sample_update_response = {
    "quantity": 45,
    "manufacturing_time": "2020-12-30T09:13:34",
    "expiry_time": "2022-12-30T09:13:34",
    "inventory_id": 1,
    "inventory_name": "item-pqr",
    "inventory_category": "cat-c"
}


class TestInventoryResource(unittest.TestCase):
    def test_fetch_single_inventory(self):
        response = requests.get(local_url + "/inventory/item-6")
        self.assertEqual(response.json(), sample_get_response)
        self.assertEqual(response.status_code, 200)

    def test_fetch_by_category(self):
        response = requests.get(local_url + "/category/cat-c")
        self.assertEqual(response.json(), sample_get_response)
        self.assertEqual(response.status_code, 200)

    def test_fetch_all_inventories(self):
        response = requests.get(local_url + "/inventories")
        self.assertEqual(response.status_code, 200)

    def test_create_inventory(self):
        response = requests.post(local_url + "/inventory/item-13", json=sample_post_response)
        self.assertEqual(response.status_code, 201)

    def test_delete_inventory(self):
        response = requests.delete(local_url + "/inventory/item-7")
        self.assertEqual(response.status_code, 200)

    def test_update_inventory(self):
        response = requests.put(local_url + "/inventory/2", json=sample_update_response)
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
