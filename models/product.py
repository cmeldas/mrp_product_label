from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    label_title = fields.Char(string='Title', copy=True)
    label_subtitle = fields.Char(string='Subtitle', copy=True)
    label_ingredients = fields.Text(string='Ingredients', copy=True)
    label_lifetime = fields.Integer(string='Lifetime (days)', copy=True)
    label_storage_temp = fields.Integer(string='Storage Temperature (°C)', copy=True, default=8 )
    label_fixed_weight = fields.Char(string='Fixed weight', copy=True, default=False, help="Leave empty to use scale weight during printing labels")
