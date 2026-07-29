#!/bin/bash

echo "🔥 Odoo Native Hot-Reload Başlatılıyor..."
echo "✅ Watchdog kütüphanesi aktif! Python (.py) değişiklikleri otomatik algılanır ve Odoo GÜVENLE (port kapatmadan) kendini yeniler."
echo "✅ XML veya CSV değişiklikleri tarayıcıyı yenilediğiniz (Cmd + R) anda ANINDA yansır! (Eskisi gibi -u ile tam güncelleme beklemenize gerek yok)."
echo "Durdurmak için Ctrl + C tuşlarına basabilirsiniz."
echo "------------------------------------------------"

# Varsa askıda kalmış eski odoo süreçlerini (portları) temizle
kill $(pgrep -f "odoo-bin") 2>/dev/null
sleep 1

# Odoo'yu native --dev=all modu ile başlat
"/Users/serhanagan/Developer/Odoo Core/venv/bin/python" "/Users/serhanagan/Developer/Odoo Core/odoo-bin" -c "/Users/serhanagan/Developer/Kaleseramik_ERP/KS Envanter Takip/odoo.conf" --dev=all "$@"
