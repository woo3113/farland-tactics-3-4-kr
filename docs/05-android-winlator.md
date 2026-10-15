# 05. 안드로이드 병행 경로 (Winlator)

PortMaster는 안드로이드에서 동작하지 않습니다. 안드로이드 게임기를 **그대로 쓰면서** 이 게임을 하려면
**Winlator(Wine + Box64/FEX)** 를 사용합니다. 이 경로는 이미 패키지가 만들어져 있습니다.

## 1. 이미 준비된 산출물

| 파일 | 크기 | 내용 |
|---|---|---|
| `F:\DGGL\Export\파랜드택틱스3(K)_Winlator.zip` | 약 349 MB | 게임 + dgVoodoo2 + reg + 가이드 (한국어 음성만) |
| `F:\DGGL\Export\파랜드택틱스4(K)_Winlator.zip` | 약 354 MB | 게임 + dgVoodoo2 + reg + 가이드 |

각 zip 안에는 `_안드로이드_실행가이드.txt` 가 포함되어 있습니다.

## 2. 요약 절차

1. zip을 기기로 옮겨 **ZArchiver** 등으로 압축 해제
2. **Winlator 11.x 이상**(또는 Winlator CMOD/Bionic) 설치
   - Snapdragon + Adreno → 그래픽 드라이버 **Turnip**
   - Box64 프리셋 **Performance**, Windows 버전 10
   - 화면 640×480, Virtual Desktop 켜기, 종횡비 유지
3. 컨테이너의 `D:` 에 게임 폴더 연결(경로는 `D:\FT3` 처럼 짧게)
4. 실행: `_FT3_Kor_Voice.exe` (안 되면 `FT3K.EXE` 직접), **작업 디렉터리를 게임 폴더로 지정**
5. 색상 깨짐 → `_Winlator\dgVoodoo2\` 의 `ddraw.dll`,`D3DImm.dll`,`dgVoodoo.conf` 를 게임 루트에 복사
6. 무음(BGM) → `DOOGIE\_inmm.reg` 를 regedit로 등록(자세한 내용은 zip 내 가이드)

## 3. PortMaster 경로와의 관계

| | PortMaster(Wine) | Android(Winlator) |
|---|---|---|
| 실행 환경 | 리눅스 CFW (ROCKNIX/ArkOS/muOS) | 안드로이드 앱 |
| 번역 계층 | box86/hangover + wine | Box64/FEX + Wine |
| 조작 | gptokeyb(마우스 매핑) | Winlator 터치 오버레이 / BT 마우스 |
| 설치 난이도 | CFW 설치 필요(듀얼부트 가능) | 앱 설치만 |
| 디버깅 | `log.txt` / ssh | Winlator 로그, adb |

**결론**: 두 경로 모두 "Wine으로 감싼다"는 본질은 같고, **게임 데이터와 무음(BGM) 대응이 동일한 이슈**를 공유합니다.
PortMaster 문서의 06(문제 해결) 항목이 안드로이드에도 그대로 적용됩니다.

## 4. 기기 이원화 팁

- 안드로이드 기기가 **ROCKNIX를 지원**한다면(예: 일부 Snapdragon 기기, RP5/Mini 계열 dev 빌드)
  → SD카드 듀얼부트로 **안드로이드(평상시) + ROCKNIX(PortMaster)** 를 함께 쓸 수 있습니다.
- 이 경우 게임 데이터는 **같은 폴더를 공유**하도록 배치하면 중복 저장을 피할 수 있습니다.
