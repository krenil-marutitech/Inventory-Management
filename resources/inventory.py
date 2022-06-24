import datetime

from flask import request
from flask_restful import Resource

from schema.inventory import InventorySchema
from models.inventory import InventoryModel
from strings import err_msg
from time_con import convert_date_into_cst, remove_trunk
from app import logger

inventory_schema = InventorySchema()
inventory_list_schema = InventorySchema(many=True)


class Inventory(Resource):
    @classmethod
    def get(cls, inventory_name: str):
        logger.info("Fetch a single inventory by 'inventory_name'")
        inventory = InventoryModel.find_by_name(inventory_name)
        if inventory:
            logger.debug("Checking product expiry.")
            if str(datetime.datetime.now()) > str(inventory.expiry_time):
                logger.info("Inventory is expired.")
                return {"Alert": "Inventory is expired.", "inventory": inventory_schema.dump(inventory)}, 200
            logger.info("Successfully fetched one inventory.")
            return inventory_schema.dump(inventory), 200
        logger.error("Inventory not found in the database.")
        return {"message": err_msg.get_msg("inventory_not_exists").format(inventory_name)}, 404

    @classmethod
    def post(cls, inventory_name: str):
        logger.info("Creating new inventory.")
        if InventoryModel.find_by_name(inventory_name):
            logger.warn("Two inventories can not have same names.")
            return {"message": err_msg.get_msg("inventory_already_exists").format(inventory_name)}, 400

        inventory_json = request.get_json()
        inventory_json["inventory_name"] = inventory_name

        # Time conversion to CST
        inventory_json["manufacturing_time"] = remove_trunk(
            convert_date_into_cst(inventory_json["timezone"],
                                  inventory_json["manufacturing_time"]))
        inventory_json["expiry_time"] = remove_trunk(
            convert_date_into_cst(inventory_json["timezone"],
                                  inventory_json["expiry_time"]))

        inventory = inventory_schema.load(inventory_json)
        try:
            inventory.save_to_db()
        except:
            logger.error("Error occurred at the time of inserting the data.")
            return {"message": err_msg.get_msg("error_insertion")}, 500

        logger.info("Successfully saved new inventory to the database.")
        return inventory_schema.dump(inventory), 201

    @classmethod
    def delete(cls, inventory_name: str):
        logger.info("Starting deleting inventory.")
        inventory = InventoryModel.find_by_name(inventory_name)
        if inventory:
            logger.info("Inventory found and successfully deleted from the database.")
            inventory.delete_from_db()
            return {"message": err_msg.get_msg("inventory_deletion").format(inventory_name)}, 200
        logger.info("Inventory does not exist in the database.")
        return {"message": err_msg.get_msg("inventory_not_exists").format(inventory_name)}, 404


class UpdateInventory(Resource):
    @classmethod
    def put(cls, inventory_id: int):
        logger.info("Update inventory information by 'inventory_id'.")
        inventory_json = request.get_json()
        inventory = InventoryModel.find_by_id(inventory_id)

        if inventory:
            inventory.inventory_name = inventory_json["inventory_name"]
            inventory.inventory_category = inventory_json["inventory_category"]
            inventory.quantity = inventory_json["quantity"]
            inventory.manufacturing_time = inventory_json["manufacturing_time"]
            inventory.expiry_time = inventory_json["expiry_time"]
        else:
            logger.info("Inventory not found, so created new inventory.")
            # Time conversion to CST
            inventory_json["manufacturing_time"] = remove_trunk(
                convert_date_into_cst(inventory_json["timezone"],
                                      inventory_json["manufacturing_time"]))
            inventory_json["expiry_time"] = remove_trunk(
                convert_date_into_cst(inventory_json["timezone"],
                                      inventory_json["expiry_time"]))
            inventory = inventory_schema.load(inventory_json)

        logger.info("Inventory updated and saved successfully.")
        inventory.save_to_db()

        return inventory_schema.dump(inventory), 201


class InventoryByCategory(Resource):
    @classmethod
    def get(cls, inventory_category: str):
        inventory = InventoryModel.find_by_category(inventory_category)
        if inventory:
            return inventory_list_schema.dump(inventory), 200
        return {"message": err_msg.get_msg("no_inventory_in_category").format(inventory_category)}, 404


class InventoryList(Resource):
    @classmethod
    def get(cls):
        logger.info("Fetch all inventories from the database.")
        return {"inventories": inventory_list_schema.dump(InventoryModel.find_all())}, 200
