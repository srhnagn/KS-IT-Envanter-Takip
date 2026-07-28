# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KsItAsset(models.Model):
    _name = 'ks.it.asset'
    _description = 'IT Varlık ve Demirbaş'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Cihaz / Varlık Adı', required=True, tracking=True)
    asset_type = fields.Selection([
        ('computer', 'Bilgisayar / Laptop'),
        ('monitor', 'Monitör'),
        ('phone', 'Telefon / Tablet'),
        ('network', 'Ağ Cihazı (Switch, AP)'),
        ('printer', 'Yazıcı / Tarayıcı'),
        ('consumable', 'Sarf Malzeme (Mouse, Klavye, Kablo)'),
        ('software', 'Yazılım / Lisans')
    ], string='Varlık Türü', default='computer', required=True, tracking=True)
    
    brand = fields.Char(string='Marka')
    model_name = fields.Char(string='Model')
    
    serial_number = fields.Char(string='Seri No / Servis Etiketi', tracking=True)
    mac_address = fields.Char(string='MAC Adresi (Wi-Fi / LAN)')
    
    purchase_date = fields.Date(string='Satın Alma Tarihi')
    warranty_end_date = fields.Date(string='Garanti Bitiş Tarihi', tracking=True)
    
    status = fields.Selection([
        ('available', 'Boşta / Depoda'),
        ('assigned', 'Zimmetli / Kullanımda'),
        ('repair', 'Tamirde / Serviste'),
        ('scrapped', 'Hurtaya Ayrıldı')
    ], string='Durum', default='available', tracking=True)
    
    internal_notes = fields.Text(string='İç Notlar / Özellikler')
    
    # İlişkiler
    assignment_ids = fields.One2many('ks.it.assignment', 'asset_id', string='Zimmet Geçmişi')
    repair_ids = fields.One2many('ks.it.repair', 'asset_id', string='Tamir ve Servis Geçmişi')
    
    # Mevcut Zimmetli Kişi
    current_assignee_id = fields.Many2one('res.partner', string='Şu Anki Kullanıcı', compute='_compute_current_assignee', store=True)

    @api.depends('assignment_ids.state', 'assignment_ids.employee_id')
    def _compute_current_assignee(self):
        for asset in self:
            active_assignment = asset.assignment_ids.filtered(lambda a: a.state == 'active')
            if active_assignment:
                asset.current_assignee_id = active_assignment[0].employee_id
            else:
                asset.current_assignee_id = False

    def action_open_form(self):
        """Tablodaki butona basılınca varlığın tam form görünümünü açar."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ks.it.asset',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }
