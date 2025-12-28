# 📘 CHANGELOG

> 이 문서는 BVE 자동 전주 설계 프로그램의 버전별 변경사항을 기록합니다.

---

## [1.0.0] - 2025-04-10
### ✨ Added
- 전주 랜덤 자동 배치 기능
- BVE CSV 파일 출력 기능 (전주, 전차선)
- 전차선 평면도 DXF 출력 기능

### ⚙ Structure
- 파라미터 기반 객체지향 구조 리팩토링 완료
- `config.json` 설정 기반 입력 처리

---

## [1.0.1] - 2025-04-15
### 🐞 Fixed`: 버그 수정
- af,fpw offset 미적용 버그수정

---

## [1.0.2] - 2025-04-16
### 🐞 Fixed`: 버그 수정
- structurelist에서 1번째 행이 누락되는 문제 수정
📦 Structure`: 내부 구조 리팩토링/변경
-create_pole 메서드에서 예외처리 추가 및 적용
(위치:  `PoleGenerator` 클래스, `CsvRwRouteParser.py`)
유틸함수  isbridgetunnel에서 예외처리 추가 및 적용 
(위치:  `util.py`)

---


## [1.0.3] - 2025-05-13
### 🐞 Fixed`: 버그 수정
- 구배 미반영 버그수정
- 전주가 좌측일때 버그수정
- 발견된 버그:
- 인덱스: 1716
위치: 89930
예외 종류: TypeError
예외 메시지: unsupported operand type(s) for *: 'NoneType' and 'float'
전체 트레이스백:
Traceback (most recent call last):
  File "C:\Users\Administrator\Documents\파이썬\AutoPOLE\core\wire.py", line 60, in create_wires
    self._set_contact_wire(
  File "C:\Users\Administrator\Documents\파이썬\AutoPOLE\core\wire.py", line 107, in _set_contact_wire
    next_offset = next_sign * 0.2
                  ~~~~~~~~~~^~~~~
TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'


---


## [1.0.4] - 2025-05-14
### 🐞 Fixed`: 버그 수정
- pole position과 pole길이 불일치
- dxf csv pole wire 독스트링및 타입힌트 강화
- 발견된 버그:
- dxf 출력시 list out of range
### 🔧 Changed
- dataloader 파라미터 전달방식 변경
- databundle클래스로 전달

---
## [1.0.5] - 2025-05-16
### 📦 Structure: 리팩토링
- structure , bvealignmnet 클래스를 생성
- 기존의 튜플, 리스트, 딕셔너리 대신 사용 코드개선
- 발견된 버그: 없음
- 미해결 버그: 
   dxf 출력시 list out of range

---
## [1.0.6] - 2025-07-17
### 📦 Structure: 리팩토링
- 디버그 모드 자동 파일 경로 설정 기능 추가
- GUI 단계 분기 구조 개선 및 사용자 편의성 향상

### 🐞 Fixed: 버그 수정
- dxf 평면도 출력시 마지막 인덱스 범위 에러 수정


## [1.0.7] - 2025-12-28
### 📦 리팩토링
- 코드 구조 리팩토링 및 TaskWizard 모듈화


---
## [예정 버전]

### [1.1.0] - (예정)
#### ✨ 추가 예정
- AJ 구간 처리 로직
- 옵션 기반 전주 종류 선택

#### 🐞 수정 예정
- 전차선 수평각 계산 정확도 향상

#### 📦 기타
- 폴더 구조 정비 및 불필요 파일 제거

---

## 형식 안내
- `✨ Added`: 새로운 기능 추가
- `🔧 Changed`: 기능 개선 또는 수정
- `🐞 Fixed`: 버그 수정
- `🧹 Removed`: 삭제된 기능
- `📦 Structure`: 내부 구조 리팩토링/변경
