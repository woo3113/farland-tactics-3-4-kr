# 08. 참고: 드림캐스트 네이티브 이식 (연구)

PortMaster/Wine 경로와 별개로, **원본 데이터를 읽는 네이티브 엔진**을 드림캐스트(KallistiOS)에
올리는 연구를 진행했습니다. 목표는 "안드로이드 기기에서 Flycast로 실행"까지 포함합니다.

## 1. 왜 드림캐스트인가
- 런타임이 Win9x와 유사(단일 스레드, 고정 하드웨어, OS 없음) → DirectDraw/DirectInput/DirectSound 대응 구현이 단순
- 코퍼스: 이 PC에 툴체인(`kallistios/dc-kos-toolchain`, sh-elf-gcc 14.2)과 **Flycast**가 이미 있음
- 결과물이 GD-ROM 이미지(.cdi) → **안드로이드 Flycast**로 바로 실행 가능

## 2. 검증된 POC (실측 완료)

| POC | 내용 | 산출물 |
|---|---|---|
| POC-A | KOS 빌드 → selfboot CDI → Flycast 부팅 | `F:\DGGL\RE\dc\poc1\poc1.{elf,cdi}` |
| POC-B | **실제 게임 8bpp 팔레트 PVR 텍스처 + 컬러키 투명 + BGM(22050Hz 스테레오)** | `F:\DGGL\RE\dc\poc2\poc2.{elf,cdi}` |

- 파이프라인: PAC → LZSS 해제 → BMP(8bpp) → `.tex/.pal` → `pvr_txr_load_ex(PVR_TXRLOAD_8BPP)` → PVR
- 해제기 C 코드: `F:\DGGL\RE\dc\lib\lzss.c` (Python 구현과 MD5 일치)
- 빌드: `docker run --rm -v F:/DGGL/RE/dc:/src -w /src kallistios/dc-kos-toolchain bash /src/build_poc2.sh`

## 3. 남은 난관 (정직한 평가)

| 항목 | 상태 |
|---|---|
| 에셋 파이프라인(BMP→PVR) | ✅ 검증 |
| 사운드(BGM/효과음) | ✅ BGM 재생 검증 / 스트리밍·CDDA는 미구현 |
| **MSA 스프라이트(애니메이션)** | ⬜ 포맷 미규명(프레임 테이블 구조) |
| **SCR 스크립트 VM** | 🔶 85% (오퍼랜드 디스크립터 마무리 필요) |
| 전투/AI 규칙 | ⬜ exe 내부 네이티브 코드 → 장기 리버싱 |

→ 즉 **"에셋과 런타임"은 되고, "게임 규칙"이 남았습니다.** 그래서 현실적 정답은 Wine(경로 A/B)입니다.

## 4. 관련 자료 위치
- 리버싱 작업장: `F:\DGGL\RE\README.md`
- 포맷: `F:\DGGL\RE\docs\FORMAT_PAC.md`, `FORMAT_SCR.md`
- POC 소스: `F:\DGGL\RE\dc\poc1`, `poc2`
- 추출 에셋: `F:\DGGL\RE\extract\`
