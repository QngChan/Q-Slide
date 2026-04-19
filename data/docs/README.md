<<<<<<< HEAD:README.md
Q-Slide
=======
# Q-Slidee Conference
>>>>>>> 3d18819 (Refactor: Move files to src/ and web/, update docs and .gitignore):data/docs/README.md

Q-Slide iki ekrandan oluşur:

Sunucu (Host) ekranı: Web tabanlı bir paneldir. Masaüstünde uygulama penceresi (Edge/Chrome --app) olarak açılır.

<<<<<<< HEAD:README.md
İzleyici (Viewer) ekranı: Yalnızca aktif fotoğraf veya video içeriğini gösterir.
=======
## Urun Modeli (Guncel)
- Metin/slayt yayinlama yok.
- Host:
  - foto/video dosyasi yukler,
  - PowerPoint (`.pptx`), Word (`.docx`), Excel (`.xlsx`/`.xls`) ve **PDF (`.pdf`)** yukler ve slaytlari dogrudan sunum modunda render eder,
  - medya kutuphanesinden secip izleyiciye yansitir,
  - sunumlar icin onceki/sonraki slayt komutlarini verir,
  - sagdaki buyuk side preview panelinde izleyicinin gordugunu canli izler.
- Viewer:
  - ilk acilista bos ekran gorur,
  - host aktif medya sectiginde onu tam ekran gorur.
>>>>>>> 3d18819 (Refactor: Move files to src/ and web/, update docs and .gitignore):data/docs/README.md

Ürün Modeli
Sunucu (Host)

Fotoğraf ve video dosyası yükler.

PowerPoint (.pptx) dosyası yükler ve slaytları doğrudan sunum modunda gösterir (PNG dosyası üretmez).

Medya kütüphanesinden içerik seçerek izleyici ekranına yansıtır.

PowerPoint için önceki ve sonraki slayt komutlarını yönetir.

Sağ tarafta bulunan büyük ön izleme panelinde, izleyicinin gördüğünü canlı olarak takip eder.

İzleyici (Viewer)

İlk açılışta boş ekran görüntülenir.

<<<<<<< HEAD:README.md
Sunucu aktif bir medya seçtiğinde, bu içerik tam ekran olarak gösterilir.
=======
```bash
python -m app.host
```

Host uygulamasi acildiginda ayni anda web sunucusu da baslar.
- Varsayilan port `8100` doluysa otomatik olarak bos bir porta gecer.
- Host app-window ve izleyici linki terminalde yazdirilir.
- WebSocket kutuphanesi yoksa sistem polling fallback ile calismaya devam eder.
- PowerPoint senkronu icin Microsoft PowerPoint gerekmez.
- Render uygulama icinde yerel olarak yapilir (`python-pptx`).

## EXE Build (Windows)

```powershell
.\build_exe.ps1
```

EXE cikisi:
- `dist\Q-Slidee.exe`

Notlar:
- PyInstaller kurulumlari `requirements-dev.txt` icindedir.
- `app/web` dosyalari EXE icine dahil edilir.

## Dokumantasyon (Agent Context)

Yeni bir AI agent bu projede calismaya baslamadan once asagidaki dosyalari okumali:

1. `AGENT_CONTEXT.md`
2. `ARCHITECTURE.md`
3. `CHANGELOG.md`
4. `NEXT_STEPS.md`

Her yeni ozellik veya davranis degisikliginde bu dosyalar ayni degisiklikte guncellenmelidir.
>>>>>>> 3d18819 (Refactor: Move files to src/ and web/, update docs and .gitignore):data/docs/README.md
