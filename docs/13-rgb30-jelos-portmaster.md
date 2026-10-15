# 13. RGB30(JELOS) PortMaster-wine 시도 기록

Powkiddy RGB30 (Rockchip RK3566, aarch64) 에서 파랜드 택틱스 3/4 를 **PortMaster 방식(wine)** 으로
돌리기 위한 실측 기록입니다. **결론: 이 카드의 JELOS 20231003 에는 디스플레이 서버가 없어 실행 불가.**
준비물(wine/프리픽스/포트/데이터)은 모두 만들어 두었으므로 **ROCKNIX 등으로 CFW 만 바꾸면 그대로 사용 가능**합니다.

---

## 1. 기기/CFW 실측

| 항목 | 값 |
|---|---|
| 기기 | Powkiddy RGB30 (정사각 720x720) |
| SoC | Rockchip **RK3566** (Cortex-A55 x4) / aarch64 |
| CFW | **JELOS 20231003** (2023-10-03, 마지막 지원 세대) |
| 부트 | `/dev/sdX3` = FAT32 `JELOS` (KERNEL, SYSTEM(squashfs), dtb들) |
| 데이터 | `/dev/sdX4` = ext4 `STORAGE` → `/roms` (JELOS 병합 저장) |
| box86/box64 | `/usr/bin/box86`, **`/usr/bin/box64` 있음** (2023-10 빌드) |
| gptokeyb | `/usr/bin/gptokeyb` 있음 |
| `/usr/lib32` | 있음 (gl4es 등 32비트 ARM) |
| PortMaster | `/roms/ports/PortMaster` (2023-10 구버전, `tasksetter` 없음) |
| **wine** | **없음** (직접 준비) |
| **디스플레이 서버** | **없음** ← 결정적 제약 |

### 디스플레이 서버 확인 결과 (SYSTEM squashfs 전수 검색)
```
Xwayland : 없음    Xorg : 없음    Xvfb : 없음
weston   : 없음    sway : 없음    cage : 없음    labwc : 없음
(X11 라이브러리는 일부 존재: libX11.so, libxcb, libEGL …)
UI 는 KMS/DRM + EmulationStation 직결 → X/Wayland 세션이 없음
```
wine 은 X11 또는 Wayland 로만 출력하므로 **JELOS 에서는 wine 게임 실행이 구조적으로 불가**합니다.

---

## 2. SD 카드 접근 방법 (PC에서 ext4 직접 읽고 쓰기)

Windows 탐색기로는 JELOS 의 ext4 `STORAGE` 파티션을 읽을 수 없습니다. 아래 조합으로 해결했습니다.

```powershell
# (1) WSL 기동 후 USB 카드리더를 WSL 에 넘김 (usbipd-win, 관리자 1회 필요)
wsl -d Ubuntu -u root -e true
usbipd attach -w Ubuntu -b 14-4         # 14-4 = Genesys Logic USB3.0 Card Reader

# (2) WSL 안에서 마운트 (라벨 사용 → 장치명 변화에 견고)
wsl -d Ubuntu -u root -e bash -c "mkdir -p /mnt/rgb30 && mount -L STORAGE /mnt/rgb30"
```
> ⚠️ **WSL 은 명령마다 인스턴스가 죽으면 마운트/attach 가 풀립니다.**
> → (a) `wsl -d Ubuntu -u root -e sleep 1000000` 을 백그라운드로 띄워 유지하거나,
> → (b) 모든 스크립트 첫머리에서 `findmnt || mount -L STORAGE` 로 재마운트.
> ⚠️ 이때 WSL `--mount \\.\PHYSICALDRIVEn` 방식은 이 USB 리더에서 `ERROR_INVALID_DRIVE` 로 실패합니다.

---

## 3. 준비한 산출물 (카드에 이미 반영됨)

```
/roms/windows/.winecellar/
  ├─ wine-11.19-amd64-wow64/          # Kron4ek wine 11.19 (wow64) — 734MB (include 삭제)
  └─ prefix-farland/                  # 79MB  ← system32/syswow64 를 빌드로 심볼릭 링크해 613MB→79MB
        user.reg  ← TGL\FO, TGL\FO2, irori\_inmm.dll(+Player) 주입 완료

/roms/ports/Farland Tactics 3.sh      # box64 + wine 런처 (실행권한)
/roms/ports/Farland Tactics 4.sh
/roms/ports/farlandtactics3/
  ├─ farlandtactics3.gptk             # RGB30(스틱): 왼쪽 스틱=마우스, A/L1=좌클릭
  └─ data/                            # 게임 본체 592MB + dgVoodoo2(ddraw.dll 등)
/roms/ports/farlandtactics4/          # 417MB
```

- **wine 빌드**: `Kron4ek/Wine-Builds` 의 `wine-11.19-amd64-wow64` (94.7MB 압축 / 801MB 해제)
  — aarch64 에서 32비트 PE 게임을 돌리는 정석 조합이 `box64 + wine(amd64, wow64)` 입니다.
- **프리픽스**: PC(x86_64)에서 미리 만들어 카드에 넣었습니다(기기 첫 실행 시간 절약).
  `drive_c/windows/system32`, `syswow64` 의 DLL 을 빌드 폴더로 **상대 심볼릭 링크**로 바꿔 613MB→79MB.
- **레지스트리**: `tools/reg2wine.py` 로 게임 폴더의 `DOOGIE/*.reg` 를 프리픽스 `user.reg` 에 병합
  (`irori` 3건, `TGL` 2건 확인).

---

## 4. 검증한 것 / 검증 못 한 것

| 항목 | 결과 |
|---|---|
| wine + 프리픽스 + 레지스트리로 게임 실행 | ✅ **PC(WSLg X11)에서 45초간 정상 실행** — X 창 생성, 레지스트리 오류 없음 |
| box64 로 wine 구동 | ❌ 미검증 (디스플레이 서버가 없어 기기에서 시도 불가) |
| RK3566 성능(A55x4) | ❌ 미검증 |

즉 **게임/wine 설정 자체는 유효**하고, 막는 것은 오직 CFW 의 디스플레이 서버 부재입니다.

---

## 5. 다음 단계 (택1)

### (A) ROCKNIX 로 전환 — 권장
- RGB30 정식 지원, 유지보수 활발, **weston/Xwayland + box64 + PortMaster wine 지원**.
- **새 microSD(16~32GB)** 에 ROCKNIX 를 굽고, 현재 128GB 카드는 게임 카드로 계속 사용.
- 위 3절의 `windows/.winecellar`(wine+프리픽스)와 `ports/farlandtactics*` 를 그대로 복사하면 됩니다.
  (ROCKNIX 의 PortMaster 는 최신 버전이므로 런처의 `$directory` 경로만 자연스럽게 맞습니다.)

### (B) weston(웨이랜드) 번들 시도 — 실험적
- ROCKNIX 이미지에서 `weston` + 의존 라이브러리를 추출해 JELOS 에 넣고,
  wine 11 의 **네이티브 Wayland 드라이버**(Xwayland 불필요)로 출력.
- 성공 시 기존 카드 그대로 사용 가능하지만 **glibc/ABI mismatch 리스크**가 큽니다.

### (C) 보류
- 안드로이드(Winlator) 쪽은 이미 동작하므로 리눅스는 나중에.

---

## 6. 참고: 최신 PortMaster 설치 위치

| CFW | 포트 폴더 | 런타임(libs) |
|---|---|---|
| ROCKNIX | `/roms/ports/` | `/roms/ports/PortMaster/libs/` |
| JELOS | `/roms/ports/` | 〃 |
| ArkOS | `/roms/tools/` | `/roms/tools/PortMaster/libs/` |
| muOS | `/mnt/mmc/ROMS/Ports/` | `/MUOS/PortMaster/libs/` |
| Knulli | `/userdata/roms/ports` | `/userdata/system/.local/share/PortMaster/libs` |
