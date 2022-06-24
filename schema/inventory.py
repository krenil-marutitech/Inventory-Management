from ma import ma
from models.inventory import InventoryModel


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InventoryModel
        load_instance = True
        dump_only = ("inventory_id",)
