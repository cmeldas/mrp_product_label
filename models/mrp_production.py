from odoo import models, fields, api
from datetime import datetime, timedelta

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # We want to copy the label data to MO, so we can track their values at production time
    # even if the product's label data changes later (new recipe, new name/title, etc.)
    label_title = fields.Char(string='Title')
    label_subtitle = fields.Char(string='Subtitle')
    label_ingredients = fields.Text(string='Ingredients')
    label_description = fields.Html(string='Description', sanitize=True)
    label_storage_temp = fields.Integer(string='Storage Temperature (°C)')
    label_fixed_weight = fields.Char(string='Fixed Weight', help="Leave empty to use scale weight during printing labels")
    label_lifetime = fields.Integer(string='Lifetime (days)', help="From MO date or pasteurisation date to compute expiry date on labels")
    label_lifetime_from_print = fields.Boolean(string='Lifetime from Print Date', default=False, help="If checked, the expiry date on the label will be counted from the date of printing instead of the pasteurisation date.")

    label_expiry_date = fields.Date(string='Expiry Date', compute='_compute_label_expiry_date', store=True, help="Computed from the production/pasteurisation date and the product's label lifetime, but can be edited manually.")

    @api.depends('pasteurisation_start', 'date_start', 'label_lifetime', 'label_lifetime_from_print')
    def _compute_label_expiry_date(self):
        today = fields.Date.today()
        for record in self:
            if not record.label_lifetime:
                record.label_expiry_date = False
            elif record.label_lifetime_from_print:
                record.label_expiry_date = today + timedelta(days=record.label_lifetime)
            elif record.pasteurisation_start:
                record.label_expiry_date = record.pasteurisation_start + timedelta(days=record.label_lifetime)
            elif record.date_start:
                record.label_expiry_date = record.date_start + timedelta(days=record.label_lifetime)
            else:
                record.label_expiry_date = False

    def _cron_recompute_label_expiry_date(self):
        """Recompute expiry date daily for MOs where lifetime is counted from print date."""
        productions = self.search([
            ('label_lifetime_from_print', '=', True),
            ('label_lifetime', '>', 0),
            ('state', 'not in', ('done', 'cancel')),
        ])
        productions._compute_label_expiry_date()

    def _update_label_data_from_product(self):
        self.ensure_one()
        if self.product_id:
            self.write({
                'label_title': self.product_id.label_title,
                'label_subtitle': self.product_id.label_subtitle,
                'label_ingredients': self.product_id.label_ingredients,
                'label_description': self.product_id.label_description,
                'label_storage_temp': self.product_id.label_storage_temp,
                'label_fixed_weight': self.product_id.label_fixed_weight,
                'label_lifetime': self.product_id.label_lifetime,
                'label_lifetime_from_print': self.product_id.label_lifetime_from_print,
            })

    def action_update_label_data(self):
        """Update label data from the product."""
        for record in self:
            record._update_label_data_from_product()

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
            self.label_ingredients = self.product_id.label_ingredients
            self.label_description = self.product_id.label_description
            self.label_storage_temp = self.product_id.label_storage_temp
            self.label_fixed_weight = self.product_id.label_fixed_weight
            self.label_lifetime = self.product_id.label_lifetime
            self.label_lifetime_from_print = self.product_id.label_lifetime_from_print
           # self._compute_label_expiry_date()
        return res
