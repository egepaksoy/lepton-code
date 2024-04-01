import time
import numpy as np
import cv2
import Lepton

# Raspberry Pi'ye Lepton kamerayı bağlama
Lepton.init_spi()

# Termal görüntüyü okuma ve işleme fonksiyonu
def capture_image():
    _, frame = Lepton.capture()
    # Görüntüyü 8-bit grayscale'e dönüştürme
    frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return frame

# Raspberry Pi ekran boyutları
screen_width = 640
screen_height = 480

# Raspberry Pi ekranını oluşturma
disp = cv2.VideoCapture(-1)
disp.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
disp.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

while True:
    # Termal görüntüyü al
    thermal_image = capture_image()
    
    # Raspberry Pi ekranına termal görüntüyü gönderme
    _, frame = disp.read()
    frame[:thermal_image.shape[0], :thermal_image.shape[1]] = thermal_image
    
    # Raspberry Pi ekranını gösterme
    cv2.imshow('Thermal Camera', frame)
    
    # Çıkış tuşuna basılırsa döngüyü kır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Pencereleri kapatma ve Lepton bağlantısını kapatma
cv2.destroyAllWindows()
disp.release()
Lepton.deinit()
