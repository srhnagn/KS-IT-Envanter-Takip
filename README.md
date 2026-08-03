# KS IT Asset Manager (Bilgi İşlem Varlık Yönetimi)

KS IT Asset Manager, Odoo 17 altyapısı üzerinde tamamen sıfırdan geliştirilmiş, kurumsal şirketlerin Bilgi İşlem (IT) departmanlarına özel kapsamlı bir donanım, lisans, zimmet ve arıza takip platformudur. 

Şirket içindeki tüm donanım hareketlerini (kimde, nerede, hangi durumda) saniyesi saniyesine izlemenizi sağlarken, teknik servis süreçlerini ve garanti takibini tek bir çatı altında toplar.

## ✨ Temel Özellikler (Key Features)

* **Detaylı IT Envanteri:** Bilgisayar, Monitör, Yazılım Lisansı, Ağ Cihazı, Akıllı Telefon/Tablet, Yazıcı ve Sarf Malzemeler için özel oluşturulmuş 7 farklı kategoriyle envanterdekı yazılım ve donanımların takibi.
* **Gelişmiş Zimmet (Assignment) Yönetimi:** 
  * Cihazları personellere veya departmanlara **Kalıcı (Permanent)** veya **Geçici (Temporary)** olarak zimmetleme.
  * Odoo'nun QWeb PDF motoruyla tek tıkla şirket formatına ve ıslak imzaya hazır **Zimmet/Teslim Tutanağı** basımı.
  * Süresi gecikmiş "Geçici" zimmetlerde ekranlarda otomatik olarak devreye giren **Dinamik Neon Kırmızı (İadesi Gecikti)** uyarı rozetleri.
* **Kurumsal Teknik Servis Simülasyonu:** 
  * Arıza veya bakım durumundaki donanımların takibi. 
  * Bir cihaz servisten döndüğünde (Tamamlandı), sistem arka planda önceki sahibini tanır ve eski aktif zimmetine cihazı geri döndürerek iş akışını koparmadan sürdürür.
* **Otomatik Garanti Uyarısı (Cron Job):** Arka planda çalışan Python otonom görevleri sayesinde garanti süresinin bitimine 30 gün kalan tüm cihazlar için sistem otomatik olarak yöneticiye "Aktivite/Görev" atar.
* **Modern ve Özelleştirilmiş OWL Dashboard:** Odoo Web Library (JavaScript) kullanılarak yazılmış, tüm departmanın genel durumunu, arızalı cihazları ve geciken ödünçleri tek ekranda gösteren canlı raporlama paneli.
* **Koyu Tema (Dark Mode) Uyumluluğu:** SCSS ile geliştirilmiş ve gece modunda bile göz yormayan, transparan zemin kullanan yüksek çözünürlüklü etiket (Badge) tasarımları.
* **Otomatik Kodlama ve El Terminali Altyapısı (ir.sequence):** Sisteme eklenen her yeni donanıma otomatik olarak "IT-2026-0001" formatında ardışık benzersiz barkodlar atanır. Sistem, endüstriyel el terminalleri (Barcode Scanners) ile entegre çalışabilecek tarama altyapısına sahiptir.
* **Dinamik QR Kod ve PDF Etiket Basımı (QWeb):** Python kütüphaneleriyle sistemdeki her cihaz için otonom olarak benzersiz QR kod üreten altyapı ve bu kodları donanımların üzerine yapıştırmak üzere tasarlanmış kare formatlı (QR Label) PDF raporlama çıktısı.
* **Active Directory (LDAP) Entegrasyon Altyapısı:** Kurumsal ağlarda personellerin tek şifreyle güvenli giriş yapabilmesi için, IT yöneticilerinin production ortamında kolayca bağlayabileceği Enterprise LDAP yetkilendirme altyapısı.
* **Kalite Güvence (QA) ve Unit Testing:** Sistemin hata toleransını ölçmek için geliştirilmiş özel Odoo Test betikleri bulunmaktadır. (`test_ks_it_asset.py`). Otomatik barkod ve Cron Job gibi kritik arka plan süreçleri sahte (dummy) cihazlarla izole ortamda test edilip doğrulanmıştır.

## 🛠 Kullanılan Teknolojiler
* **Backend:** Python 3.10+, Odoo 17 Framework, PostgreSQL
* **Frontend:** Odoo Web Library (OWL) JS, QWeb (XML), SCSS, Bootstrap
* **Mimari:** Modüler, MVC (Model-View-Controller) ve Object Relational Mapping (ORM)

## 🚀 Projeyi İlk Kez Kuracak Geliştiriciler İçin (Kurulum Rehberi)
Projeyi bilgisayarınıza çektikten (clone) sonra şu adımları izleyin:

### 1. PostgreSQL Kurulumu
Odoo'nun çalışması için lokalinizde PostgreSQL olmalıdır. (Mac için Homebrew önerilir)
```bash
brew install postgresql@17
brew services start postgresql@17
createdb kaleseramik_db
```

### 2. Odoo Yapılandırması (`odoo.conf`)
Proje ana dizininde bulunan `odoo.conf` dosyasının içindeki veritabanı adını kendi oluşturduğunuz DB adıyla eşleştirin. Örnek bir `odoo.conf` içeriği şu şekilde olmalıdır:

```ini
[options]
admin_passwd = gizli_master_sifre
db_host = False
db_port = False
db_user = bilgisayar_kullanici_adiniz
db_password = False
addons_path = /odoo/addons_yolu, /kendi_projenizin_yolu
```

### 3. Modülü Yükleme (Otomatik Veritabanı İnşası)
PostgreSQL'de tabloları sizin elle oluşturmanıza gerek yoktur! Aşağıdaki komutu çalıştırdığınızda Odoo, Python modellerini okuyacak ve veritabanı şemasını sizin için sıfırdan çizecektir:

```bash
./start.sh -i ks_it_assets
```

*Not: `-i` parametresi (install) modülü kurar. Sonraki çalıştırmalarınızda kod güncellemelerini yansıtmak için `./start.sh -u ks_it_assets` (update) kullanmalısınız.*

### 4. Arayüze Erişim
Kurulum bittikten sonra geliştirme (local) ortamında tarayıcınızdan `http://localhost:8069` adresine giderek sisteme giriş yapabilirsiniz. 

*(Not: Eğer sistem canlı sunucuya (Production) alınırsa, tarayıcıdan localhost yerine doğrudan sunucunun IP adresi veya kurumun belirlediği alan adı - örneğin: `https://erp.kaleseramik.com` - üzerinden sisteme girilir. Port numarası veya ek bir kurulum gerekmez, Odoo web portunu otomatik dışarı açar.)*

## 🤝 İş Akışı (Business Logic) Notları
Bu modül, büyük işletmelerin "Lokasyon/Fiziksel Durum" ile "Yasal Zimmet" ayrımını yapabilmesi için tasarlanmıştır. Örneğin; bir laptop garantiye (servise) gönderildiğinde personelin üzerindeki "zimmeti" yasal olarak düşmez, sadece "arızalı" veya "serviste" durumuna geçer. Bu sayede personel ve cihaz arasındaki kurumsal bağ kopmamış olur.

---

## ⚖️ Lisans ve Telif Hakkı (License)

**Proprietary License (Özel Ticari Lisans)** Bu yazılımın tüm telif hakları geliştiricisine aittir. Kaynak kodları kopyalanamaz, çoğaltılamaz, izinsiz dağıtılamaz, değiştirilemez veya farklı bir marka/isim altında ticari olarak satılamaz. Yazılımın her türlü ticari kullanımı, kurulumu ve kurumsal entegrasyonu tamamen geliştiricinin özel iznine ve lisans sözleşmelerine tabidir.

---

**Serhan Ağan** tarafından *Kaleseramik ERP ve Kurumsal Entegrasyon Projeleri Kapsamında Geliştirilmiştir.*
