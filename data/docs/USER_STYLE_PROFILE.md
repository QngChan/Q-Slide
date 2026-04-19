# User Style Profile (QngChan)

Bu dosya, projeye yeni katilan agentlarin kullanicinin calisma tarzina hizli adapte olmasi icin hazirlanmistir.

## 1) Iletisim Tarzi
- Dil tercihi: Turkce.
- Net, direkt ve teknik iletisim ister.
- Gereksiz uzun aciklama yerine sonuc odakli ilerlemeyi tercih eder.
- Sorun gordugunde hizli geri bildirim verir (`hala olmadi`, `simdi bunu ekleyelim` gibi).

## 2) Calisma Sekli
- Iteratif gelistirme sever:
  - once calisan MVP,
  - sonra hizli iyilestirme,
  - sonra paketleme (`exe`) ve gercek kullanim testi.
- Pratik deger ureten ozellikleri onde tutar (kullaniciya anlik fayda saglayan isler).
- "Yapalim" dediginde plan degil dogrudan uygulama bekler.

## 3) Teknik Tercihler (Gozlenen)
- Web tabanli UI + Python backend modelini sever.
- Masaustu calistirma icin hafif cozumleri tercih eder (`browser --app`, `pyinstaller`).
- Port cakismasi, startup, fallback gibi operasyonel dayanıkliliga onem verir.
- Cok cihazli kullanim (LAN/phone remote) gibi gercek kullanim senaryolarini onceler.

## 4) Guvenlik ve Kontrol Yaklasimi
- Ag uzerinden kullanimda pratik ama kullanisli guvenlik ister:
  - token,
  - trusted cihaz mantigi gibi.
- Kullanimi zorlastirmayan, ama kotuye kullanimi azaltan hafif korumalar tercih edilir.

## 5) UI/UX Tercihleri
- Gorsellik onemli ama islevin onune gecmemeli.
- Host ve Viewer rollerinin net ayrilmasini sever.
- Mobil/uzak kumanda tarafinda sade ve gorev odakli ekran ister.

## 6) Dokumantasyon Beklentisi
- Projede AGENTS.md kurallarina uyumu bekler.
- Degisikliklerde baglam dokumanlarinin da ayni committe guncellenmesini ister.
- Yeni agent onboarding'ini hizlandiracak ozet dosyalari degerli bulur.

## 7) Agent icin Uygulama Kurallari
- Her gorevde once mevcut proje dokumanlarini oku (`AGENTS.md` ve referans dosyalari).
- Degisiklik yaparken:
  - calisirlik,
  - hata toleransi,
  - paketleme (exe) etkisi,
  - gercek kullanim senaryosu etkisi
  birlikte degerlendir.
- "Calismiyor" geri bildirimi gelirse:
  - teorik tartisma yerine hizli reproduksiyon + log + fix uygula.
- Sonuc tesliminde:
  - degisen dosyalar,
  - calistirma komutu,
  - varsa kalan risk
  net olarak belirtilmeli.

## 8) Kisa Ozet (One-liner)
Kullanici, hizli iterasyonla gercek dunyada calisan, paketlenebilir, dayanıklı ve sade urun cikisini onceleyen pragmatik bir gelistirme tarzina sahip.
