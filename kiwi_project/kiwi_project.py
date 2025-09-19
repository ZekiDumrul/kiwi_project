import cv2
import numpy as np
import matplotlib.pyplot as plt

# Görüntü yükleme
image_path = r"C:\Users\Zeki\Desktop\resim\kiwi.jpg"
image = cv2.imread(image_path)
if image is None:
    print("Görsel yüklenemedi!")
    exit()

copy = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# HSV kivi icin
lower_green = np.array([20, 40, 40])
upper_green = np.array([100, 255, 255])
broad_mask = cv2.inRange(hsv, lower_green, upper_green)

#HSV yaprak icin    
lower_leaf = np.array([40, 80, 80])
upper_leaf = np.array([85, 255, 255])
leaf_mask = cv2.inRange(hsv, lower_leaf, upper_leaf)

final_mask = cv2.bitwise_and(broad_mask, cv2.bitwise_not(leaf_mask))

# Morfolojik işlemler
kernel = np.ones((5,5), np.uint8)
final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel, iterations=4)
final_mask = final_mask.astype(np.uint8)



# Otsu + Canny
otsu_thresh, _ = cv2.threshold(final_mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
lower_o = max(10, int(otsu_thresh * 0.5))
upper_o = max(lower_o+5, int(otsu_thresh))
edges_otsu = cv2.Canny(final_mask, lower_o, upper_o)


contours, _ = cv2.findContours(edges_otsu, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
kiwi_mask = np.zeros_like(final_mask)
kiwi_count = 0

#Alan sınırları
min_area = 700
max_area = 50000

for c in contours:
    hull = cv2.convexHull(c)
    area = cv2.contourArea(hull)
    if min_area < area < max_area:
        cv2.drawContours(kiwi_mask, [hull], -1, 255, -1)
        kiwi_count += 1

# Souçlar
fig, axs = plt.subplots(1, 3, figsize=(15, 6))

axs[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axs[0].set_title("Orijinal Görüntü")
axs[0].axis('off')

axs[1].imshow(edges_otsu, cmap='gray')
axs[1].set_title(f"Otsu ile Kenar tespiti (th={otsu_thresh:.1f})")
axs[1].axis('off')

axs[2].imshow(kiwi_mask, cmap='gray')
axs[2].set_title(f" Kiviler (count={kiwi_count})")
axs[2].axis('off')

plt.tight_layout()
plt.show()

print(f"Tespit edilen kivi sayısı: {kiwi_count}")
