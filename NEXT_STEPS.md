# Next Steps

Bu dosya acik isleri ve sonraki gelisim adimlarini tutar.

## Oncelik 1
- PowerPoint icin "slayt numarasina git" (direct goto) kontrolu
- PowerPoint import hatalarinda daha detayli host UI hata raporu
- Medya kutuphanesinde siralama/arama/etiketleme
- Medya silme ve yeniden adlandirma
- Izleyici sayisi gostergesi (canli bagli client sayisi)
- BGM playlist (sirali/crossfade) destegi
- Autoplay unblock adimi icin hostta "izleyicide bir kez dokun" yonlendirmesi
- Bucket bazli medya tasima (music <-> presentation) araci
- Kart tiklamasi icin cift tiklama/tek tiklama tercihi ayari

## Operasyon Notu
- Ortam kurulumunda `pip install -r requirements.txt` calismadan host baslatilmamali.
- WebSocket backend yoksa sistem polling fallback ile yine calisir.
- EXE build icin `.\build_exe.ps1` ve `q-slidee.spec` kullanilir.
- `pywin32==311` gereksinimi Windows COM destegi icin zorunludur.
- EXE cikisi: `dist\\Q-Slidee.exe`
- EXE hata logu: `Q-Slidee.log`
- EXE icinde uvicorn baslatma loglari `Q-Slidee.log` dosyasina yazilir.
- EXE icinde uvicorn log formatter hatasi `log_config=None` ile giderildi.

## Oncelik 2
- State persistence (uygulama yeniden basladiginda medya listesi + aktif medya korunmasi)
- Drag-drop ile toplu medya yukleme
- Buyuk dosyalarda yukleme ilerleme gostergesi

## Oncelik 3
- Mobil viewer optimizasyonu
- Oynatilan video icin uzaktan play/pause/seek kontrolu
- Docker compose ile paketli calistirma

## Guncelleme Kurali
- Bir is tamamlandiginda bu dosyada ilgili madde:
  - tamamlandi olarak isaretlenmeli veya kaldirilmali
  - gerekiyorsa yeni alt maddeler eklenmeli

## Son Guncelleme
- 2026-03-12: Host UI'ya Siyah/Açık tema secici eklendi; varsayilan tema siyah.
- 2026-03-12: Host UI tema paletleri gri skala olacak sekilde guncellendi.
- 2026-03-12: Host UI yukleme bolumunde “Gozat” girdi alani gizlendi; yukleme butonlari dosya secip otomatik yukler hale getirildi.
- 2026-03-12: Terminalsiz baslatma icin `start_host.pyw` eklendi, `host.py` print cikisleri guvenli hale getirildi.
- 2026-03-12: PPT upload `uuid` import hatasi giderildi.
- 2026-03-12: LibreOffice tespit mantigi Windows PATH + Program Files dizinleri ile iyilestirildi.
- 2026-03-12: Sunum coklu yukleme + PDF/Excel destegi eklendi.
- 2026-03-12: Sunum medya/dokuman yukleme alani birlestirildi ve desteler kutuphanede gosterilir.
- 2026-03-12: Host panel klasik yerlesime geri alindi.
- 2026-03-12: Sunum destelerine kutuphane onizlemesi eklendi.
- 2026-03-12: Viewer bos durumunda animasyonlu "Q Slide" marka yazisi gosterimi eklendi.
- 2026-03-12: EXE build notu (PyInstaller spec + build script) eklendi.
- 2026-03-12: `pywin32` 311'e guncellendi ve PyInstaller spec koku cozumu duzeltildi.
- 2026-03-12: EXE hata logu (`Q-Slidee.log`) eklendi.
- 2026-03-12: EXE icinde uvicorn baslatma loglari eklendi.
- 2026-03-12: EXE icin uvicorn log formatter hatasi giderildi.
- 2026-03-14: Host kutuphane onizlemeleri lazy-load edildi; video kartlari metadata preload ile hafifletildi.
- 2026-03-14: Viewer bos ekran animasyonlari `prefers-reduced-motion` ile azaltilir hale getirildi.
- 2026-03-14: Host LibreOffice durum kontrol araligi 10 saniyeye cikarildi.
- 2026-03-14: Viewer durum metni sadece degistiginde guncellenerek gereksiz DOM isleri azaltildi.
