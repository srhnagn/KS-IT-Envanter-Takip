# KS IT Asset Manager (Bilgi İşlem Varlık Yönetimi)

KS IT Asset Manager, Odoo 17 altyapısı üzerinde tamamen sıfırdan geliştirilmiş, kurumsal şirketlerin Bilgi İşlem (IT) departmanlarına özel kapsamlı bir donanım, lisans, zimmet ve arıza takip platformudur. 

Şirket içindeki tüm donanım hareketlerini (kimde, nerede, hangi durumda) saniyesi saniyesine izlemenizi sağlarken, teknik servis süreçlerini ve garanti takibini tek bir çatı altında toplar.

## ✨ Temel Özellikler (Key Features)

* **Detaylı IT Envanteri:** Bilgisayar, Monitör, Yazılım Lisansı, Ağ Cihazı, Akıllı Telefon/Tablet, Yazıcı ve Sarf Malzemeler için özel oluşturulmuş 7 farklı yüksek kontrastlı (Neon) renk kategorisiyle donanım takibi.
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
* **Barkod Altyapısı:** El terminalleri ve mobil cihazlar için veritabanında hazır bekleyen `barcode` mimarisi.

## 🛠 Kullanılan Teknolojiler
* **Backend:** Python 3.10+, Odoo 17 Framework, PostgreSQL
* **Frontend:** Odoo Web Library (OWL) JS, QWeb (XML), SCSS, Bootstrap
* **Mimari:** Modüler, MVC (Model-View-Controller) ve Object Relational Mapping (ORM)

## 🚀 Kurulum (Installation)
1. Modülü Odoo `addons/` klasörünüzün veya kendi custom eklenti yolunuzun içerisine taşıyın.
2. `odoo.conf` dosyanızda eklenti yolunu (addons_path) doğru tanımladığınızdan emin olun.
3. Odoo arayüzüne Geliştirici Modunda (Developer Mode) giriş yapıp "Uygulama Listesini Güncelle (Update Apps List)" seçeneğine tıklayın.
4. Uygulamalar (Apps) arasından **KS IT Envanter Takip** modülünü bularak kurun (Etkinleştirin).
5. (Opsiyonel) Odoo sunucusunu yeniden başlatarak JavaScript ve SCSS asset'lerinin derlenmesini sağlayın.

## 🤝 İş Akışı (Business Logic) Notları
Bu modül, büyük işletmelerin "Lokasyon/Fiziksel Durum" ile "Yasal Zimmet" ayrımını yapabilmesi için tasarlanmıştır. Örneğin; bir laptop garantiye (servise) gönderildiğinde personelin üzerindeki "zimmeti" yasal olarak düşmez, sadece "arızalı" veya "serviste" durumuna geçer. Bu sayede personel ve cihaz arasındaki kurumsal bağ kopmamış olur.

---
**Geliştirici:** Serhan Ağan 
*Kaleseramik ERP ve Kurumsal Entegrasyon Projeleri Kapsamında Geliştirilmiştir.*
