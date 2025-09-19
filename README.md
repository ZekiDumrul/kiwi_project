## openCV ile kivi tespit etme
Bu proje, OpenCV ve NumPy kullanarak görseldeki kivileri tespit etmeyi amaçlar.
HSV renk uzayı, morfolojik işlemler, Otsu threshold ve Canny edge detection yöntemleri kullanılarak kiviler maskelenir ve konturlar yardımıyla sayılır.

## Özellikler:
- HSV tabanlı maskeleme (kivi rengi + yaprak ayırma)
- Gürültü azaltma için morfolojik işlemler
- Otsu + Canny ile kenar tespiti
- Kontur analizi ile kivi sayımı
- Görselleştirme: Orijinal resim, kenar tespiti, maske

## Gerekli Araçlar :
Python 3.x
OpenCV
NumPy
Matplotlib

## Çalışma Mantığı

1. **Görselin yüklenmesi**
   - Kullanıcı tarafından verilen görüntü okunur.  

2. **HSV Renk Uzayına Çevirme**  
   - Görsel, BGR’den HSV renk uzayına dönüştürülür.  
   - HSV, renk tabanlı nesne tespitinde daha kararlı sonuçlar verdiği için tercih edilir.  

3. **Kivi ve Yaprak Maskelerinin Oluşturulması**  
   - Kivi için uygun HSV aralığı tanımlanır.  #hue (h) = renk tonu , saturatiın (s) = dolgunluk , value (v) = parlaklık
   - Yapraklar için ayrıca bir HSV aralığı belirlenir.  
   - Kivi maskesi, yaprak maskesi çıkarılarak elde edilir.  

4. **Morfolojik İşlemler**  
   - Gürültüyü azaltmak için **close** ve **open** işlemleri uygulanır.  
   - Böylece maskede daha düzgün bölgeler elde edilir.  

5. **Otsu + Canny ile Kenar Tespiti**  
   - Otsu metodu ile dinamik bir eşik değeri hesaplanır.  
   - Bu eşik değeri Canny algoritmasına verilerek kenarlar çıkarılır.  

6. **Kontur Analizi ile Kivi Bulma**  
   - Kenarlardan konturlar elde edilir.  
   - Her konturun alanı hesaplanır.  
   - ""min_area < alan < max_area"" koşulunu sağlayan konturlar kivi olarak kabul edilir.  

7. **Sonuçların Gösterilmesi**  
   - Orijinal görüntü, kenar tespiti ve kivi maskesi görselleştirilir.  
   - Terminalde toplam **kivi sayısı** yazdırılır.  
