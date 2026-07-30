# KS IT Envanter Takip - Blueprint

## Staj Defteri Hikayesi

**Proje:** KS IT Envanter Takip - Bilgi Teknolojileri Zimmet, Ödünç ve Arıza Yönetimi Platformu

**Hikaye Özeti:**
"Şirketin Bilgi İşlem (IT) departmanı, yüzlerce bilgisayar, monitör, yazılım lisansı ve donanımın takibini, kimde zimmetli olduğunu ve arıza/garanti süreçlerini kopuk dosyalarla yönetiyordu. Hangi cihazın kimde geçici ödünç olarak durduğu, tamirdeki cihazın ne durumda olduğu bilinemiyordu. Ben bu spesifik sorunu çözmek için Kaleseramik_ERP altyapısına yeni ve bağımsız bir IT Varlık Yönetim Modülü (KS IT Envanter) ekledim."

**Hikayenin Katmanları:**
*   **🔴 Problem:** Manuel tutanaklar, cihaz lokasyonunun (kimde olduğunun) anlık bilinememesi, garanti sürelerinin kaçırılması ve teknik servis süreçlerinin belirsizliği.
*   **🔧 Çözüm Süreci:** Odoo üzerinde özel modeller tasarlandı. Varlıklar (Cihazlar), Zimmet/Ödünç (Atama işlemleri) ve Teknik Servis kayıtları birbirine bağlandı. OWL (Odoo Web Library) kullanılarak JavaScript tabanlı anlık bir gösterge paneli (Dashboard) oluşturuldu.
*   **🟢 Sonuç:** IT personeli tek ekrandan tüm envanterin özetini gördü, süresi dolan cihazları fark etti ve şirket içi donanım akışı tam kontrol altına alındı.
*   **📊 Teknik Derinlik:** Çoklu ilişkilendirilmiş Python modellemesi (One2many, Many2one), Odoo OWL Framework (JavaScript/XML Dashboard), güvenlik katmanları ve özel SCSS teması.

---

## 📝 Staj Defteri Raporlama Taslağı (Tüm Projeler İçin Şablon)

Her proje staj defterine yazılırken şu yapıyı takip etmelidir:

1.  **Mevcut Durum (Problem):** Firma X şeyi Y şekilde yapıyordu, şu sorunlar vardı.
2.  **Analiz:** Ben şu gereksinimleri tespit ettim.
3.  **Tasarım:** Veri modeli, kullanıcı akışı, teknik mimari.
4.  **Geliştirme:** Hangi teknolojiyi neden seçtim, hangi güçlüklerle karşılaştım.
5.  **Sonuç:** Müdür/kullanıcı tepkisi, gerçek faydası.

---

## 🌟 Projeyi Zirveye Taşıyan Final Entegrasyonlar

Bu aşamalar projenin teknik derinliğini ve pratik faydasını en üst düzeye çıkarmak için sonradan eklenmiş, IT departmanının iş yükünü sıfıra indiren kritik geliştirmelerdir:

### 1. Garanti Süresi Takibi & Otomatik Uyarılar (Cron Job)
*   **Problem:** Yüzlerce cihazın garanti süresinin manuel tablolardan takip edilememesi ve hak kayıpları.
*   **Çözüm:** Arka planda çalışan bir Python **Cron Job (Zamanlanmış Görev)** yazıldı. Bu sistem, garanti süresinin bitimine 30 gün kalan tüm cihazları her gece otomatik tarayarak IT personeline sistem üzerinden bir aktivite (Odoo Activity) uyarısı veya bildirim atar.

### 2. Otomatik "Zimmet Teslim Tutanağı" Çıktısı (QWeb Report)
*   **Problem:** Cihaz teslimlerinde Word/Excel üzerinden manuel tutanak doldurmanın getirdiği zaman kaybı.
*   **Çözüm:** Odoo'nun **QWeb PDF Raporlama Motoru** kullanılarak, zimmet işlemi yapıldığı an tek tıkla şirket logolu, cihaz seri numaralı ve teslim alan personel bilgileriyle dolu, ıslak imzaya hazır bir PDF Tutanak üretimi sağlandı.

### 3. Dinamik QR Kod Üretimi ve PDF Etiket Basımı (QWeb)
*   **Problem:** Sahada yüzlerce cihaz arasında doğru ekipmanı bulmanın zorluğu ve donanımları fiziksel olarak numaralandırma/etiketleme ihtiyacı.
*   **Çözüm:** Python kütüphaneleri kullanılarak sisteme eklenen her IT donanımına (laptop, monitör, switch vb.) özel benzersiz bir QR kod üreten bir yapı entegre edildi. Ayrıca Odoo'nun QWeb raporlama motoruyla bu QR kodları cihazların üzerine yapıştırılacak kare etiketler (QR Label) formatında topluca çıktı almayı sağlayan PDF şablonları tasarlandı.

### 4. Ekstra (Blueprint'te Olmayan) Mükemmelleştirmeler
*   **Özelleştirilmiş Yönetim Paneli:** OWL (Odoo Web Library) JS tabanlı modern Dashboard.
*   **Koyu Tema Uyumluluğu:** CSS/SCSS ile Kaleseramik koyu temasına özel yüksek kontrastlı 7 farklı varlık kategorisi rengi (Neon renk paleti).
*   **Dinamik Tasarım:** Satır renkleriyle eşleşen ve transparan zemin kullanan Odoo Badge (Rozet) tasarımları.
*   **Kurumsal Servis Simülasyonu:** Teknik Servis mantığının kurumsal ERP iş akışına göre simüle edilmesi (Servis dönüşünde önceki zimmetin tanınması vb.).
*   **Dinamik Uyarılar:** Geciken ödünç zimmetler için dinamik hesaplanan durum tetikleyicileri (`display_state`).


## Yapılacaklar (To-Do) Listesi

- [x] **QR Kod ve Barkod Entegrasyonu:** Her IT donanımına (laptop, monitör, switch vb.) özel, benzersiz QR kod üreten yapının kodlanması ve Odoo QWeb raporlama motoru kullanılarak barkod etiketlerinin PDF şablonlarının tasarlanması.
- [x] **Otomatik Garanti ve Bakım Uyarı Sistemi (Cron Jobs):** Garanti süresinin bitimine örneğin 30 gün kalan cihazları tespit eden arka plan işlemlerinin (Scheduled Actions / Cron Jobs) yazılması ve IT ekibine otomatik Odoo/E-posta bildirimlerinin (email triggers) kurulması.
