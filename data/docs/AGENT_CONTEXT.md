# Agent Context

Bu dosya, projeye yeni giren AI agentların hızlı bağlam kazanması için tek sayfalık özetidir.

## Proje Amacı
- Hostun fotoğraf/video/doküman medyalarını ekleyip izleyici ekranına yansıtması.
- Sunum dosyalarının (PPTX, DOCX, XLSX, PDF) yüksek kaliteli imajlara dönüştürülüp izletilmesi.

## Güncel Durum (2026-03-15 - Güncelleme 2)
- **Backend**: FastAPI, PDF'leri kaydırılabilir medya olarak işler.
- **Kaydırma Senkronizasyonu**: Host üzerindeki PDF kaydırma hareketi otomatik olarak tüm izleyicilere (WebSocket üzerinden) yansıtılır.
- **Hata Yönetimi**: 500 hataları için terminal/log yönlendirmeli detaylı hata paneli eklendi.
- **Dönüşüm**: PPTX/DOCX → LibreOffice; PDF → Doğrudan Render (PyMuPDF).
- **Frontend**: `host.html` (yönetim) ve `viewer.html` (izleyici). 
- **Senkron**: WebSocket (birincil) veya 350ms Polling (yedek).
- **Paketleme**: PyInstaller ile tek dosya EXE (`Q-Slidee.exe`).

## Önemli Dosyalar
- `app/server.py`: Belge işleme ve API lojiği.
- `app/host.py`: Uygulama başlatıcı ve port yönetimi.
- `app/web/host.html`: Host arayüzü ve API entegrasyonu.
- `app/web/viewer.html`: İzleyici ekranı.

## Çalışma Kuralı
- Yeni özellik eklendiğinde `MD_Dosyaları` altındaki tüm dokümanlar (`AGENT_CONTEXT`, `ARCHITECTURE`, `CHANGELOG`, `NEXT_STEPS`) güncellenir.
- Kod "DRY" (Don't Repeat Yourself) prensibine göre optimize tutulur.
