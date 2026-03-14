# Architecture

## Bilesenler

### 1) Host Desktop Launcher
- Dosya: `app/host.py` (opsiyonel terminalsiz baslatma: `start_host.pyw`)
- Teknoloji: Python stdlib + tarayici `--app` modu
- Gorevler:
  - WebSocket backend uygunlugunu kontrol eder (`websockets` veya `wsproto`)
  - FastAPI server'i arka planda baslatir
  - Varsayilan `8100` doluysa otomatik bos port secer
  - `http://127.0.0.1:<port>/host` adresini Edge/Chrome app-window olarak acar
  - Ek GUI kutuphanesi gerektirmez

### 2) Host Web UI
- Dosya: `app/web/host.html`
- Teknoloji: plain HTML/CSS/JS
- Gorevler:
  - Foto/video dosyalarini yukler (`/api/media/upload`)
  - Sunum dokumanlari yukler (`/api/ppt/upload`) ve medya yukleme alanindan yonlendirilir
  - Yukleme butonlari dosya secim penceresini acar ve secimden sonra otomatik yukleme baslar
  - Yuklenen sunumu secer (`/api/ppt/select`)
  - PowerPoint slaytlarini onceki/sonraki ilerletir (`/api/ppt/prev`, `/api/ppt/next`)
  - Medya kutuphanesini listeler (`/api/media`)
  - Secili medyayi izleyiciye yansitir (`/api/media/show`)
  - Audio/video kaynaklarindan arka plan muzigi secer (`/api/bgm/set`)
  - BGM play/pause/stop/restart/volume kontrolu yapar (`/api/bgm/control`)
  - Video oynatma komutlarini gonderir (`/api/video/control`)
  - Izleyici ekranini buyuk iframe onizleme panelinde gosterir (resizable side panel + ac/kapat)
  - Medya kutuphanesini iki ayri bolumde sunar:
    - Sunum medyalari (image/video)
    - Muzik medyalari (audio/video)
  - Kutuphane kartlari tiklanabilir aksiyon modelindedir (ek buton yok):
    - Sunum karti tiklama -> `/api/media/show`
    - Muzik karti tiklama -> `/api/bgm/set`
  - Tema secici (Siyah/Açık) bulunur; acilista varsayilan tema siyah, paletler gri skala (#000000-#BFBFBF / #C0C0C0-#FFFFFF)
  - Kutuphane onizlemeleri lazy-load kullanir; video kartlari metadata preload ile daha hafif yuklenir.
  - LibreOffice durum kontrolu 10 saniyelik aralikla yenilenir.
  - Sunum desteleri sunum kutuphanesinde listelenir ve tiklayinca aktif edilir.
  - Yerlesim:
    - Sol panel: sunum yukleme, sunum dosyalari, ses yukleme + ses kontrolleri
    - Sag panel: canli onizleme iframe + altta video kontrol alani

### 3) API + WebSocket Server
- Dosya: `app/server.py`
- Teknoloji: `FastAPI`
- Veriler:
  - In-memory `ConferenceState`
  - Alanlar: `media_items[]`, `current_media_id`, `bgm_media_id`, `video_control`, `bgm_control`, `bgm_volume`
  - Medya kayitlarinda `bucket` alani bulunur (`presentation` veya `music`)
  - PowerPoint deck kayitlari tutulur (`ppt_decks[]`, `active_ppt_id`, `current_index`)
- Endpointler:
  - `GET /` -> viewer HTML
  - `GET /host` -> host HTML
  - `GET /api/state` -> aktif medya state
  - `GET /api/media` -> medya listesi
  - `GET /api/ppt` -> sunu listesi, aktif slayt bilgisi ve onizleme gorseli
  - `POST /api/media/upload` -> foto/video yukle
  - `POST /api/ppt/upload` -> `.pptx/.docx/.xlsx/.pdf` yukle, slaytlari dogrudan sunum verisi olarak parse et
  - `POST /api/ppt/select` -> aktif sunuyu sec
  - `POST /api/ppt/prev` -> onceki slayt
  - `POST /api/ppt/next` -> sonraki slayt
  - `POST /api/media/show` -> secilen medyayi aktif et + broadcast
  - `POST /api/bgm/set` -> secilen medya ile BGM belirle + broadcast
  - `POST /api/bgm/control` -> BGM kontrol komutlari + broadcast
  - `POST /api/video/control` -> video kontrol komutlari + broadcast
  - `WS /ws` -> canli izleyici baglantisi
  - `GET /media/*` -> yuklenen dosyalarin statik servisi
  - Belge Donusum Hatti (PPTX/DOCX):
    - 1. Tercih: LibreOffice + PyMuPDF (PDF -> PNG). Slaytlar yuksek cozunurluklu gorseller olarak sunulur.
    - 2. Tercih (Sadece PPTX): Windows COM (PNG export).
    - 3. Tercih: Manuel parser (Nesne tabanli render).
  - PPT upload icin `uuid` uretimi kullanilir (import eksikligi 2026-03-12'de duzeltildi).
  - LibreOffice tespiti Windows PATH + Program Files kurulum dizinleri ile yapilir (2026-03-12).
  - PDF yuklemeleri PyMuPDF ile dogrudan sayfa render eder (2026-03-12).

### 4) Viewer Web UI
- Dosya: `app/web/viewer.html`
- Teknoloji: plain HTML/CSS/JS
- Davranis:
  - Acilista bos ekran gosterir
  - Gelen state'e gore image/video render eder
  - Bos durumda animasyonlu "Q Slide" marka yazisi gosterir
  - Video kontrol butonlari yoktur (host-only kontrol)
  - BGM kaynagini gizli audio/video elementinde oynatir
  - Tarayici autoplay engeli olursa kullaniciya "Medyayi Etkinlestir" adimi gosterir
  - Komutlardaki `at_ms` zaman damgasina gore video/BGM `currentTime` gecikme telafisi uygular
  - WebSocket yoksa polling fallback ile state ceker
  - `prefers-reduced-motion` ile bos ekran animasyonlari azaltilir; durum metni degismedikce DOM guncellenmez.

## Veri Akisi
1. Host panelinde medya secimi yapilir (normal medya veya PowerPoint).
2. Host panel, `POST /api/media/upload` veya `POST /api/ppt/upload` ile icerik ekler.
3. PowerPoint yuklemede server slaytlari nesne modeline cevirir (PNG dosya uretmez).
4. Host panel, kart tiklamasi veya PPT prev/next komutlariyla aktif slaydi/medyayi secer.
5. Server aktif medyayi kaydeder ve websocket istemcilerine state broadcast eder.
6. Viewer websocket veya polling ile aktif medyayi anlik gorur.
7. Host, BGM ve video kontrol komutlarini API ile yollar; viewer bu komutlari uygular.

## Build & Dagitim
- PyInstaller spec: `q-slidee.spec` (`app/host.py` entrypoint)
- Web UI dosyalari EXE icine `app/web` olarak dahil edilir.
- Build komutu: `.\build_exe.ps1`
- PyInstaller icin `pywin32==311` gereksinimi kullanilir.
- EXE cikisi tek dosya: `dist\\Q-Slidee.exe`
- EXE hata logu: `Q-Slidee.log` (EXE ile ayni klasorde)
- Uvicorn baslatma hatalari log dosyasina yazilir.
- EXE modunda uvicorn log konfigurasyonu devre disidir (`log_config=None`).
