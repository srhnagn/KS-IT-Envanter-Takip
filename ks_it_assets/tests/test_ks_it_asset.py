# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from datetime import date
from dateutil.relativedelta import relativedelta

class TestKsItAsset(TransactionCase):

    def setUp(self):
        super(TestKsItAsset, self).setUp()
        self.Asset = self.env['ks.it.asset']
        
    def test_01_auto_barcode_generation(self):
        """Test if barcode is automatically generated via ir.sequence on creation."""
        asset = self.Asset.create({
            'name': 'Test Geliştirici Laptop',
            'asset_type': 'computer',
            'brand': 'Apple',
            'model_name': 'MacBook Pro'
        })
        
        # Barkodun boş gelmediğini ve IT- ile başladığını kontrol et (Sequencedan dolayı)
        self.assertTrue(asset.barcode, "Barkod alanı boş kalamaz!")
        self.assertTrue(asset.barcode.startswith('IT-'), "Barkod doğru formatta (IT-...) üretilmedi!")
        
    def test_02_warranty_cron_job(self):
        """Test if the cron job correctly identifies assets with expiring warranties."""
        # Garantisi 30 gün sonra bitecek bir cihaz oluştur (Cron sınırında)
        expiring_date = date.today() + relativedelta(days=29)
        asset_expiring = self.Asset.create({
            'name': 'Garanti Test Cihazı 1',
            'warranty_end_date': expiring_date
        })
        
        # Garantisi çoktan bitmiş bir cihaz
        expired_date = date.today() - relativedelta(days=10)
        asset_expired = self.Asset.create({
            'name': 'Garanti Test Cihazı 2',
            'warranty_end_date': expired_date
        })
        
        # Güvenli cihaz (garantisi 1 yıl sonra bitecek)
        safe_date = date.today() + relativedelta(days=365)
        asset_safe = self.Asset.create({
            'name': 'Garanti Test Cihazı 3',
            'warranty_end_date': safe_date
        })

        # Cron Job fonksiyonunu manuel tetikle
        self.Asset._cron_check_warranty_expiry()

        # Sonuçları kontrol et
        self.assertTrue(asset_expiring.warranty_warning_sent, "30 günden az kalan cihaza uyarı gitmedi!")
        self.assertTrue(asset_expired.warranty_warning_sent, "Garantisi çoktan bitmiş cihaza (gecikmeli) uyarı gitmedi!")
        self.assertFalse(asset_safe.warranty_warning_sent, "Garantisi bitmesine 1 yıl olan cihaza gereksiz yere uyarı gitti!")
