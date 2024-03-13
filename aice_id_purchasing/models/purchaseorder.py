# -*- coding: utf-8 -*-

from odoo import models, fields, api



class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    ponumber = fields.Char(
        string='PA Number',
        required=True,
        tracking=True,
        index=True, copy=False)
    
    po_date_created = fields.Date(string='PO Date Created', required=True, index=True, copy=False, default=fields.Datetime.now)


class AccountMoveLine(models.Model):
    _inherit = ['account.move.line']



    def asset_create(self):
        # Convert self.quantity to integer
        quantity = int(self.quantity)
        for x in range(quantity):
            if self.asset_category_id:
                price_subtotal = self.currency_id._convert(self.price_subtotal,
                                                        self.company_currency_id,
                                                        self.company_id,
                                                        self.move_id.invoice_date or fields.Date.context_today(
                                                            self))
                vals = {
                    'name': self.name,
                    'code': self.name or False,
                    'category_id': self.asset_category_id.id,
                    'value': price_subtotal/quantity,
                    'partner_id': self.move_id.partner_id.id,
                    'company_id': self.move_id.company_id.id,
                    'currency_id': self.move_id.company_currency_id.id,
                    'date': self.move_id.invoice_date or self.move_id.date,
                    'invoice_id': self.move_id.id,
                }
                changed_vals = self.env['account.asset.asset'].onchange_category_id_values(vals['category_id'])
                vals.update(changed_vals['value'])
                asset = self.env['account.asset.asset'].create(vals)
                if self.asset_category_id.open_asset:
                    if asset.date_first_depreciation == 'manual':
                        asset.first_depreciation_manual_date = asset.date
                    asset.validate()
        return True