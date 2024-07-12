from app.schemas import ma
from marshmallow import fields, validate


class ProductSchema(ma.Schema):
    id = fields.Integer(required=False) # id is autogenerated
    name = fields.String(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0)) # can add 'max=100' (dollars) if we want. Right now, no max restrictions

# Create an instance of the ProductSchema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True) # For handling multiple products