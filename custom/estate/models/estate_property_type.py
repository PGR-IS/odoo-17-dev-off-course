from odoo import fields, models

# Create the estate property type model
class EstatePropertyType(models.Model):
  _name = "estate.property.type"
  _description = ""

  name = fields.Char(string="Name", required=True)