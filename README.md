# OpenUSD 기반 산업 부품 자동 검사·불량 분류 디지털 트윈

컨베이어로 투입되는 산업 부품을 감지·검사하고, 불량품을 로봇으로 분류하는 생산 셀의 디지털 트윈 프로젝트입니다. OpenUSD 장면 구성, Isaac Sim 물리·센서·로봇 연동, 생산 KPI, 장애 재현, What-if 분석을 하나의 포트폴리오로 완성하는 것이 목표입니다.

## MVP 범위

```text
부품 생성 → 투입 컨베이어 → 감지 센서 → 비전 검사
                                      ├─ PASS → 출하 컨베이어
                                      └─ FAIL → 로봇 → 불량품 박스
```

- 컨베이어 제품 이동 및 센서 감지
- PASS/FAIL 판정과 로봇 불량품 제거
- 명시적인 생산 셀 상태 머신
- 총생산량, 정상/불량 수량, 불량률, 평균 사이클타임 KPI
- 부품 걸림과 로봇 픽업 실패 장애 및 Reset
- 컨베이어 속도별 처리량·병목 What-if 비교

실제 AI 모델 학습, 실제 PLC 연결, 다중 로봇, 공장 전체 모델링은 초기 범위에서 제외합니다.

## 빠른 시작

현재 Python 코어는 Isaac Sim 없이도 제어 로직을 검증할 수 있습니다. Python 3.10 이상을 권장합니다.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_demo.py --parts 30 --seed 42
python3 scripts/run_scenarios.py
```

패키지 설치 후에는 다음 명령도 사용할 수 있습니다.

```bash
python3 -m pip install -e .
inspection-cell-demo --parts 30
```

데모는 실제 시간을 기다리지 않고 가상 사이클타임으로 KPI를 계산합니다. Isaac Sim 연결 시 `src/inspection_cell/adapters/isaac_sim.py`의 포트에 실제 센서, 컨베이어, 로봇 제어를 연결합니다.

## 디렉터리 구조

```text
.
├── assets/                 # 외부 원본 에셋(Reference로 사용)
├── cells/                  # 셀 집계 USD
├── layouts/                # 장비 배치 USD
├── layers/                 # 물리·동작·재질·조명 레이어
├── configs/                # 기본값과 What-if 시나리오
├── data/                   # 실행 로그와 분석 결과(생성물)
├── docs/                   # 기획·요구사항·설계·일정·검증 문서
├── scripts/                # 로컬 데모와 시나리오 실행 진입점
├── src/inspection_cell/    # 시뮬레이터 독립 제어 코어
└── tests/                  # 상태 전이와 KPI 단위 테스트
```

## 문서 안내

- [프로젝트 정의](docs/PROJECT_CHARTER.md)
- [요구사항과 완료 기준](docs/REQUIREMENTS.md)
- [시스템·OpenUSD 아키텍처](docs/ARCHITECTURE.md)
- [Isaac Sim 연동 가이드](docs/ISAAC_SIM_INTEGRATION.md)
- [5주 구현 로드맵](docs/ROADMAP.md)
- [시험 및 검증 계획](docs/TEST_PLAN.md)

## 핵심 설계 원칙

- 외부 에셋 원본은 수정하지 않고 USD Reference로 조립합니다.
- 배치, 물리, 동작, 재질, 조명을 레이어로 분리합니다.
- 도메인 로직은 Isaac Sim API와 분리해 빠르게 단위 테스트합니다.
- 모든 장애는 재현 가능한 설정과 로그를 갖게 합니다.
- 성능 비교에서는 속도뿐 아니라 로봇·검사 병목과 장애율을 함께 봅니다.

## 참고 자료

- [Isaac Sim Pick-and-Place 예제](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/robot_setup_tutorials/tutorial_pickplace_example.html)
- [OpenUSD 기반 디지털 트윈 개요](https://docs.omniverse.nvidia.com/vfi/latest/guide/open-usd.html)
- [NVIDIA Digital Twin Scene Assembly](https://docs.nvidia.com/learning/physical-ai/assembling-digital-twins/latest/getting-started/overview.html)
