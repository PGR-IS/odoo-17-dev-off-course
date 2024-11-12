from odoo import fields, models, api

class EstateProperty(models.Model):
  _inherit = "estate.property"

  def estate_property_sold_button_action(self):
    # TO FINISH
    return super().estate_property_sold_button_action()
