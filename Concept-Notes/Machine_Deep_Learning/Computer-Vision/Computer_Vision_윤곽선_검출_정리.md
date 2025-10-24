

---

# 🖼️ Contour Detection (윤곽선 검출) 정리

## 1. Input Image

* **입력 이미지 준비**
  일반적으로 그레이스케일(grayscale) 변환 후 엣지 검출을 수행하는 것이 효과적임.

  ```python
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ```

---

## 2. Canny Edge Detector (엣지 검출)

Canny 알고리즘은 대표적인 엣지 검출 방식으로 **5단계**로 요약됨.

1. **노이즈 제거**

   * Gaussian Blur(가우시안 필터)를 적용하여 고주파 노이즈 제거
   * 이유: 노이즈가 그대로 있으면 엣지 검출 과정에서 잘못된 경계가 생김

   ```python
   blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
   ```

2. **Gradient 계산 (엣지 강도 추출)**

   * Sobel 커널을 X, Y 방향에 적용하여 기울기(gradient) 계산
   * 강한 기울기 → 엣지 가능성이 높은 픽셀

3. **Non-Maximum Suppression (비최대 억제)**

   * gradient 방향을 따라 **가장 큰 픽셀 값만 유지**, 나머지는 0으로 제거
   * 얇고 선명한 엣지를 남김

4. **Double Threshold (이중 임계값 적용)**

   * `high threshold`, `low threshold` 두 개의 값을 지정
   * **강한 엣지(strong edge)**는 무조건 유지
   * **약한 엣지(weak edge)**는 강한 엣지와 연결된 경우만 유지

5. **Edge Tracking by Hysteresis**

   * 연결된 엣지들을 최종적으로 남겨 확정

   ```python
   edges = cv2.Canny(blurred, 100, 200)  # low=100, high=200
   ```

---

## 3. Dilation (팽창 연산)

* Canny 결과는 얇은 선만 추출되기 때문에 **빈 공간을 메우고 연결성 강화** 필요
* Morphological 연산 중 `dilate` 사용
* 여러 contour들이 끊어져 검출되는 문제를 완화

```python
kernel = np.ones((3,3), np.uint8)
dilated = cv2.dilate(edges, kernel, iterations=1)
```

---

## 4. Contour Detection

* **윤곽선 찾기 (cv2.findContours)**

  * 검출된 edge map을 입력받아, 픽셀들을 연결하여 **윤곽선(contour)**으로 반환
  * 반환값: `contours, hierarchy`

  ```python
  contours, hierarchy = cv2.findContours(
      dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
  )
  ```

* 주요 파라미터

  * `cv2.RETR_EXTERNAL`: 외곽선만 검출
  * `cv2.RETR_TREE`: 모든 계층적 윤곽선 검출
  * `cv2.CHAIN_APPROX_SIMPLE`: 점들을 직선으로 압축하여 저장 (메모리 효율 ↑)

---

## 5. 결과 시각화

* `cv2.drawContours` 함수를 사용해 최종 윤곽선을 원본 이미지에 표시

```python
result = image.copy()
cv2.drawContours(result, contours, -1, (0,255,0), 2)
```

---

# 📌 전체 파이프라인 요약

1. **Input Image** → (컬러 → 그레이스케일 변환)
2. **Canny Edge Detection**

   * Gaussian Blur → Sobel → Non-Max Suppression → Double Threshold → Edge Tracking
3. **Morphological Dilation** (끊어진 엣지 연결)
4. **Contour Detection** (`cv2.findContours`)
5. **결과 시각화** (`cv2.drawContours`)

---

# 💡 추가 포인트

* **Canny의 threshold 값(예: 100, 200)은 하이퍼파라미터**
  → 데이터마다 최적 값이 다르므로 실험 필요
* **Dilation과 Erosion**을 적절히 조합하면, 노이즈 제거/구멍 채우기/객체 경계 강화 가능
* Contour는 단순히 객체 경계뿐 아니라 **객체 검출, 분할(Segmentation), 특징 추출**에도 많이 활용됨

---

