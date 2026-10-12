from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    label_title = fields.Char(string='Title', copy=True)
    label_subtitle = fields.Char(string='Subtitle', copy=True)
    label_ingredients = fields.Text(string='Ingredients', copy=True)
    label_description = fields.Html(string='Label Description', copy=True, sanitize=True)
    label_lifetime = fields.Integer(string='Lifetime (days)', copy=True)
    label_lifetime_from_print = fields.Boolean(string='Lifetime from Print Date', copy=True, default=False, help="If checked, the expiry date on the label will be counted from the date of printing instead of the pasteurisation date.")
    label_storage_temp = fields.Integer(string='Storage Temperature (°C)', copy=True, default=8 )
    label_fixed_weight = fields.Char(string='Fixed weight', copy=True, default=False, help="Leave empty to use scale weight during printing labels")
