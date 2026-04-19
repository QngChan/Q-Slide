# Changelog

Bu dosya, davranışsal değişiklikleri kronolojik olarak tutar.

## 2026-03-18
- **Host Paneli İzleyici Butonları**: Host ekranına iki yeni buton eklendi:
  - "İzleyiciyi Aç": İzleyici ekranını yeni sekmede açar
  - "URL Kopyala": İzleyici URL'sini panoya kopyalar
- **Tema Güncellemesi**: Host ve Viewer için tamamen siyah tonlarında yeni tema:
  - Viewer boş ekran: Q-SLIDE yazısı siyah (#1a1a1a) arka plan siyah (#000000)
  - Host ekranı: Siyah tonları ağırlıklı, minimalist görünüm
  - Renk paleti: #000000 - #3a3a3a arası gri/siyah tonları
- **Linux Uyumluluğu**:
  - `host.py`: Windows-spesifik `ctypes.windll` ve `MessageBoxW` kaldırıldı
  - `host.py`: Linux için `xdg-open`, `gio`, `gnome-open` tarayıcı açma desteği eklendi
  - `host.py`: `tkinter` fallback popup desteği eklendi
- **Host Kapatma Algılama**:
  - Host sekmesi kapandığında uygulama otomatik kapanır
  - 3 saniyede bir heartbeat sistemi eklendi
  - `/api/host/alive` ve `/api/host/bye` endpointleri eklendi
  - `beforeunload` ve `pagehide` eventleri ile kapatma algılama

## 2026-03-15
- **PDF Desteği**: Sunum dosyası olarak `.pdf` formatı doğrudan desteklenir hale getirildi.
- `server.py`: `.pdf` uzantısı izin verilen sunum formatlarına eklendi.
- `server.py`: Sunum yükleme akışına doğrudan PDF render stratejisi entegre edildi.
- `host.html`: Sunum ekleme alanındaki dosya seçici filtrelerine `.pdf` eklendi.
- Dokümantasyon: Proje genelindeki markdown dosyaları yeni PDF desteğine göre güncellendi.

## 2026-03-14
### Kod Optimizasyonu ve Refactoring
- `server.py`: Tekrarlanan PDF→PNG render kodu `_render_pdf_to_slides()` helper fonksiyonuna taşındı (~75 satır kod tasarrufu).
- `server.py`: `pythoncom` import'u platform bağımsızlığı (Linux uyumu) için koşullu yapıldı.
- `server.py`: `extract_docx_slides` içindeki kullanılmayan (ölü) kodlar temizlendi.
- `host.py`: Sunucu başlatma mantığındaki erişilemez (unreachable) duplicate exception bloğu düzeltildi.
- `host.html`: API isteklerindeki tekrarlı retry mantığı `makeRetryHandler` helper'ı ile merkezi hale getirildi.
- `host.html`: Dosya uzantı kontrolleri dinamik diziler yerine global `Set` sabitlerine taşınarak performansı artırıldı.
- `host.html`: `readResponseDetail` ve `parseErrorDetail` fonksiyonları tek bir yardımcı fonksiyonda birleştirildi.

### Hata Yönetimi ve UI/UX
- Host kutuphane onizlemeleri lazy-load edildi; video kartlari metadata preload ile hafifletildi.
- Host LibreOffice durum kontrol araligi 10 saniyeye cikarildi.
- Viewer bos ekran animasyonlari `prefers-reduced-motion` ile azaltilir hale getirildi.
- Viewer durum metni sadece degistiginde guncellenerek gereksiz DOM isleri azaltildi.
- Host baslatma ve calisma hatalari icin kullaniciya detayli cozum adimlari iceren popup mesajlari eklendi.
- Host web arayuzunde tum hata durumlari icin detayli popup rehberleri ve global hata yakalama eklendi.
- Host ve Host UI icin hata doktoru akisi (otomatik deneme + alternatif yol + bildirim) eklendi.
- Host UI yukleme alanlarina surukle-birak ile dosya yukleme eklendi.
- Host UI surukle-birak sirasinda desteklenmeyen dosyalar icin uyari bandi ve yukleme ilerleme gostergesi eklendi.
- Host UI uyari bandi otomatik kapanir hale getirildi; basarisiz dosyalar ayri hata panelinde listelenir.

## 2026-03-12
- Host UI'ya Siyah/Açık tema secici eklendi; varsayilan tema siyah.
- Host UI tema paletleri gri skala (Siyah: #000000-#BFBFBF, Açık: #C0C0C0-#FFFFFF).
- Host UI yükleme butonları dosya seçip otomatik yükler hale getirildi.
- Terminalsiz baslatma icin `start_host.pyw` eklendi.
- Sunum yukleme coklu dosya secimini destekler hale getirildi (PPTX/DOCX/XLSX/PDF).
- PDF dosyalari PyMuPDF ile render edilerek sunum akimina eklendi.
- Excel (XLSX/XLS) dosya destegi eklendi (LibreOffice gerektirir).
- PyInstaller EXE build sistemi kuruldu (`dist\Q-Slidee.exe`).

## 2026-03-08
- LibreOffice Entegrasyonu (Slayt kalitesi için PDF -> PNG hattı).
- `pymupdf` bağımlılığı eklendi.
- PowerPoint ve Word eş zamanlı sunum özelliği.
- BGM (Arka plan müziği) senkronizasyonu ve kontrolü.
- Viewer autoplay engeli çözümü ("Medyayı Etkinleştir").
- Host UI modern iki kolonlu düzene geçiş.
- WebSocket ve Polling fallback sistemi.
