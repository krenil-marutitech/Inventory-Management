msg = {
    "inventory_not_exists": "Inventory with name: '{}' does not exist.",
    "no_inventory_in_category": "There are no inventories found in '{}' category.",
    "inventory_already_exists": "Inventory with name: '{}' already exists.",
    "error_insertion": "There is some error occurred in inserting data.",
    "inventory_deletion": "Inventory with name: '{}' is deleted successfully."
}


def get_msg(text: str):
    return msg[text]
