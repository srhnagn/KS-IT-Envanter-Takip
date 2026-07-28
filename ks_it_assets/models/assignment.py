# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KsItAssignment(models.Model):
    _name = 'ks.it.assignment'
    _description = 'IT Varlık Zimmet ve Ödünç İşlemleri'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='İşlem Kodu', required=True, copy=False, readonly=True, default='Yeni Zimmet')
    
    asset_id = fields.Many2one('ks.it.asset', string='Varlık / Cihaz', required=True, tracking=True)
    employee_id = fields.Many2one('res.partner', string='Personel', required=True, tracking=True)
    
    assignment_type = fields.Selection([
        ('permanent', 'Kalıcı Zimmet'),
        ('temporary', 'Geçici Ödünç')
    ], string='İşlem Türü', default='permanent', required=True, tracking=True)
    
    assigned_date = fields.Date(string='Veriliş Tarihi', default=fields.Date.context_today, required=True)
    expected_return_date = fields.Date(string='Beklenen İade Tarihi', tracking=True)
    actual_return_date = fields.Date(string='Gerçekleşen İade Tarihi', readonly=True)
    
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('active', 'Aktif (Personelde)'),
        ('returned', 'İade Edildi')
    ], string='Durum', default='draft', tracking=True)
    
    note = fields.Text(string='Notlar')
    document_pdf = fields.Binary(string='İmzalı Zimmet Formu (PDF)')
    document_filename = fields.Char(string='Dosya Adı')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Yeni Zimmet') == 'Yeni Zimmet':
                vals['name'] = self.env['ir.sequence'].next_by_code('ks.it.assignment') or 'ZMT-YENI'
        return super().create(vals_list)

    def action_confirm(self):
        for record in self:
            if record.asset_id.status != 'available':
                pass # Hata fırlatılabilir, şu anlık pass
            record.state = 'active'
            record.asset_id.status = 'assigned'

    def action_return(self):
        for record in self:
            record.state = 'returned'
            record.actual_return_date = fields.Date.context_today(record)
            record.asset_id.status = 'available'
