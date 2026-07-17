#!/usr/bin/env bash
set -euo pipefail

mkdir -p assets/products

fetch() {
  local slug="$1" url="$2" ext="$3"
  curl -L --fail --silent --show-error --max-time 60 -A 'Mozilla/5.0' "$url" -o "assets/products/${slug}.${ext}"
}

fetch truu-fountain-3 'https://www.truu.com/fileadmin/_processed_/0/f/csm_fountain-for-web_ad3701fcc1.png' png
fetch mrwater-premium-ro 'https://misterwater.eu/wp-content/uploads/SilverStar_5.png' png
fetch wertach-pantera 'https://wertach-quelle.shop/wp-content/uploads/pantera-product2-ws-home-beschriftet.webp' webp
fetch osmofresh-fusion-pro 'https://www.osmofresh.de/media/44/a3/60/1773822405/OF_PD_FusionPro_1600x1600px_G01.webp' webp
fetch greifenstein-inox 'https://greifenstein-wasser.de/wp-content/uploads/2016/03/INOX-Umkehrosmoseanlage-edelstahl.jpg' jpg
fetch wasserhaus-zen-flow 'https://www.wasserhaus.de/media/catalog/product/cache/6313a447ba58f50f694423d100027e83/z/e/zen-flow-mit-osmosehahn-led_10.jpg' jpg
fetch arktisquelle-direct-flow-premium 'https://arktisquelle.de/cdn/shop/files/ProduktbildColdFriendlyOffer-Weiss_c315947d-1c19-4fa2-9a22-8de2b2cf1968.png?v=1783893381&width=1500' png
fetch myaqua-1900 'https://www.arka-biotech.de/fileadmin/_processed_/5/e/csm_myAQUA1900_Detail_c9ea9ae75c.jpg' jpg
fetch purway-pur-booster-quick 'https://shop.purway.de/cdn/shop/files/pur_booster_7.jpg?crop=center&height=1005&v=1782862244&width=1005' jpg
fetch osmounity-direct-flow 'https://osmounity.de/media/bf/14/72/1725001579/anlage4mitgestell-gross.jpg' jpg
fetch bwt-aqa-drink-pro-20 'https://www.bwt.com/media/f1/29/a5/1666091755/BWT_AQADrink_20CAS_Auftisch_030Grad.png' png
fetch bwt-bestaqua-roc 'https://www.bwt.com/pl-pl/-/media/bwt/global-data/images/professional/produktbilder/bwt_bestaqua_roc_16_1280x1280.png?rev=db1dd460f81941419a43059b5e6ca339&h=1280&w=1280' png
fetch gruenbeck-geno-osmo-x 'https://www.gruenbeck.de/fileadmin/user_upload/02_Produkte/Frischwasser/Membrantechnik/GENO-OSMO-X_web_big.png' png
fetch alfiltra-ro-professional 'https://www.alfiltra.de/image/filtraselect-reos-plug-and-play-reverse-osmosis-system.jpg?width=1200&max-height=1200' jpg
fetch aquion-premium-7 'https://aquion.de/templates/yootheme/cache/c9/Premium5000-Kuechenzeile-Fenster-c9f38047.jpeg' jpg
fetch quooker-front-cube 'https://images.eu.ctfassets.net/vmooolt7lvvp/7dnuv5YjoespvRWUlXeTwy/0960ae7e2e603a680d7ef006056ed38b/2146_FTBLK_Front_tap_Black_Quooker_pantry.jpg?fm=webp&q=100&w=1200' webp
fetch brita-mypure-p1 'https://sw.brita.de/thumbnail/b1/0a/72/1696590821/brita-consumer-mypure-P1-P1000-filter-under-the-sink-kitchen-2019-1576_280x280.jpg?ts=1716459196' jpg
fetch franke-mythos-water-hub 'https://www.franke.com/product-images/ALL/390-1x1/PP001_160.0708.955.jpg' jpg
fetch blanco-unit-drink-systems 'https://blancoprod-media.e-spirit.cloud/9f636415-de00-4f0d-b9ac-5d43b09ce3ee/bilder/unit-communication/taps-1/shape-001.webp' webp
fetch bela-aqua-oblige-directflow 'https://bela-aqua.de/web/image/333496/Bela-Aqua-OBLIGE-Touch-Panel.jpg' jpg
fetch gewapur-osmo-star-2 'https://gewapur.de/wp-content/uploads/2024/08/osmostar-2-inkl.wasserhahn.webp' webp
