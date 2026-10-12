from datetime import datetime, timedelta

from odoo import fields
from odoo.tests import Form, TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestMrpProductLabel(TransactionCase):
    """Etiketa: kopie z produktu na výrobní zakázku, onchange ve formuláři, datum spotřeby a cron."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.product'].create({
            'name': 'Jogurt bílý',
            'type': 'consu',
            'label_title': 'Jogurt',
            'label_subtitle': 'bílý',
            'label_ingredients': 'mléko, jogurtová kultura',
            'label_description': '<p>Z ranče</p>',
            'label_lifetime': 14,
            'label_storage_temp': 6,
            'label_fixed_weight': '150 g',
        })
        cls.other_product = cls.env['product.product'].create({
            'name': 'Tvaroh',
            'type': 'consu',
            'label_title': 'Tvaroh',
            'label_lifetime': 7,
        })

    def _create_mo(self, product, **vals):
        return self.env['mrp.production'].create({'product_id': product.id, 'product_qty': 1.0, **vals})

    def test_label_copied_on_create(self):
        production = self._create_mo(self.product)
        self.assertEqual(production.label_title, 'Jogurt')
        self.assertEqual(production.label_subtitle, 'bílý')
        self.assertEqual(production.label_ingredients, 'mléko, jogurtová kultura')
        self.assertIn('Z ranče', production.label_description)
        self.assertEqual(production.label_lifetime, 14)
        self.assertEqual(production.label_storage_temp, 6)
        self.assertEqual(production.label_fixed_weight, '150 g')
        self.assertFalse(production.label_lifetime_from_print)

    def test_default_storage_temperature(self):
        self.assertEqual(self.other_product.label_storage_temp, 8)

    def test_onchange_product_in_form(self):
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product
        self.assertEqual(mo_form.label_title, 'Jogurt')
        mo_form.product_id = self.other_product
        self.assertEqual(mo_form.label_title, 'Tvaroh')
        self.assertEqual(mo_form.label_lifetime, 7)
        production = mo_form.save()
        self.assertEqual(production.label_title, 'Tvaroh')

    def test_update_label_data_from_product(self):
        production = self._create_mo(self.product)
        self.product.label_title = 'Jogurt nový'
        self.assertEqual(production.label_title, 'Jogurt')
        production.action_update_label_data()
        self.assertEqual(production.label_title, 'Jogurt nový')

    def test_expiry_date(self):
        start = datetime(2026, 10, 1, 8, 0)
        production = self._create_mo(self.product, date_start=start)
        self.assertEqual(production.label_expiry_date, start.date() + timedelta(days=14))

        pasteurisation = datetime(2026, 10, 3, 9, 30)
        production.pasteurisation_start = pasteurisation
        self.assertEqual(production.label_expiry_date, pasteurisation.date() + timedelta(days=14))

        production.label_lifetime = 0
        self.assertFalse(production.label_expiry_date)

    def test_expiry_from_print_and_cron(self):
        production = self._create_mo(self.product, date_start=datetime(2026, 1, 1, 8, 0))
        production.label_lifetime_from_print = True
        today = fields.Date.today()
        self.assertEqual(production.label_expiry_date, today + timedelta(days=14))

        # cron přepočítá jen zakázky s trvanlivostí od tisku; ruční hodnota se přepíše dnešním výpočtem
        production.label_expiry_date = today
        cron = self.env.ref('mrp_product_label.ir_cron_recompute_label_expiry_date')
        self.assertTrue(cron.active)
        self.env['mrp.production']._cron_recompute_label_expiry_date()
        self.assertEqual(production.label_expiry_date, today + timedelta(days=14))
