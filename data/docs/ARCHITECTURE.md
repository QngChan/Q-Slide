# Architecture

## Bilesenler

### 1) Host Desktop Launcher
- Dosya: `app/host.py`
- Gorevler: FastAPI server'i baslatir, port cakismasini yonetir, tarayiciyi acar.
- Platform: Windows, Linux, macOS uyumlu (tarayici acma icin platform-bagli kod)
- Ozellikler: 
  - tkinter ile capraz-platform popup destegi
  - Host sekmesi kapatildiginda otomatik uygulama kapatma (heartbeat sistemi)
  - Windows: `ctypes.windll`, `os.startfile`, Edge/Chrome PATH arama
  - Linux: `xdg-open`, `gio`, `gnome-open`, webbrowser fallback

### 2) Host Web UI
- Dosya: `app/web/host.html`
- Teknoloji: HTML/CSS/JS (Vanilla)
- Gorevler: Medya yonetimi, sunum kontrolu, BGM ayarlari.
- Ozellikler: 
  - 3 saniyede bir heartbeat ping'i (`/api/host/alive`)
  - `beforeunload`/`pagehide` eventleri ile kapatma bildirimi (`/api/host/bye`)

### 3) API + WebSocket Server
- Dosya: `app/server.py`
- Teknoloji: FastAPI
- Gorevler: State yonetimi, dosya yukleme, belge donusturme (PDF/PPTX/DOCX/XLSX).
- Endpointler:
  - `/api/host/alive`: Host istemci heartbeat kabul eder
  - `/api/host/bye`: Host istemci cikis bildirimi kabul eder
  - Diger: medya upload, PPT kontrol, BGM, scroll sync

### 4) Viewer Web UI
- Dosya: `app/web/viewer.html`
- Gorevler: Canli yayin elemani. WebSocket/Polling senkronizasyonu.
- Tema: Tamamen siyah tonlarinda minimalist gorunum.

## Veri Akisi
1. Host dosyayi yukler (`/api/media/upload` veya `/api/ppt/upload`).
2. Server belgeyi slaytlara (PNG/Text) donusturur.
3. Host aktif medyayi secer, server WebSocket uzerinden Viewer'lara state'i yayinlar.
4. Viewer anlik olarak elemani gunceller.
5. Host sekmesi kapanirsa, uygulama heartbeat yoklugundan otomatik kapanir.
