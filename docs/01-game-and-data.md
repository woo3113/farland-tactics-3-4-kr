# 01. 게임 정보와 데이터 (요약)

이 문서는 실행 경로에 공통으로 필요한 **게임 데이터 구조**와, 이미 확보한 **리버싱 자산**을 정리합니다.
전체/심화 내용은 기존 작업장(`F:\DGGL\RE\docs\`)에 있습니다.

## 1. 게임 식별

| | FT3 | FT4 |
|---|---|---|
| 원제 | ファーランドオデッセイ 伝説を継ぐ者 | ファーランドオデッセイ2 君に贈るセレナーデ |
| 국내명 | 파랜드 택틱스 3 | 파랜드 택틱스 4 |
| 빌드 | 1999-09-13, MSVC, PDB `E:\fo\fo_src\Release\FO.pdb` | 2000-11-16, MSVC, PDB `D:\ft4\source\Release\FO2.pdb` |
| 실행 파일 | `FT3K.EXE`(한) / `FT3J.EXE`(일) | `FT4.EXE` |
| 등록번호 | GL9907-CR81 | 2000-FCR0495 |

공통: **PE32 / GUI**, 임포트 = `DDRAW.DLL, DINPUT.DLL, DSOUND.DLL, _INMM.DLL`

## 2. 데이터 파일

| 파일/폴더 | 내용 |
|---|---|
| `GRPDATA.PAC` / `grpdata.pac` | 그래픽 아카이브 (BMP/스프라이트) |
| `MAPDATA.PAC` / `mapdata.pac` | 맵 데이터 (맵 그래픽 + `MapEdit ` 맵 + MSA) |
| `DAT/`, `data_ud/` | 캐릭터/클래스/맵 테이블 |
| `SCR/`, `scr/` | 이벤트 스크립트 (`EV` 컨테이너) |
| `BGM/` / `bgm/` | BGM (FT3: WAV 20곡 / FT4: mp3 21곡) |
| `CVJ`,`CVK`,`WVJ`,`WVK` | 음성(일/한) · 효과음 |
| `_inmm.dll`, `_inmm.ini`, `DOOGIE\_inmmserv.exe` | CD음악 → 파일 재생 대체(BGM) |
| `_FT3_Kor_Voice.exe` / `_FT4.exe` | VB6 런처(레지스트리/음성 설정) |

## 3. 아카이브 포맷 (완전 규명)

### 3.1 PAC 컨테이너
```
'PAC_FILE\0'(9B) + u32 엔트리수 + 엔트리당 20B(name[16] + u32 (데이터절대오프셋-4)) + 데이터
  data_start(i) = value(i) + 4
  size(i)       = value(i+1) - value(i)     (마지막: fileSize - value(i) - 4)
```

### 3.2 엔트리 블록
```
'IEL1' + u32 해제크기 + 압축스트림        ← 압축
IEL1 매직 없음 → 블록 전체가 원본 파일     ← 비압축
```

### 3.3 압축 = 고전 LZSS (Okumura LZSS.c 변종)
```
ring[4096] 초기값 0x20, r = 4078
flag 바이트 1개 = 토큰 8개(LSB 우선)
  bit=1 → 리터럴 1바이트
  bit=0 → 매치: off = ((c&0xF0)<<4)|b (12비트), len = (c&0x0F)+3 (3~18)
```
- 해제기: `F:\DGGL\RE\tools\pac_decode.py` (Python), `F:\DGGL\RE\dc\lib\lzss.c` (C, Python과 MD5 일치)

### 3.4 SCR 스크립트
- 컨테이너: `"EV"`(UTF-16LE) + `u32 fileSize` + **`u32 vars[256]`** + 코드 스트림(0x408~)
- 오퍼랜드 문법: 필드 = `<tag u8><값>` (tag==0 → `vars[값]`), 문자열 = `<len u8><bytes>` (CP949)
- 대사/발화자 코퍼스: `F:\DGGL\RE\docs\SCR_text_FT3.txt`, `SCR_text_FT4.txt`

## 4. 게임/실행에 대한 사실

- CD 체크 없음 → 데이터만 있으면 실행 가능
- `_inmm`(BGM)은 **레지스트리 설정 + 별도 프로세스(`_inmmserv.exe`)** 를 쓰는 방식이라
  Wine/PotMaster 환경에서는 **동작 여부 검증 필요** → [06-troubleshooting.md](06-troubleshooting.md)
- 런처(`_FT3_Kor_Voice.exe`, `_FT4.exe`)는 VB6 스텁(MSVBVM60 필요) →
  실패하면 **본체(`FT3K.EXE`, `FT4.EXE`)를 직접 실행**하는 편이 안전

## 5. 상세 문서 위치 (기존 작업장)

| 문서 | 내용 |
|---|---|
| `F:\DGGL\RE\docs\FORMAT_PAC.md` | PAC/IEL1/LZSS 전체 스펙 + 디스어셈블 근거 |
| `F:\DGGL\RE\docs\FORMAT_SCR.md` | SCR 컨테이너/VM/오퍼랜드 문법 |
| `F:\DGGL\RE\README.md` | 리버싱 도구 인벤토리 + 재현 명령 |
| `F:\DGGL\RE\extract\` | 추출된 에셋 (FT4_grp / FT3_grp / FT4_map) |
