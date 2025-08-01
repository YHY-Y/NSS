# YOLO 기반 객체 탐지 파이프라인
*YOLO-based Object Detection Pipeline*

## 프로젝트 개요 (Overview)
이 소프트웨어는 YOLO 기반 객체 탐지 모델의 학습, 성능 평가, 데이터 증강을 위한 전체 파이프라인을 포함합니다.

##  코드 설명
### 📁 `data_augmentation/` – 데이터 증강 스크립트
YOLO 학습을 위한 데이터 다양성 확보 목적으로 사용되며, 다양한 변형 기법을 이미지에 적용합니다.

**color.py**
→ HSV 색상 변환을 통해 이미지의 색조(Hue), 채도(Saturation), 명도(Value)를 조절합니다.
(예: hue+15, sat+40, val+25)

**gaussian_noise.py**
→ 정규분포 기반의 가우시안 노이즈를 이미지에 추가하여 센서 노이즈나 조명 문제를 시뮬레이션합니다.

**salt_paper.py**
→ 무작위 픽셀을 흰색(255) 또는 검정색(0)으로 설정하는 Salt & Pepper 노이즈를 추가합니다.

**blur.py**
→ (7x7) 커널, σ=2 설정으로 강한 가우시안 블러를 적용하여 초점 흐림 환경을 구현합니다.

---

### 📁 `evaluation/` – 추론 결과 및 성능 평가
실험 후 모델의 성능을 정량적으로 분석하고, 시각화 및 평가 로그를 생성합니다.

**test.py**
→ YOLO 모델을 사용하여 AVI 영상의 각 프레임에서 객체 탐지를 수행하며,
바운딩 박스를 그린 결과를 영상(.avi)과 **텍스트 로그(.txt)**로 저장합니다.
(로그 포맷: frame_xxxxxx, cls conf x1 y1 x2 y2)

**fps.py**
→ 지정된 폴더 내 모든 영상에 대해 추론을 수행하고, 영상별 및 평균 FPS(초당 프레임 수),
**Latency(프레임당 처리 시간)**를 계산하여 로그 파일로 저장합니다.

**result.py**
→ test.py의 추론 로그와 CVAT 형식의 GT XML을 비교하여
Precision, Recall, F1 score, mean IoU, mAP@0.5 등의 성능 지표를 산출하고
CSV로 저장합니다.
또한 모델별 평균 성능을 요약한 modelwise_summary.csv 파일도 자동 생성됩니다.

---

### 📁 `training/` – YOLO 모델 학습 스크립트
YOLOv10 기반의 객체 탐지 모델을 학습하는 설정 및 실행 스크립트를 포함합니다.

**train.py**
→ ultralytics 라이브러리의 YOLO 모델을 불러와, 지정된 data.yaml 설정에 따라 학습을 진행합니다.
학습 epoch, batch size, 이미지 크기, AMP 설정 등을 사용자 정의할 수 있습니다.

**data.yaml**
→ 학습 및 검증 이미지 경로, 클래스 수(nc), 클래스 이름(names)을 지정하는 설정 파일입니다.


##  환경 세팅 및 설치
이 프로젝트는 [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) 저장소 기반으로 YOLO 모델 학습 및 추론을 진행합니다.
YOLOv8~11 버전이 포함된 공식 라이브러리 설치 후 실행하면 됩니다.
```bash
pip install ultralytics
```


##  실행 방법 (Usage)

```bash
# 1) 데이터 증강 (예: HSV 색상 증강)
python data_augmentation/color.py

# 2) 모델 학습
python training/train.py

# 3) 추론 및 시각화
python evaluation/test.py

# 4) 성능 측정 (FPS)
python evaluation/fps.py

# 5) 정량 평가 및 요약
python evaluation/result.py
```


##  참고 사항
GT 파일은 CVAT XML 형식을 기반으로 평가됩니다.
이미지 경로 구조는 train/noise, val/noise 기준으로 고정되어 있어야 합니다.
추론 결과는 log, output 디렉토리에 자동 저장됩니다.
