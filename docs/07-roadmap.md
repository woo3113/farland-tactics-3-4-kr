# 07. 로드맵 / 체크리스트

## 단계 0 — 준비 (완료)
- [x] 게임/데이터 식별, 실행 파일 API 확인(PE32, DDRAW/DINPUT/DSOUND, inmm)
- [x] PAC/IEL1/LZSS 포맷 규명 + 에셋 전량 추출(6,312개, 실패 0)
- [x] 안드로이드(Winlator) 실행 패키지 제작
- [x] 조작 매핑(.gptk) 초안
- [x] PortMaster 포트 패키지(스크립트 + port.json + 문서) 초안

## 단계 1 — PortMaster 실기 검증 (다음)
- [ ] 대상 기기/CFW 확정 (ROCKNIX / ArkOS / muOS / Knulli)
- [ ] **32비트 지원 여부 확인** → box86 경로 vs Hangover 경로 결정
- [ ] wine 러너 확보(`.winecellar` 또는 dev 빌드) + `wine --version` 확인
- [ ] 포트 설치 후 `log.txt` 로 첫 실행 성공 확인
- [ ] `winetricks -q ddr=opengl` 적용, 팔레트/색상 정상 확인
- [ ] 마우스 커서/클릭 동작 + `mouse_scale` 튜닝
- [ ] 저장(세이브) 위치 확인 및 `config/` bind 적용
- [ ] FT4도 동일 절차로 검증

## 단계 2 — 오디오/BGM
- [ ] 효과음/음성 정상 확인(FT3: `WVK`, FT4: `wav/`)
- [ ] `_inmm` BGM 동작 시도(레지스트리 + 작업 디렉터리)
- [ ] 실패 시 무음 진행 확정 / 대안(외부 재생) 검토

## 단계 3 — 사용성 다듬기
- [ ] 스크린샷/커버 캡처 → `screenshot.jpg`, `gameinfo.xml` 반영
- [ ] `package.ps1` 로 zip 생성 → autoinstall 폴더 설치 테스트
- [ ] 텍스트 입력(이름 입력) 대응: gptokeyb `textinput` 설정
- [ ] FT3(한/일 음성) · FT4 별도 포트 스크립트 정리

## 단계 4 — 확장(선택)
- [ ] 안드로이드 기기와 **데이터 폴더 공유** 구성(듀얼부트 시)
- [ ] SCR 디스어셈블러 마무리 → 텍스트/이벤트 분석(`F:\DGGL\RE\docs\FORMAT_SCR.md`)
- [ ] 드림캐스트 네이티브 이식 연구 계속(POC 이미 검증) → [08-reference-dreamcast.md](08-reference-dreamcast.md)

## 위험 요소 / 미지수

| 항목 | 위험 | 대응 |
|---|---|---|
| 32비트 미지원 SoC | box86 불가 → Hangover(느림) | 기기 선정 단계에서 확인 |
| BGM(inmm) | Wine에서 미동작 가능 | 무음 진행 가능(게임 진행 지장 없음) |
| 마우스 조작 | 실기 감도 편차 | `.gptk` 프리셋 2~3종 준비 |
| 게임 데이터 용량 | FT3 0.95GB / FT4 0.55GB | FT3는 일본어 음성(CVJ/WVJ 390MB) 제외 가능 |
