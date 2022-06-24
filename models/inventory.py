from typing import List

from db import db
from app import logger


class InventoryModel(db.Model):
    __tablename__ = "inventory"

    logger.info("Inventory table created.")

    inventory_id = db.Column(db.Integer, primary_key=True)
    inventory_name = db.Column(db.String(50), nullable=False, unique=True)
    inventory_category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    manufacturing_time = db.Column(db.DateTime, nullable=False)
    expiry_time = db.Column(db.DateTime)
    timezone = db.Column(db.String(30))

    @classmethod
    def find_by_id(cls, _id: int) -> "InventoryModel":
        logger.info("Search inventory by 'inventory_id'")
        return cls.query.filter_by(inventory_id=_id).first()

    @classmethod
    def find_by_name(cls, name: str) -> "InventoryModel":
        logger.info("Search inventory by 'inventory_name'")
        return cls.query.filter_by(inventory_name=name).first()

    @classmethod
    def find_by_category(cls, category: str) -> List["InventoryModel"]:
        logger.info("Search inventories by 'inventory_category'")
        return cls.query.filter_by(inventory_category=category).all()

    @classmethod
    def find_all(cls) -> List["InventoryModel"]:
        logger.info("Find all inventories from database.")
        return cls.query.all()

    def save_to_db(self) -> None:
        logger.info("Save an inventory object to the database.")
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        logger.info("Delete an inventory from the database.")
        db.session.delete(self)
        db.session.commit()
