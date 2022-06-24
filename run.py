from app import app, api
from resources.inventory import Inventory, UpdateInventory, InventoryByCategory, InventoryList
from db import db
from ma import ma


@app.before_first_request
def create_tables():
    if __name__ == "__main__":
        db.create_all()


api.add_resource(Inventory, '/inventory/<string:inventory_name>')
api.add_resource(UpdateInventory, '/inventory/<int:inventory_id>')
api.add_resource(InventoryByCategory, '/category/<string:inventory_category>')
api.add_resource(InventoryList, '/inventories')


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
