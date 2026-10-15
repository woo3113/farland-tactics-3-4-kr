# 11. Winlator 기기 세팅 실측 절차 (Retroid Pocket Classic)

실제 기기에 적용해 검증한 절차입니다. ADB만으로 대부분 자동화됩니다.

## 1. 대상 기기 (실측)

| 항목 | 값 |
|---|---|
| 모델 | Retroid Pocket Classic (`parrot`) |
| SoC | **SM4450** (Snapdragon 4 Gen 2 계열 / RP클래식 명칭 G1 Gen 2) |
| ABI | `arm64-v8a, armeabi-v7a` (32비트 ARM 지원 O) |
| Android | 14 (SDK 34) |
| RAM | 5.6GB (6GB 모델) |
| GPU | Adreno A12 (OpenGL ES 3.2) |
| 저장공간 | 내부 101GB / SD 238GB |
| **리눅스 CFW** | **미지원 → PortMaster 불가**, Winlator 경로 사용 |

> 아날로그 스틱이 없으므로 **터치스크린이 마우스 역할**을 합니다(마우스 게임이라 유리).

## 2. 준비물 (PC)

- `adb` : `C:\Users\woo31\Android\Sdk\platform-tools\adb.exe`
- 게임 zip (기기용 ASCII 경로): `tools/make_device_zip.py` 로 생성
  ```
  python tools/make_device_zip.py "F:\DGGL\Export\파랜드택틱스3(K)" "F:\DGGL\Export\FT3(K)_Winlator.zip" "FT3(K)"
  ```
- Winlator APK: `brunodev85/winlator` 최신 릴리스 (이번엔 v11.2, 150MB)

## 3. 자동 세팅 순서 (검증됨)

```powershell
$adb = "C:\Users\woo31\Android\Sdk\platform-tools\adb.exe"

# (1) 기기 확인/사양
& $adb devices -l
& $adb shell getprop ro.product.model
& $adb shell getprop ro.board.platform

# (2) 저장소 준비
& $adb shell "mkdir -p /storage/emulated/0/Winlator"

# (3) 게임 zip 푸시 (실측 30MB/s)
& $adb push "F:\DGGL\Export\FT3(K)_Winlator.zip" "/storage/emulated/0/Winlator/"
& $adb push "F:\DGGL\Export\FT4(K)_Winlator.zip" "/storage/emulated/0/Winlator/"

# (4) 기기에서 직접 압축 해제 (/system/bin/unzip)
& $adb shell "cd /storage/emulated/0/Winlator && unzip -o -q 'FT3(K)_Winlator.zip' && unzip -o -q 'FT4(K)_Winlator.zip'"

# (5) Winlator 설치
& $adb install -r "C:\...\Winlator_11.2.apk"

# (6) 앱을 한 번 실행해 컨테이너를 만들고(앱 UI), 그 다음 아래로 설정 패치
```

## 4. 컨테이너 설정 (앱에서 1개 생성 후, ADB로 교정)

컨테이너 파일 위치 (Winlator 11.x):
```
/data/data/com.winlator/files/rootfs/home/xuser-<id>/.container   ← 컨테이너 설정(JSON)
/data/data/com.winlator/files/rootfs/home/xuser-<id>/.startmenu   ← 바로가기(JSON)
/data/data/com.winlator/files/rootfs/home/xuser-<id>/.wine/       ← Wine 프리픽스
```
- 앱 APK(릴리스)는 `run-as` 로 접근 가능 → **ADB로 직접 읽고/수정 가능**
- `adb pull/push` 는 앱 영역을 직접 못 쓰므로 `run-as cp` 사용

```powershell
$H = "/data/data/com.winlator/files/rootfs/home/xuser-1"

# 설정 읽기 (raw 리다이렉트는 cmd 로!)
cmd /c "`"$adb`" exec-out run-as com.winlator cat $H/.container > container.json"

# (로컬에서 JSON 수정: tools/patch_winlator.py / fix_container_drives.py)

# 반영
& $adb push container_v2.json /data/local/tmp/
& $adb shell "run-as com.winlator cp /data/local/tmp/container_v2.json $H/.container"
```

### 적용한 값 (검증됨)
| 항목 | 값 | 이유 |
|---|---|---|
| `screenSize` | `640x480` | 원작 해상도 |
| `graphicsDriver` | `turnip,gladio` | Adreno |
| `dxwrapper` | `wined3d` | **DirectDraw 2D → wine 내장 ddraw** (DXVK 불필요) |
| `box64Preset` | `PERFORMANCE` | 속도 |
| `startupSelection` | `0` (Normal) | 오디오/서비스 호환 |
| `drives` | **`D:/storage/emulated/0/Winlator`** (단일) | 파싱 모호성 제거 |
| WoW64 | 기본 ON | **32비트 PE 실행의 핵심** |

> ⚠️ drives 문자열은 `<문자>:<경로>` 를 구분자 없이 이어붙이는 형식이라
> 여러 개일 때 파싱이 모호합니다 → **단일 드라이브 권장**.

### 심볼릭 링크 직접 교정 (즉시 반영용)
Wine이 실제로 쓰는 이름은 **`d:`(콜론 포함)** 입니다. 컨테이너 실행 시 앱이 재생성하지만,
즉시 적용하려면:
```powershell
& $adb shell "am force-stop com.winlator"
& $adb shell "run-as com.winlator sh -c 'cd $H/.wine/dosdevices && rm -f d: && ln -s /storage/emulated/0/Winlator d:'"
# 검증 (앱 uid 로 읽히면 OK)
& $adb shell "run-as com.winlator ls $H/.wine/dosdevices/d:/"
```

### 바로가기 추가 (`.startmenu`)
```json
{"name":"파랜드 택틱스","children":[
  {"name":"파랜드 택틱스 3","path":"D:/FT3(K)/FT3K.EXE"},
  {"name":"파랜드 택틱스 4","path":"D:/FT4(K)/FT4.EXE"}]}
```
- Winlator의 Shortcuts 탭/컨테이너 시작메뉴에 표시됩니다.

## 5. 실행

1. Winlator → Containers → 컨테이너 선택 → **Explorer** → `D:` → `FT3(K)` → **`FT3K.EXE`**
2. 바로가기가 보이면 그걸 탭 (동일)
3. 첫 실행은 초기화 때문에 다소 걸릴 수 있음

## 5.1 레지스트리 주입 (필수) — "레지스트리에 등록되어 있지 않습니다" 오류

이 게임들은 **레지스트리 키 존재를 확인**합니다. Wine 프리픽스에 없으면 실행이 거부됩니다.

| 프로그램 | 확인하는 키 (실측: exe/dll 문자열) |
|---|---|
| `FT3K.EXE` | `HKCU\Software\TGL\FO` |
| `FT4.EXE` | `HKCU\Software\TGL\FO2` |
| `_inmm.dll` | `HKCU\Software\irori\_inmm.dll` (+ `\Player`, INMM v2.38 확인) |

게임 폴더의 `DOOGIE\*.reg` 를 **Wine 레지스트리(user.reg)로 변환해 주입**한다.

```powershell
$H = "/data/data/com.winlator/files/rootfs/home/xuser-1"
# 0) 컨테이너 정지 (Wine이 레지스트리를 덮어쓰지 않도록)
& $adb shell "am force-stop com.winlator"

# 1) user.reg + .reg 파일 회수  (raw 리다이렉트는 cmd 로!)
cmd /c "`"$adb`" exec-out run-as com.winlator cat $H/.wine/user.reg > user.reg"
& $adb pull "/storage/emulated/0/Winlator/FT3(K)/DOOGIE/_inmm.reg" .
& $adb pull "/storage/emulated/0/Winlator/FT3(K)/DOOGIE/FT3.reg" .
& $adb pull "/storage/emulated/0/Winlator/FT4(K)/DOOGIE/_inmm.reg" .
& $adb pull "/storage/emulated/0/Winlator/FT4(K)/DOOGIE/_FT4.reg" .

# 2) 병합  (tools/reg2wine.py : Windows .reg → Wine user.reg 형식, 중복 섹션 제거)
python tools/reg2wine.py user.reg user_new.reg FT3_inmm.reg FT3_FT3.reg FT4_inmm.reg FT4_FT4.reg

# 3) 반영 (백업 후)
& $adb shell "run-as com.winlator cp $H/.wine/user.reg $H/.wine/user.reg.bak"
& $adb push user_new.reg /data/local/tmp/
& $adb shell "run-as com.winlator cp /data/local/tmp/user_new.reg $H/.wine/user.reg"

# 4) 확인
& $adb shell "run-as com.winlator grep -c irori $H/.wine/user.reg"   # 5 이상
```

- 컨테이너를 **새로 만들면 프리픽스가 새로 생기므로**(`xuser-2` …) 그 컨테이너에도 같은 주입이 필요하다.
- 다른 컨테이너에 적용할 때는 `$H` 의 `xuser-N` 만 바꾸면 된다.

## 6. 알려진 이슈 / 대응

| 증상 | 대응 |
|---|---|
| **"레지스트리에 등록되어 있지 않습니다"** | 5.1 레지스트리 주입 (가장 흔함) |
| 색상/팔레트 깨짐 | `FT3(K)\_Winlator\dgVoodoo2\` 의 3개 파일을 `FT3(K)\` 루트로 복사 |
| 소리 없음 | 컨테이너 `startupSelection=0`(Normal) 확인, 재실행 |
| BGM만 없음 | 정상적 실패 모드(무음 진행 가능) |
| 커서 조작 | 터치 = 마우스, 더블클릭은 두 번 탭 |
| 게임이 안 뜸 | Winlator 로그 확인, exe 경로(D:\FT3(K)\FT3K.EXE) 재확인 |

## 7. 참고: 기기 zip 만들기 (한글 파일명 문제 회피)

기기의 `/system/bin/unzip` 은 한글 파일명을 깨뜨릴 수 있어 **zip 내부 경로를 ASCII로** 만듭니다.
```
python tools/make_device_zip.py <원본폴더> <출력zip> <내부루트명>
```
- 한글 파일명은 자동으로 ASCII 로 변환(내용 유지), `_안드로이드_실행가이드.txt` → `_READ_ME_KR.txt`
