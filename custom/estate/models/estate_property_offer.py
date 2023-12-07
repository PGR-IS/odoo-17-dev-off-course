from odoo import fields, models

class EstatePropertyOffer(models.Model):
  _name = "estate.property.offer"
  _description = ""

  price = fields.Float(string="Price", required=True)
  status = fields.Selection(selection=[
    ("accepted", "Accepted"),
    ("refused", "Refused")
  ], copy=False)
  partner_id = fields.Many2one("res.partner", required=True)
  property_id = fields.Many2one("estate.property", required=True)
  property_state = fields.Selection(string="Property State", related="property_id.state")


  # Methods
  # - Accept offer button action
  def accept_offer_button_action(self):
    for record in self:
      # Accept the current offer and update the property infos
      record.status = "accepted"
      record.property_id.state = "offer accepted"
      record.property_id.buyer = record.partner_id
      record.property_id.selling_price = record.price
      # Refuse the other offers
      for offer in record.property_id.offer_ids:
        if offer.id != record.id:
          offer.status = 'refused'
    return True
  # - Accept offer button action
  def refuse_offer_button_action(self):
    for record in self:
      record.status = "refused"
    return True 