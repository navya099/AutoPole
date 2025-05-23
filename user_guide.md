# 🛠 프로그램 사용법 (Usage Guide)

> 본 프로그램은 BVE 노선용 전차선 및 전주 자동 배치 도구입니다.

---

## ✅ 사전 준비

1. `curve_info.txt`, `pitch_info.txt`, `bve_coordinates.txt`, `구조물.xlsx` 등 필수 입력 파일 준비  
2. 입력 파일들은 찾기 쉬운 위치에 배치 
3. Python 환경이 준비되어 있어야 하며, 패키지 설치 필요시 `requirements.txt` 참조

---

## 🚀 실행 방법

### 기본 실행

```
bash
python main.py
```
---

## ⚙️ 기능 설명

- 새 작업 버튼을 눌러서 작업 시작
종료 버튼을 눌러서 프로그램 종료

- 새 작업을 누르면 마법사가 생성되며
마법사의 안내에 따라 진행
---
__마법사 단계별 설명__

**단계1** 파일선택

>필수파일 4개를 순차적으로 선택

**단계2** 모드선택
>1. 기존 노선용 - (미개발)
#todo 랜덤 측점 생성방식이 아닌 미리 정의된 측점 파일을 입력으로 사용하여 처리
>2. 새 노선용 - 
신규 노선 배치용

**단계3** 필수값 입력

>설계속도: 노선의 설계속도

각 설계속도에 맞는전주와 브래킷이 배치됨

입력가능항목 150km/v, 250km/v , 350km/v

입력시에는 숫자만
>2. 선로갯수

단선이면 1 복선 또는 그 이상이면 갯수 입력
현재는 단선만 지원

3.선로중심간격
단선이면 0 복선이면 선로 중심간격 입력
음수도 가능
음수 입력시 현재 선로의 좌측으로 인식
양수는 현재 선로의 우측으로 인식

4. 폴방향
전주 설치방향
-1 좌측 
1 우측

단계4 작업시작
작업시작버튼을 눌러서 진행

작업 진행도중 배치가끝나면 자동으로 파일 저장 대화상자가 열리면서
전주,전차선 csv파일 을 저장할수 있음

## 단계5 작업완료
마침을 눌러 창닫기

## 📂 출력 결과

- `*.csv` : BVE용 전주 및 전차선 정보 CSV
- `*.dxf` : 전차선 평면도 DXF 도면 파일
- `log.txt` : 전주 배치 과정 로그 #todo

---

## 📌 주의사항

- 곡선 반경, 캔트, 기울기 등의 수치가 현실적이지 않으면 전차선 설치에 오류가 발생할 수 있습니다.
- 프로그램은 파일 내용을 체크하지 않으므로 입력 데이터를 반복 확인해주세요.

