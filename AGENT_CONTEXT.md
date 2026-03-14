# Agent Context

Bu dosya, projeye yeni giren AI agentlarin hizli baglam kazanmasi icin tek sayfalik ozetidir.

## Proje Amaci
- Hostun foto/video medyalarini ekleyip izleyici ekranina yansitmasi
- Izleyicinin sadece aktif medyayi gormesi (metin/slayt formu yok)

## Guncel Durum (2026-03-08)
- Host UI: `app/web/host.html` (medya yukleme kutusu + medya kutuphanesi + secip yansitma)
- Host shell: `app/host.py` (Edge/Chrome `--app`, otomatik port secimi)
- Terminal gorunmeden baslatmak icin `start_host.pyw` launcher eklendi.
- Backend: `app/server.py` (`FastAPI`, media upload, PowerPoint upload/export, aktif medya state, websocket + polling uyumlu)
- Viewer: `app/web/viewer.html` (bos ekran + aktif image/video gosterimi)
- Viewer bos durumunda metin yerine animasyonlu "Q Slide" marka yazisi gosterir.
- Host tarafinda buyuk on-izleme side paneli var ve boyutu ayarlanabilir.
- `websockets` yoksa sistem polling fallback ile calismaya devam eder.
- Arka plan muzigi (BGM) eklendi: audio/video kaynaktan calabilir.
- Video kontrolu sadece host tarafindan yapilir; izleyici ekraninda video kontrolleri kapali.
- Viewer tarafinda autoplay engeli icin "Medyayi Etkinlestir" katmani eklendi.
- Host kutuphane gorunumu ikiye ayrildi:
  - Sunum medyalari (image/video)
  - Muzik medyalari (audio/video)
- Host arayuzu yeni duzende:
  - Sol: sunum yukleme + sunum dosyalari + ses alanlari
  - Sag: buyuk onizleme ve altta video kontrolleri
- Medya yukleme artik bucket bazli:
  - `presentation` yuklenenler sadece sunum bolumune gider.
  - `music` yuklenenler sadece muzik bolumune gider.
- Viewer senkronu iyilestirildi:
  - Video/BGM komutlarinda zaman damgasi ile gecikme telafisi uygulanir.
- Yukleme sonrasi otomatik baslatma yoktur; medya host tarafinda tiklaninca etkinlestirilir.
- Host kutuphane kartlari butonsuzdur:
  - Sunum kartina tiklama -> yansitma
  - Muzik kartina tiklama -> muzik secimi
- PowerPoint ve Word es zamanli sunum sistemi (Option 3 - 2026-03-08):
  - Yuksek kaliteli render icin LibreOffice (`soffice`) kullanılır.
  - Dosyalar PDF'e dönüştürülüp `PyMuPDF` ile 1920px genişliğinde PNG olarak işlenir.
  - LibreOffice yoksa Host UI uzerinden otomatik kurulum (MSI) secenegi sunulur.
  - Yedek olarak `python-pptx` / `python-docx` ve Windows COM (`pywin32`) mantigi korunur.
- PPT upload endpointinde `uuid` import eksikligi giderildi (2026-03-12).
- LibreOffice tespiti Windows PATH ve yaygin kurulum dizinlerini kapsayacak sekilde genisletildi (2026-03-12).
- Sunum yukleme alani coklu dosya destekler (PPTX/DOCX/XLSX/PDF) ve PDF/Excel girisi eklendi (2026-03-12).
- Sunum yukleme tek alanda birlestirildi (medya + dokuman) ve sunum desteleri sunum kutuphanesinde listelenir (2026-03-12).
- Host UI, onceki (klasik) panel tasarimina geri alindi (2026-03-12).
- Sunum desteleri kutuphane karti olarak gorunur ve ilk slayt gorseliyle onizleme sunar (2026-03-12).
- Host UI'da dosya secimi icin “Sunum Dosyasi Ekle / Muzik Medyasi Ekle” butonlari dosya penceresini acar ve secimden sonra otomatik yukler (2026-03-12).
- Host UI tema secici eklendi (Siyah/Açık); varsayilan tema siyah (2026-03-12).
- Tema paletleri gri skala (Siyah: #000000-#BFBFBF, Açık: #C0C0C0-#FFFFFF) olarak ayarlandi (2026-03-12).
- PyInstaller ile EXE build icin `q-slidee.spec` ve `build_exe.ps1` eklendi; dev bagimliliklari `requirements-dev.txt` altina alindi (2026-03-12).
- PyInstaller build icin `pywin32` surumu 311'e guncellendi; spec dosyasinda proje koku `Path.cwd()` ile tespit edilir (2026-03-12).
- EXE cikisi tek dosya olarak `dist\\Q-Slidee.exe` uretir (2026-03-12).
- EXE calistiginda hata ayiklama icin `Q-Slidee.log` dosyasina log yazar (2026-03-12).
- EXE icinde uvicorn baslatma hatalari loglanir; secilen port loga yazilir (2026-03-12).
- EXE'de uvicorn log formatter hatasi icin `log_config=None` kullanilir (2026-03-12).
- Host kutuphane onizleme gorselleri lazy-load edilir; video onizlemeleri metadata preload ile hafifletilir (2026-03-14).
- Viewer bos ekran animasyonlari `prefers-reduced-motion` ile azaltilir; durum metni gereksiz DOM guncellemesi yapmaz (2026-03-14).
- Host LibreOffice durum kontrolu 10 saniyelik aralikla yapilir (2026-03-14).

## Hemen Bakilacak Dosyalar
- `app/host.py`
- `app/server.py`
- `app/web/host.html`
- `app/web/viewer.html`
- `README.md`

## Calisma Kurali
- Yeni ozellik eklendiginde veya davranis degistiginde su dosyalar guncellenir:
  - `AGENT_CONTEXT.md`
  - `ARCHITECTURE.md`
  - `CHANGELOG.md`
  - `NEXT_STEPS.md`
- Kod degisimi varsa dokumantasyon guncellemesi ayni degisiklik setinde yapilir.
