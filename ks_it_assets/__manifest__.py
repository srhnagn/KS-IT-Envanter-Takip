# -*- coding: utf-8 -*-
{
    'name': "KS IT Asset Manager",

    'summary': "Kaleseramik Bilgi İşlem (IT) Varlık, Zimmet ve Servis Yönetimi",

    'description': """
Kaleseramik IT Departmanı için özel olarak geliştirilmiş donanım, yazılım, sarf malzeme ve zimmet takip sistemi.
- Bilgisayar, Monitör, Yazıcı, Telefon vb. tekil takibi
- Geçici ödünç verme veya kalıcı zimmetleme
- Teknik servis ve arıza durumu kayıtları
    """,

    'author': "Serhan Agan",
    'website': "https://www.kaleseramik.com",
    'category': 'Human Resources',
    'version': '1.0.10',

    # Modülümüzün KS Envanter altyapısından ve Odoo'nun temel mail (chatter) yapısından faydalanması için
    'depends': ['base', 'mail'],

    # Yüklenecek dosyalar
    'data': [
        'security/ks_it_security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/cron_jobs.xml',
        'reports/assignment_report.xml',
        'reports/qr_label_report.xml',
        'views/dashboard_views.xml',
        'views/asset_views.xml',
        'views/assignment_views.xml',
        'views/repair_views.xml',
        'views/menu_views.xml',
    ],
    
    # Static dosyalar (CSS, JS)
    'assets': {
        'web.assets_backend': [
            'ks_it_assets/static/src/scss/it_styles.scss',
            'ks_it_assets/static/src/js/navbar_fix.js',
            'ks_it_assets/static/src/js/dashboard.js',
            'ks_it_assets/static/src/js/list_renderer_persist.js',
            'ks_it_assets/static/src/xml/dashboard.xml',
        ],
    },

    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}

