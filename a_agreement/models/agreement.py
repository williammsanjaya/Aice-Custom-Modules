# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests
from odoo.exceptions import ValidationError
import io
import os
import PyPDF2

# Class for the actual conponnent
class AgreeList(models.Model):
    _name = "a_agreement.list"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Agreement list system"

    #defining a sequence number for the name.
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Agreement'
            vals['state'] = 'sent'
        if vals.get('name', _('New Agreement')) == _('New Agreement'):
            vals['name'] = self.env['ir.sequence'].next_by_code('a_agreement.list') or _('New Agreement')
            vals['state'] = 'sent'
        res = super(AgreeList, self).create(vals)
        return res

    # Going to the next item in the sequence
    def toDraft(self):
        self.state = 'draft'

    def toSent(self):
        self.state = 'sent'

    # Name of the operation.
    name = fields.Char(string='Agreement Number', required=True, copy=False, readonly=True, default=lambda self: _('New Agreement'))
    
    # Gets the actual datte time from the server.
    date_creation = fields.Datetime(string='Cheated On ', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    
    # Observations
    note = fields.Text(string='Description')
    doc_name = fields.Char(string='Document Name', required=True)
    doc_reference = fields.Char(string='Document Ref', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True, change_default=True, index=True, tracking=1)
    user_id = fields.Many2one('res.users', string='Responsible', index=True, tracking=2, required=True, default=lambda self: self.env.user)
    
    # Array of status names.
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Saved'),
        ('done', 'Document Sent'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    # Archive / Unarchive
    active = fields.Boolean(string='Active', default=True, tracking=True)

    # PDF File field
    pdf_file = fields.Binary(string='PDF File')

    def download_pdf(self):
        file_data = self.pdf_file
        if file_data:
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/?model=a_agreement.list&id=%s&field=pdf_file&download=true&filename=%s.pdf' % (self.id, self.name),
                'target': 'self',
            }
        else:
            return False
    
    
# Class responsable for The item list itself.
#class AgreeListLine(models.Model):
    #_name = 'a_agreement.list.line'
    #_description = 'Agreement List Line'
    #_check_company_auto = True
    
    # Product field
    #product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True)
    # Quantity field
    #product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    # Price field
    #price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    # the id of the order
    #agreement_id = fields.Many2one('a_agreement.list', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    #Test = fields.Char(string='Test Text', required=True)

    # Subtotal
    #subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store = True)
    
    #tax_id = fields.Many2one('account.tax', string='Tax')
    #tax = fields.Float(string='Tax', compute='_compute_tax', store=True)

    #@api.depends('tax_id', 'subtotal')
    #def _compute_tax(self):
    #    for linha_pedido in self:
    #        linha_pedido.tax = linha_pedido.subtotal * (linha_pedido.tax_id.amount / 100) if linha_pedido.tax_id else 0.0
   
    # Getting the dependency
    #@api.depends('product_uom_qty', 'price_unit', 'tax_id')
    #def _compute_subtotal(self):
    #    for line in self:
    #        line.subtotal =  line.product_uom_qty * line.price_unit 
