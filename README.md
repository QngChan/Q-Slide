# Q-Slidee Conference

Q-Slidee iki ekrandan olusur:

- Host ekrani: Web tabanli panel, masaustunde app-window olarak acilir (Edge/Chrome `--app`)
- Izleyici ekrani: Sadece aktif foto/video medyasini gosterir

## Urun Modeli (Guncel)
- Metin/slayt yayinlama yok.
- Host:
  - foto/video dosyasi yukler,
  - PowerPoint (`.pptx`) yukler ve slaytlari dogrudan sunum modunda render eder (PNG dosya uretmez),
  - medya kutuphanesinden secip izleyiciye yansitir,
  - PowerPoint icin onceki/sonraki slayt komutlarini verir,
  - sagdaki buyuk side preview panelinde izleyicinin gordugunu canli izler.
- Viewer:
  - ilk acilista bos ekran gorur,
  - host aktif medya sectiginde onu tam ekran gorur.

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Calistirma

```bash
python app/host.py
```

Terminal acilmasin isterseniz:

```bash
pythonw start_host.pyw
```

Windows'ta terminalsiz calistirmak icin `start_host.pyw` dosyasini cift tiklayabilirsiniz.

Alternatif:

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
