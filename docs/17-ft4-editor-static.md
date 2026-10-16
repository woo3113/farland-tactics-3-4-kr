# 17. FT4 에디터 (완전 정적 분석 — 캡처 불필요)

FT4는 원작이 **세이브 에디터가 아니라 마스터데이터 에디터**를 동봉했습니다.
그 에디터의 **정의 파일(CFG)에 필드 테이블 전체가 평문으로 들어 있어**, DOSBox·화면캡처 없이
정적 분석만으로 에디터를 완성할 수 있었습니다.

---

## 1. 툴 정체 (FT4 CFG 헤더에 박혀 있음)

```
Game Editer Make Tool (C)Oh-sutaeck, Inc.
```
| 게임 | 에디터 EXE | 대상 파일 | 제작자 |
|---|---|---|---|
| FT3 | `EDITER.EXE` | 세이브 `ODDATA*.FOS` | (00년대 초 툴 사용) |
| FT4 | `ITEMEDIT.EXE` | `ITEM.CFG` (아이템 99) | **나정환** (najw@nownuri.net) |
| FT4 | `STATEDIT.EXE` | `STAT.CFG` (스탯 99) | **한빛공자(서광욱)** [GO TOKDO] |

- 두 EXE 모두 **PKLITE 1.12** → depklite 로 해제 시 114,283 bytes (동일 크기 = 같은 툴/런타임)
- CFG 문자열은 **조합형(Johab)** 인코딩 ⚠️ (FT3 는 CP949 — 세대 차이)
  ```python
  open("ITEM.CFG","rb").read().decode("johab")   # → 한글 정상 표시
  ```

## 2. CFG = 에디터의 정의 파일 (필드 테이블 원문)

형식 (CRLF 구분, 항목당 4줄):
```
<이름>
<세이브 내 오프셋>
<최대값>
<기본값>
```
헤더 예 (ITEM.CFG):
```
Game Editer Make Tool (C)Oh-sutaeck, Inc.
파랜드 택틱스 아이템 에디터
나정환 (najw@nownuri.net)
화일이 없넹...- -;
fo2sv_00.fos … fo2sv_09.fos      ← 편집 대상 파일 목록
돈 / 8225 / 999999999 / 0
E-쥬얼 / 8373 / 999 / 0
…
```
→ 이걸 그대로 읽으면 **이름·오프셋·최대값**이 전부 나옵니다 (파싱 결과: ITEM.CFG 99개, STAT.CFG 99개).

## 3. FT4 세이브(`fo2sv_*.fos`, 704,396 bytes) 주요 오프셋

| 항목 | 오프셋 | 크기 | 비고 |
|---|---|---|---|
| 돈 | `0x2021` (8225) | 4 | 최대 999999999 |
| E-쥬얼 | `0x20B5` (8373) | 2 | |
| 요정의 구슬 | `0x20B9` (8377) | 2 | 4바이트 간격으로 아이템들 |
| 유니 HP | `0x049D` (1181) | 2 | |
| 유니 MP | `0x04A9` (1193) | 2 | |
| 유니 SP | `0x04B5` (1205) | 2 | |
| 실버 HP | `0x06E9` (1769) | 2 | 캐릭터별 588 간격 |

(전체 목록: `ITEM.CFG` 99개 + `STAT.CFG` 99개 → 에디터에 자동 삽입)

## 4. 재현 절차 (다른 게임에 그대로)

```powershell
# 1) 에디터 EXE 압축 해제
python pkla.py -p ITEMEDIT.EXE        # -> PKLITE 1.12, cmpr @784
./depklite -o itemedit.bin ITEMEDIT.EXE 784
# 2) 에디터가 함께 배포한 정의 파일(.CFG/.DAT) 찾기
#    → 여기에 이름/오프셋/최대값이 평문(CP949 또는 Johab)으로 들어 있는 경우가 많음
# 3) 문자열 인코딩 확인 (CP949 실패하면 johab 시도)
# 4) 정의 파일이 없으면: 합성 세이브(각 u16 = 오프셋/2) + 메뉴 순회로 역산 (FT3 방식)
# 5) 에디터 HTML 은 동일 파일(editor/fos-editor.html)을 확장
```

## 5. 현재 `editor/fos-editor.html` 지원 범위

| 대상 | 섹션 |
|---|---|
| FT3 세이브 (`ODDATA*.FOS`, 21,704B) | 소지금·코인 / 캐릭터 8명 HP·HP-MAX·SP·SP-MAX·경험치 / **직업 스탯 6슬롯×8명** (CLSSCHNG.DAT 순서) |
| FT4 세이브 (`fo2sv_*.fos`, 704,396B) | 소지금(0x2021) / **아이템 99** / **스탯 99** (CFG 정의 그대로) |
공통: 값 찾아서 바꾸기(1·2·4바이트), 되돌리기, 원본 파일명 유지 저장
