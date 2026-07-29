# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KsItRepair(models.Model):
    _name = 'ks.it.repair'
    _description = 'IT Teknik Servis ve Saha Çıkış İşlemleri'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Talep No', required=True, copy=False, readonly=True, default='Yeni Servis')
    
    asset_id = fields.Many2one('ks.it.asset', string='Arızalı / İlgili Cihaz', required=True, tracking=True)
    technician_id = fields.Many2one('res.users', string='Teknisyen (IT Personeli)', default=lambda self: self.env.user, tracking=True)
    
    repair_type = fields.Selection([
        ('internal', 'İç Tamir (IT Odası)'),
        ('external', 'Dış Servis (Garanti vb.)'),
        ('field', 'Saha Kurulumu / Müdahale')
    ], string='İşlem Türü', default='internal', required=True, tracking=True)
    
    issue_description = fields.Text(string='Arıza Özeti / Saha Notu', required=True)
    
    report_date = fields.Date(string='Bildirim Tarihi', default=fields.Date.context_today)
    completion_date = fields.Date(string='Tamamlanma Tarihi', readonly=True)
    
    state = fields.Selection([
        ('draft', 'Bekliyor'),
        ('in_progress', 'İşlemde'),
        ('done', 'Tamamlandı'),
        ('cancelled', 'İptal')
    ], string='Durum', default='draft', tracking=True)
    
    resolution_note = fields.Text(string='Çözüm / Yapılan İşlemler')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Yeni Servis') == 'Yeni Servis':
                vals['name'] = self.env['ir.sequence'].next_by_code('ks.it.repair') or 'SRV-YENI'
        records = super().create(vals_list)
        # Kayıt oluşturulurken zaten 'in_progress' ise varlığı senkronize et
        for record in records:
            if record.state == 'in_progress' and record.asset_id:
                record.asset_id.status = 'repair'
        return records

    def write(self, vals):
        res = super().write(vals)
        # Durum değişikliklerinde varlık durumunu otomatik güncelle
        if 'state' in vals:
            for record in self:
                if record.state == 'in_progress' and record.asset_id:
                    record.asset_id.status = 'repair'
                elif record.state in ['done', 'cancelled'] and record.asset_id:
                    if record.asset_id.current_assignee_id:
                        record.asset_id.status = 'assigned'
                    else:
                        record.asset_id.status = 'available'
        return res

    def action_start(self):
        for record in self:
            record.state = 'in_progress'
            # write() hook'u zaten asset_id.status = 'repair' yapacak

    def action_done(self):
        for record in self:
            record.state = 'done'
            record.completion_date = fields.Date.context_today(record)
            # write() hook'u zaten asset_id.status = 'available' yapacak
