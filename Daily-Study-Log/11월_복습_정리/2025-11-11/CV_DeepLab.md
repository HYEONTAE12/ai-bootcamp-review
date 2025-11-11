

---

## 🧠 DeepLab 요약 정리

### 1️⃣ 개요

DeepLab은 **세그멘테이션(Semantic Segmentation)** 모델로,
기존 FCN·U-Net이 겪던 “해상도 손실 문제”를 해결하기 위해 만들어졌어요.
핵심은 **해상도를 유지하면서도 넓은 문맥 정보를 얻는 것**입니다.

---

### 2️⃣ 핵심 구성 요소

| 구성 요소                                     | 역할          | 설명                                                            |
| ----------------------------------------- | ----------- | ------------------------------------------------------------- |
| **Dilated (Atrous) Convolution**          | 해상도 유지      | Pooling 없이 커널 간격을 띄워 넓은 Receptive Field 확보                    |
| **ASPP (Atrous Spatial Pyramid Pooling)** | 멀티스케일 문맥 이해 | 여러 dilation rate(예: 1, 6, 12, 18)를 병렬로 적용하여 다양한 크기의 객체를 인식    |
| **Decoder (v3+ 추가)**                      | 경계 복원       | 저해상도 feature(semantic) + 고해상도 feature(spatial)를 결합해 세밀한 경계 복원 |
| **CRF (v1~v2)**                           | 경계 정교화      | 픽셀 간 유사도 기반으로 경계선을 매끄럽게 보정                                    |

---

### 3️⃣ 버전별 발전 과정

| 버전              | 주요 특징                                    |
| --------------- | ---------------------------------------- |
| **DeepLab v1**  | Atrous Conv + CRF 결합                     |
| **DeepLab v2**  | ASPP 추가로 멀티스케일 인식 강화                     |
| **DeepLab v3**  | 개선된 ASPP (image-level pooling 포함)        |
| **DeepLab v3+** | Encoder-Decoder 구조로 경계 복원 강화 (U-Net과 유사) |

---

### 4️⃣ 구조 요약 (v3+ 기준)

```
Input
 ↓
Backbone (ResNet / Xception)
 ↓
Atrous Convolution (stride↓, 해상도 유지)
 ↓
ASPP (다양한 dilation rate 병렬 적용)
 ↓
Decoder (저수준 feature와 결합)
 ↓
Upsampling → Output (Segmentation Map)
```

---

### 5️⃣ 장단점

| 장점           | 설명                                |
| ------------ | --------------------------------- |
| ✅ 해상도 유지     | pooling 없이 dilated conv로 넓은 시야 확보 |
| ✅ 다양한 스케일 인식 | ASPP로 크기 다른 객체 처리 가능              |
| ✅ 경계선 정밀     | Decoder/CRF로 세부 경계 복원             |
| ⚠️ 단점        | 연산량 많고 구조 복잡 (속도 느림)              |

---

### 🎯 핵심 한 줄 요약

> **DeepLab은 Dilated Convolution + ASPP + Decoder 구조를 통해**
> 해상도를 유지하면서 넓은 문맥 정보를 활용하고,
> 경계까지 정교하게 복원하는 **고성능 세그멘테이션 모델**이다. ✅

---

