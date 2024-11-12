from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
  _name = "estate.property.offer"
  _description = ""
  _order = "price desc"

  price = fields.Float(string="Price", required=True)
  status = fields.Selection(selection=[
    ("accepted", "Accepted"),
    ("refused", "Refused")
  ], copy=False)
  partner_id = fields.Many2one("res.partner", required=True)
  property_id = fields.Many2one("estate.property", required=True)
  property_state = fields.Selection(string="Property State", related="property_id.state")
  validity = fields.Integer(string="Validaty (In days)", default=7)
  date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
  estate_property_type = fields.Many2one(string="Property Type", related="property_id.estate_property_type", store=True)


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
  
  # - Compute the validity date
  @api.depends("validity","create_date")
  def _compute_date_deadline(self):
    for record in self:
      try:
        record.date_deadline = fields.Date.add(value=record.create_date, days=record.validity) if self.create_date else fields.Date.add(value=fields.Date.today(), days=record.validity)
      except:
        record.date_deadline = fields.Date.add(value=fields.Date.today(), days=record.validity)

  # - The inverse function for the deadline and validity
  def _inverse_date_deadline(self):
    for record in self:
      if record.create_date:
        record.validity = (record.date_deadline - fields.Date.today()).days
      
      
  
  # SQL constraints
  _sql_constraints = [
    ('check_price', 'CHECK(price>0)', 'The price must be strictly postif')
  ]

  # Override CRUD methods
  # - Create Method
  @api.model
  def create(self, vals):
    try:
      offers= self.env['estate.property'].browse(vals['property_id']).offer_ids
      max_offer = max([offer.price for offer in offers])
    except ValueError:
      max_offer = 0
    if vals['price'] < max_offer:
      raise ValidationError(_("You must enter an offer that is higher than the highest existing offer"))
    else:
      self.env['estate.property'].browse(vals['property_id']).state = 'offer received'
    return super().create(vals)
  