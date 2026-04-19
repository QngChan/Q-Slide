# AGENTS.md

## Start-of-task checklist
Yeni bir goreve baslamadan once su dosyalari oku:

1. `AGENT_CONTEXT.md`
2. `ARCHITECTURE.md`
3. `CHANGELOG.md`
4. `NEXT_STEPS.md`

## Update rule (mandatory)
Eger kod davranisi, mimari, kurulum veya plan degistiyse ayni degisiklikte su dosyalari da guncelle:

- `AGENT_CONTEXT.md`
- `ARCHITECTURE.md`
- `CHANGELOG.md`
- `NEXT_STEPS.md`

## Project intent
- Host: masaustu uygulamasi
- Viewer: sadece web
- Ana akıs: Host -> FastAPI API -> WebSocket -> Viewer

## Response format
- Teknik karar verilen her cevapta kisa iki baslik zorunludur:
  - `Secilen Yol`
  - `Alternatifler`
