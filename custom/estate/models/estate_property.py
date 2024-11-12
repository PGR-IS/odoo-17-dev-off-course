from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare

# Create EstateProperty class
class EstateProperty(models.Model):
  _name = "estate.property"
  _description = """
    This module will contain the main informations concerning the property
  """
  _order = "sequence, id desc"

  name = fields.Char(string='Name', required=True, default="Unknown")
  description = fields.Text(string='Description')
  postcode = fields.Char(string='Postcode')
  date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.add(value=fields.date.today(), months=3))
  expected_price = fields.Float(string='Expected Price', required=True)
  selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
  bedrooms = fields.Integer(string='Bedrooms', default=2)
  living_area = fields.Integer(string='Living Area (sqm)')
  facades = fields.Integer(string='Facades')
  garage = fields.Boolean(string='Garage')
  garden = fields.Boolean(string='Garden')
  garden_area = fields.Integer(string='Garden Area')
  garden_orientation = fields.Selection(
    string='Garden Orientation',
    selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]  
  )
  estate_property_type = fields.Many2one("estate.property.type", string="Type")
  sequence = fields.Integer("Sequence", default=1, help="This is used to sort the property display by the type the most sold for example")



  # References and Advanced fields
  buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
  salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
  tag_ids = fields.Many2many("estate.property.tag", string="Tags")
  offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

  # Computed fields
  total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
  best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

  
  # Reserved fields
  active = fields.Boolean(default=True)
  state = fields.Selection(selection=[
    ('new', 'New'),
    ('offer received', 'Offer Received'),
    ('offer accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('canceled', 'Canceled')
  ],
    default="new",
    required=True
  )


  # Computed Methods
  # - Compute the total area
  @api.depends("living_area", "garden_area")
  def _compute_total_area(self):
    """
      Auto-Compute the total area    
    """
    for record in self:
      record.total_area = record.living_area + record.garden_area
  # - Compute the best offer
  @api.depends("offer_ids")
  def _compute_best_price(self):
    for record in self:
      try:
        record.best_price = max(record.offer_ids.mapped('price'))
      except ValueError:
        print("There are no offers")
        record.best_price = 0

  # Onchange methods
  @api.onchange("garden")
  def _onchange_garden(self):
    self.garden_area = 10 if self.garden else 0
    self.garden_orientation = "north" if self.garden else ""
      
  # Methods
  # - Sold button action
  def estate_property_sold_button_action(self):
    for record in self:
      if record.state == "offer accepted":
        record.state = "sold"
      elif record.state == "canceled":
        raise UserError(_("A CANCELED property cannot be SOLD!"))
      else:
        raise UserError(_("You need to accept an offer before switching to a SOLD state"))

    return True
  # - Canceled button action      
  def estate_property_cancel_button_action(self):
    for record in self:
      if record.state != "sold":
        record.state = "canceled"
      else:
        raise UserError(_("A SOLD property cannot be CANCELED!"))
    return True


  # SQL constraints
  _sql_constraints = [
    ('check_expected_price', 'CHECK(expected_price>0)', 'The Expected Price must be strictly positive'),
    ('check_selling_price', 'CHECK(selling_price>=0)', 'The Selling Price must be positive')
  ]

  # Python constraints
  @api.constrains("selling_price", "expected_price")
  def _check_selling_expected_price(self):
    for record in self:
      if not float_is_zero(record.selling_price, precision_digits=2):
        if float_compare(record.selling_price, (90/100) * record.expected_price, precision_digits=2) < 0:
          raise ValidationError(_("The Selling Price can not be lower than 90 percent of the Expected Price"))
  
  # Override CRUD operations
  # - Unlink method(by the mean of ondelete decorator)
  @api.ondelete(at_uninstall=False)
  def _unlink_if_state_is_new_or_canceled(self):
    for record in self:
      if record.state != "new" and record.user != 'canceled':
        raise UserError(_("You can't delete a property that is in the state '{}'".format(record.state)))
  







