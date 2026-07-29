import random
from datetime import datetime, timedelta
from odoo import fields

env = self.env

# Kullanıcılar ve personeller (Odoo'nun varsayılan demo verisinden veya mevcutlardan alalım)
partners = env['res.partner'].search([('is_company', '=', False)], limit=20)
if not partners:
    # Eğer hiç partner yoksa dummy partner oluşturalım
    partners = env['res.partner'].create([
        {'name': f'Personel {i}', 'email': f'personel{i}@kaleseramik.com'} for i in range(1, 11)
    ])

technicians = env['res.users'].search([], limit=5)

# Rastgele veri havuzları
brands_models = {
    'computer': [('Dell', 'Latitude 5420'), ('Lenovo', 'ThinkPad T14'), ('HP', 'EliteBook 840'), ('Apple', 'MacBook Pro 16')],
    'monitor': [('Dell', 'UltraSharp 27'), ('LG', '27UN850-W'), ('Samsung', 'Odyssey G5'), ('ViewSonic', 'VG2755')],
    'phone': [('Apple', 'iPhone 13 Pro'), ('Samsung', 'Galaxy S22'), ('Apple', 'iPhone 14'), ('Xiaomi', 'Redmi Note 11')],
    'network': [('Cisco', 'Catalyst 2960-X'), ('Ubiquiti', 'UniFi AP AC Pro'), ('Aruba', 'Instant On 1930'), ('Juniper', 'EX2300')],
    'printer': [('HP', 'LaserJet Pro M404n'), ('Brother', 'HL-L2350DW'), ('Epson', 'EcoTank L3250'), ('Canon', 'i-SENSYS MF443dw')],
    'consumable': [('Logitech', 'MX Master 3'), ('Logitech', 'K380'), ('Anker', 'PowerLine+ III'), ('Microsoft', 'Ergonomic Keyboard')],
    'software': [('Microsoft', 'Office 365 E3'), ('Adobe', 'Creative Cloud All Apps'), ('Autodesk', 'AutoCAD 2024'), ('JetBrains', 'IntelliJ IDEA Ultimate')]
}

statuses = ['available', 'assigned', 'repair', 'scrapped']

def random_date(start_days_ago, end_days_ago):
    return fields.Date.to_string(datetime.now() - timedelta(days=random.randint(end_days_ago, start_days_ago)))

# 1. Varlıkları (Assets) Oluştur
print("Varlıklar oluşturuluyor...")
assets = []
for asset_type, bm_list in brands_models.items():
    for i in range(5): # Her tipten 5 tane
        brand, model = random.choice(bm_list)
        purchase_date = datetime.now() - timedelta(days=random.randint(100, 1000))
        warranty_end = purchase_date + timedelta(days=random.choice([365, 730, 1095]))
        
        asset_vals = {
            'name': f"{brand} {model} - {'Oda' if asset_type == 'network' else 'IT'}-{random.randint(1000,9999)}",
            'asset_type': asset_type,
            'brand': brand,
            'model_name': model,
            'serial_number': f"SN-{brand[:2].upper()}{random.randint(100000, 999999)}",
            'mac_address': f"00:1A:2B:3C:{random.randint(10, 99)}:{random.randint(10, 99)}" if asset_type in ['computer', 'network', 'phone', 'printer'] else False,
            'purchase_date': purchase_date.strftime('%Y-%m-%d'),
            'warranty_end_date': warranty_end.strftime('%Y-%m-%d'),
            'internal_notes': f"Bu cihaz {purchase_date.strftime('%Y')} yılında departman bütçesinden alınmıştır. Genel durumu {random.choice(['iyi', 'orta', 'mükemmel'])}.",
            'status': 'available' # Başlangıçta hepsi available
        }
        asset = env['ks.it.asset'].create(asset_vals)
        assets.append(asset)

# 2. Zimmetleri (Assignments) Oluştur
print("Zimmetler oluşturuluyor...")
# Tüm bilgisayar ve telefonların %80'ini zimmetle
assignable_assets = [a for a in assets if a.asset_type in ['computer', 'phone', 'monitor']]
random.shuffle(assignable_assets)
for asset in assignable_assets[:int(len(assignable_assets) * 0.8)]:
    partner = random.choice(partners)
    assignment = env['ks.it.assignment'].create({
        'asset_id': asset.id,
        'employee_id': partner.id,
        'assignment_type': random.choice(['permanent', 'temporary']),
        'assigned_date': random_date(100, 5),
        'expected_return_date': random_date(5, -30) if random.random() > 0.5 else False,
        'note': f"{partner.name} isimli personele {asset.name} cihazı teslim edilmiştir. Tüm fonksiyonları çalışır durumdadır."
    })
    assignment.action_confirm() # Aktif duruma geçir ve cihazı 'assigned' yap

# 3. Teknik Servis Kayıtlarını (Repairs) Oluştur
print("Teknik servis kayıtları oluşturuluyor...")
# Kalan cihazlardan bazılarını tamire gönder (available olanlar)
repairable_assets = env['ks.it.asset'].search([('status', '=', 'available')], limit=6)
for asset in repairable_assets:
    technician = random.choice(technicians)
    repair = env['ks.it.repair'].create({
        'asset_id': asset.id,
        'technician_id': technician.id,
        'repair_type': random.choice(['internal', 'external', 'field']),
        'issue_description': f"{asset.name} cihazında {random.choice(['ekran kararması', 'batarya şişmesi', 'sistem yavaşlaması', 'bağlantı kopması'])} şikayeti var.",
        'report_date': random_date(20, 1)
    })
    repair.action_start() # İşlemde duruma geçir ve cihazı 'repair' yap

# Geçmiş bazı tamirleri tamamlanmış olarak ekle (Geçmiş veri olsun diye)
print("Geçmiş tamir kayıtları ekleniyor...")
completed_assets = env['ks.it.asset'].search([], limit=10)
for asset in completed_assets:
    technician = random.choice(technicians)
    repair = env['ks.it.repair'].create({
        'asset_id': asset.id,
        'technician_id': technician.id,
        'repair_type': random.choice(['internal', 'external']),
        'issue_description': f"Geçmişte yaşanmış arıza: {random.choice(['fan sesi', 'klavye tuş basmaması', 'şarj soketi temassızlığı'])}",
        'report_date': random_date(200, 100),
        'resolution_note': f"{technician.name} tarafından {random.choice(['parça değişimi', 'yazılım güncellemesi', 'temizlik'])} yapılarak sorun giderildi."
    })
    repair.action_start()
    repair.action_done()

print("Bütün dummy veriler başarıyla eklendi! Toplam oluşturulan varlık:", len(assets))
env.cr.commit()
