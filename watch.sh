#!/bin/bash

echo "🔥 Odoo Hot-Reload (KS IT Envanter Takip) Başlatılıyor..."
echo "Artık sadece kaydetmeniz (Cmd + S) yeterli. Herhangi bir Python (.py), XML (.xml) veya CSV (.csv) dosyası değiştiğinde Odoo bunu otomatik algılayıp kendini GÜNCELLEYEREK yeniden başlatacaktır."
echo "Tarayıcıyı yenilemeden (Cmd + R) önce terminalde 'Yeniden başlatılıyor...' yazısını gördüğünüzden emin olun."
echo "Durdurmak için Ctrl + C tuşlarına basabilirsiniz."
echo "------------------------------------------------"

# Güvenli çıkış için trap
trap "echo 'Kapatılıyor...'; kill \$ODOO_PID 2>/dev/null; exit" SIGINT SIGTERM

last_sum=""

while true; do
    # Modül dosyalarının son değiştirilme tarihlerini al ve MD5 ile hashle
    current_sum=$(find ks_it_assets -type f \( -name "*.py" -o -name "*.xml" -o -name "*.csv" -o -name "*.scss" -o -name "*.js" \) -exec stat -f "%m" {} + | md5)
    
    if [ "$last_sum" != "$current_sum" ]; then
        if [ ! -z "$last_sum" ]; then
            echo "🔄 Değişiklik algılandı! Sunucu modülü güncelleyerek yeniden başlatılıyor..."
            kill $ODOO_PID 2>/dev/null
            wait $ODOO_PID 2>/dev/null
        fi
        
        last_sum=$current_sum
        
        # Odoo'yu başlat, -u ks_it_assets parametresini EKLE
        "/Users/serhanagan/Developer/Odoo Core/venv/bin/python" "/Users/serhanagan/Developer/Odoo Core/odoo-bin" -c "/Users/serhanagan/Developer/Kaleseramik_ERP/KS Envanter Takip/odoo.conf" --dev=all -u ks_it_assets "$@" &
        ODOO_PID=$!
    fi
    sleep 2
done
