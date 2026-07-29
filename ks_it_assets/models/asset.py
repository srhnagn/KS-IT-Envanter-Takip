# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

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
    warranty_warning_sent = fields.Boolean(string='Garanti Uyarısı Gönderildi', default=False, copy=False)
    
    barcode = fields.Char(string='Barkod / QR Kod', copy=False, tracking=True)
    
    status = fields.Selection([
        ('available', 'Boşta / Depoda'),
        ('assigned', 'Zimmetli / Kullanımda'),
        ('repair', 'Tamirde / Serviste'),
        ('scrapped', 'Hurdaya Ayrıldı')
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

    @api.model
    def _cron_check_warranty_expiry(self):
        """Her gece çalışıp garanti bitimine 30 gün kalan cihazlar için aktivite uyarısı oluşturur."""
        deadline = fields.Date.today() + relativedelta(days=30)
        
        # Garanti bitiş tarihi dolu, deadline'dan küçük/eşit ve henüz uyarı gönderilmemiş cihazları bul
        expiring_assets = self.search([
            ('warranty_end_date', '!=', False),
            ('warranty_end_date', '<=', deadline),
            ('warranty_warning_sent', '=', False)
        ])
        
        for asset in expiring_assets:
            # 1. Log/Not ekle
            asset.message_post(
                body=f"⚠️ <b>DİKKAT:</b> Bu cihazın garanti süresi <b>{asset.warranty_end_date}</b> tarihinde dolacaktır! Lütfen gerekli kontrolleri yapınız.",
                subtype_xmlid='mail.mt_note'
            )
            
            # 2. To-Do Activity Planla (Sistemi kuran veya IT Yöneticisi için)
            asset.activity_schedule(
                'mail.mail_activity_data_todo',
                summary=f'Garanti Bitiş Uyarısı ({asset.warranty_end_date})',
                note='Cihazın garantisi bitmek üzere, varsa onarım/servis işlemlerini başlatın.',
                user_id=1 # Normalde IT Yöneticisinin ID'si olur, demo için 1 (Admin) kullanıyoruz
            )
            
            # 3. Aynı uyarıyı tekrar atmamak için flag'i işaretle
            asset.warranty_warning_sent = True
