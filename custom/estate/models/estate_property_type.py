from odoo import api, fields, models

# Create the estate property type model
class EstatePropertyType(models.Model):
  _name = "estate.property.type"
  _description = ""
  _order = "name"

  name = fields.Char(string="Name", required=True)
  property_ids = fields.One2many('estate.property', 'estate_property_type', string='Properties')
  offer_ids = fields.One2many('estate.property.offer', 'estate_property_type', string="Offers")
  offer_count = fields.Integer(string="Offer Counts", compute="_compute_offer_count")
  # SQL constraints
  _sql_constraints = [
    ('unique_name', 'UNIQUE(name)', 'The TYPE name must be UNIQUE')
  ]


  # Computed fields methods
  # - Offer type methode
  @api.depends("offer_ids")
  def _compute_offer_count(self):
    for record in self:
      record.offer_count = len(record.offer_ids)
     