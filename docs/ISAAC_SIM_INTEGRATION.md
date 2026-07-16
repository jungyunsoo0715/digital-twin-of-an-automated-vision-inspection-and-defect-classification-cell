# Isaac Sim 연동 가이드

이 문서는 시뮬레이터 독립 Python 코어를 실제 USD Stage와 연결하기 위한 작업 순서를 정의한다. Isaac Sim 버전에 따라 확장 이름과 Python API가 달라질 수 있으므로, 설치된 버전의 공식 문서를 기준으로 어댑터 구현을 확정한다.

## 1. 장면 준비

1. `cells/quality_inspection_cell.usda`를 Stage 진입점으로 연다.
2. Stage 단위를 meter, Up Axis를 Z로 유지한다.
3. `layouts/factory_layout.usda`의 프록시 Reference를 실제 컨베이어, 로봇, 카메라, 펜스 에셋 Reference로 교체한다.
4. 외부 에셋별 출처, 버전, 라이선스를 해당 `assets/*/README.md`에 기록한다.
5. 원본 에셋 수정이 필요한 경우 수정본이 아니라 override 레이어를 먼저 검토한다.

## 2. 물리와 센서

- 제품에는 Rigidbody와 단순화된 Collider를 적용한다.
- 컨베이어 표면과 제품 사이 마찰 및 속도는 `layers/physics.usda`에서 조정한다.
- 감지 센서 이벤트에는 센서 ID, 부품 ID, 시뮬레이션 시간을 포함한다.
- 검사 위치 정지 오차와 제품 간 최소 간격을 계측해 기록한다.

## 3. 로봇

- 첫 구현은 고정 Pick/Place pose와 단일 제품 형상으로 제한한다.
- FAIL 결과가 확정된 뒤에만 Pick을 허용한다.
- Pick 완료, Place 완료, 타임아웃을 각각 별도 이벤트로 코어에 전달한다.
- 오류 상태에서는 새 동작 명령을 받지 않고 Reset 전까지 정지한다.

## 4. 어댑터 계약

`src/inspection_cell/adapters/isaac_sim.py`의 `CellHardwarePort`를 구현한다.

```python
hardware.set_conveyor_speed(0.35)
hardware.stop_conveyor()
detected = hardware.read_part_sensor()
hardware.command_robot_pick(part_id="part-001")
hardware.command_robot_place(target="reject_bin")
```

코어는 SDK 객체를 직접 저장하지 않는다. Stage prim path와 실제 API 호출은 어댑터 내부에만 둔다.

## 5. 권장 Prim 경로

| 대상 | Prim path |
|---|---|
| 셀 | `/World/QualityInspectionCell` |
| 투입 컨베이어 | `/World/QualityInspectionCell/Conveyors/Infeed` |
| 배출 컨베이어 | `/World/QualityInspectionCell/Conveyors/Outfeed` |
| 로봇 | `/World/QualityInspectionCell/Robot` |
| 검사 센서 | `/World/QualityInspectionCell/Sensors/InspectionTrigger` |
| 검사 카메라 | `/World/QualityInspectionCell/Inspection/Camera` |
| 불량 박스 | `/World/QualityInspectionCell/RejectBin` |

## 6. 통합 완료 기준

- Headless 또는 GUI 실행에서 동일 seed의 판정 순서가 재현된다.
- 센서 이벤트 하나가 생산 사이클 하나만 시작한다.
- 30개 연속 처리 중 제품 중첩, 이탈, 이중 집계가 없다.
- 강제 걸림/픽업 실패 후 라인이 정지하고 Reset 뒤 다시 처리한다.
