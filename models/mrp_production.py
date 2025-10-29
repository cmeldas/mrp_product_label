from odoo import models, fields, api
from datetime import datetime, timedelta

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # We want to copy the label data to MO, so we can track their values at production time
    # even if the product's label data changes later (new recipe, new name/title, etc.)
    label_title = fields.Char(string='Title')
    label_subtitle = fields.Char(string='Subtitle')
    label_ingredient = fields.Text(string='Ingredients')
    label_storage_temp = fields.Integer(string='Storage Temperature (°C)')
    label_fixed_weight = fields.Char(string='Fixed Weight', help="Leave empty to use scale weight during printing labels")
    label_lifetime = fields.Integer(string='Lifetime (days)')

    label_expiry_date = fields.Date(string='Expiry Date', compute='_compute_label_expiry_date', store=True)

    @api.depends('pasteurisation_start', 'date_start', 'label_lifetime')
    def _compute_label_expiry_date(self):
        for record in self:
            
            if record.pasteurisation_start and record.label_lifetime:
                record.label_expiry_date = record.pasteurisation_start + timedelta(days=record.label_lifetime)
            elif record.date_start and record.label_expiry_date is False and record.label_lifetime:
                record.label_expiry_date = record.date_start + timedelta(days=record.label_lifetime)
            else:
                record.label_expiry_date = False

    def _update_label_data_from_product(self):
        self.ensure_one()
        if self.product_id:
            self.write({
                'label_title': self.product_id.label_title,
                'label_subtitle': self.product_id.label_subtitle,
                'label_ingredient': self.product_id.label_ingredient,
                'label_storage_temp': self.product_id.label_storage_temp,
                'label_fixed_weight': self.product_id.label_fixed_weight,
                'label_lifetime': self.product_id.label_lifetime,
            })

    @api.model_create_multi
    def create(self, vals_list):
        productions = super().create(vals_list)
        for production in productions:
            production._update_label_data_from_product()
            #production._compute_label_expiry_date()
        return productions

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        if self.product_id:
            self.label_title = self.product_id.label_title
            self.label_subtitle = self.product_id.label_subtitle
            self.label_ingredient = self.product_id.label_ingredient
            self.label_storage_temp = self.product_id.label_storage_temp
            self.label_fixed_weight = self.product_id.label_fixed_weight
            self.label_lifetime = self.product_id.label_lifetime
           # self._compute_label_expiry_date()
        return res
