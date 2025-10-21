
---

# 전이 학습 (Transfer Learning)

## 1. 개념

**전이 학습(Transfer Learning)**이란
이미 **대규모 데이터셋**으로 사전 학습(pretraining)된 모델이 가진 지식을
**새로운 작업(Task)**이나 **데이터셋**에 활용하는 방법을 말합니다.

* 모델이 이미 학습한 **일반적 특징(Feature Representation)**을 기반으로 하여
  새로운 과제를 더 빠르고 효율적으로 학습할 수 있음.
* 특히 데이터가 적거나 도메인이 특수할 때 강력한 효과를 발휘함.

---

## 2. 주요 용어

### 📌 Pretrained Model (사전 학습 모델)

* 대규모 데이터셋을 기반으로 미리 학습된 모델.
* 특정 Task(예: 이미지 분류, 언어 모델링 등)를 학습했지만,
  그 과정에서 얻은 **범용적 지식**을 보유.
* 예시:

  * **비전 분야**: ImageNet 기반 ResNet, VGG, EfficientNet
  * **언어 분야**: BERT, GPT, PaLM
  * **멀티모달 분야**: CLIP, Stable Diffusion

---

### 📌 Fine-Tuning (파인튜닝)

* 전이 학습의 대표적 방법.
* Pretrained model에 새로운 Task에 맞는 데이터셋으로 **추가 학습**을 수행.
* 방식:

  * **마지막 분류기(FC Layer + Softmax)**만 새로 학습 (데이터 적을 때)
  * **뒷부분 Layer 일부 + 분류기** 학습 (데이터 중간 규모)
  * **모델 전체 End-to-End 학습** (데이터 충분할 때)

---

### 📌 Domain Adaptation (도메인 적응)

* 전이 학습의 또 다른 접근 방식.
* **A 도메인에서 학습한 모델**을
  **B 도메인 데이터**에 맞게 적응시킴.
* 핵심 목표: **데이터 분포 차이(domain shift)** 극복

  * 예시: 자연 이미지(ImageNet) → 의료 영상(CT, MRI)

---

## 3. 유사 학습 방법

| 방법                      | 설명                                | 예시                          |
| ----------------------- | --------------------------------- | --------------------------- |
| **Multi-task Learning** | 하나의 모델이 여러 Task를 동시에 학습, 공통 특징 공유 | 번역 + 문장 분류                  |
| **Zero-shot Learning**  | 학습하지 않은 새로운 클래스/Task도 처리 가능       | GPT가 처음 보는 질문에 답변           |
| **Few-shot Learning**   | 소량(1~수개)의 예시만으로 학습/추론 가능          | ChatGPT의 Few-shot Prompting |

---

## 4. 전이 학습 전략

### ✅ 도메인이 비슷할 때 (예: ImageNet → 다른 자연 이미지 분류)

#### (1) 데이터셋이 작은 경우

* 사전 학습 모델이 이미 충분한 Feature를 학습했으므로,
* **마지막 Classifier만 교체 → 학습**
* 장점:

  * 빠른 수렴
  * 과적합 방지

#### (2) 데이터셋이 큰 경우

* 사전 학습 Feature만으로 부족할 수 있음:

  * 도메인 차이 존재 (자연사진 vs 의료 CT)
  * 데이터가 많아 새로운 Feature 학습 여유가 있음
* 전략:

  * **뒷부분 Layer + Classifier** 함께 학습
  * 데이터가 매우 크면 **모델 전체 End-to-End Fine-tuning**

---

## 5. Learning Rate 전략

* Pretrained Model의 일반 지식을 망치지 않도록 **작은 Learning Rate** 사용
* 그러나 **마지막 FC Layer만 학습**하는 경우에는
  상대적으로 Learning Rate에 크게 민감하지 않음.
* 실무에서는 **Layer-wise Learning Rate Decay** 기법도 자주 사용
  (앞단 Layer는 LR 작게, 뒷단 Layer는 LR 크게)

---

## 6. 정리 (핵심 포인트)

* 전이 학습은 **“큰 데이터에서 배운 지식을 작은 데이터 문제에 적용”**하는 것.
* 데이터 크기 & 도메인 유사성에 따라 전략을 달리해야 함:

  * 데이터 적음 → 마지막 Layer만 학습
  * 데이터 많음 → 일부 Layer 또는 전체 Fine-tuning
* Learning Rate는 일반 Feature를 해치지 않게 **작게** 설정하는 것이 기본.

---


* **컴퓨터 비전**: 게임 화면 속 오브젝트 탐지 (ImageNet Pretrained CNN 활용)
* **자연어 처리**: NPC 대화 모델 (GPT 기반 Fine-tuning)
* **멀티모달**: 텍스트+이미지 기반 게임 추천 모델 (CLIP 활용)

---


