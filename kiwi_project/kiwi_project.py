import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = r"your_image_path"
class KiwiMask:
    def __init__(self, image_path, min_area=700, max_area=50000):
        self.image_path = image_path
        self.min_area = min_area
        self.max_area = max_area
        
        # Görüntüyü yükle
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            print("Görsel yüklenemedi")
        
        self.mask = None
        self.edges = None
        self.kiwi_mask = None
        self.kiwi_count = 0
    
    def mask_and_morf_process(self):
        #HSV 
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        
        # HSV kivi icin
        lower_green = np.array([20, 40, 40])
        upper_green = np.array([100, 255, 255])
        broad_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # HSV yaprak icin
        lower_leaf = np.array([40, 80, 80])
        upper_leaf = np.array([85, 255, 255])
        leaf_mask = cv2.inRange(hsv, lower_leaf, upper_leaf)
        
        # Kivi maskesini yapraklardan ayırma
        self.mask = cv2.bitwise_and(broad_mask, cv2.bitwise_not(leaf_mask))
        
        # Morfolojik işlemler
        kernel = np.ones((5,5), np.uint8)
        self.mask = cv2.morphologyEx(self.mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        self.mask = cv2.morphologyEx(self.mask, cv2.MORPH_OPEN, kernel, iterations=4)
        self.mask = self.mask.astype(np.uint8)
    
    def detect_edges(self):
        
        otsu_thresh, _ = cv2.threshold(self.mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        lower_o = max(10, int(otsu_thresh * 0.5))
        upper_o = max(lower_o+5, int(otsu_thresh))
        self.edges = cv2.Canny(self.mask, lower_o, upper_o)
        
    
    def find_kiwis(self):
        """Konturlar ile kivi tespiti"""
        contours, _ = cv2.findContours(self.edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.kiwi_mask = np.zeros_like(self.mask)
        self.kiwi_count = 0
        
        for c in contours:
            hull = cv2.convexHull(c)
            area = cv2.contourArea(hull)
            if self.min_area < area < self.max_area:
                cv2.drawContours(self.kiwi_mask, [hull], -1, 255, -1)
                self.kiwi_count += 1
    
    def show_results(self):
        """Gorseller"""
        fig, axs = plt.subplots(1, 3, figsize=(15, 6))

        axs[0].imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        axs[0].set_title("Orijinal Görüntü")
        axs[0].axis('off')

        axs[1].imshow(self.edges, cmap='gray')
        axs[1].set_title(f"Otsu ile Kenar tespiti ")
        axs[1].axis('off')

        axs[2].imshow(self.kiwi_mask, cmap='gray')
        axs[2].set_title(f"Kiviler (count={self.kiwi_count})")
        axs[2].axis('off')

        plt.tight_layout()
        plt.show()
    
    def run(self):
        
        self.mask_and_morf_process()
        self.detect_edges()
        self.find_kiwis()
        self.show_results()
        print(f"Tespit edilen kivi sayısı: {self.kiwi_count}")


kiwi_detect = KiwiMask(image_path)
kiwi_detect.run()
