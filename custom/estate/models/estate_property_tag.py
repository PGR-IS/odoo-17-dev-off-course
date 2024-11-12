from odoo import fields, models

class EstatePropertyTag(models.Model):
  _name = "estate.property.tag"
  _description = ""
  _order = "name"

  name = fields.Char(string="Name", required=True)
  color = fields.Integer()

  # SQL constraints
  _sql_constraints = [
    ('unique_name', 'UNIQUE(name)', 'The TAG name must be UNIQUE')
  ]