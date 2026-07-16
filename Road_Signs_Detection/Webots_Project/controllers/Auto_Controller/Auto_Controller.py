from vehicle import Driver
from controller import Keyboard
import numpy as np
import cv2
from sign_detector import Detector
from Classifier import Fr_Classifier

driver = Driver()
timestep = int(driver.getBasicTimeStep())

camera = driver.getDevice("camera")
camera.enable(timestep)
camera_width = camera.getWidth()
camera_height = camera.getHeight()

keyboard = Keyboard()
keyboard.enable(timestep)

detector = Detector("models/best.pt")

speed = 0.0
steering_angle = 0.0
frame_counter = 0

cv2.namedWindow("Camera Webots", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Camera Webots", 500, 500)

print("VÉHICULE PRÊT !")
print("Contrôle Manuel : UP/DOWN/RIGHT/LEFT")
print("Assistance activée\n")

while driver.step() != -1:
    
    key = keyboard.getKey()
    
    last_speed = speed

    if key == Keyboard.UP:
        speed = min(speed + 4.0, 100.0)
        driver.setBrakeIntensity(0.0)
    elif key == Keyboard.DOWN:
        speed = max(speed - 3.0, -30.0)
        driver.setBrakeIntensity(0.0)
    elif key == Keyboard.RIGHT:
        steering_angle = min(steering_angle + 0.02, 0.5)
    elif key == Keyboard.LEFT:
        steering_angle = max(steering_angle - 0.02, -0.5)
    elif key == ord(' '):
        speed = 0.0
        driver.setBrakeIntensity(1.0)
    else:
        steering_angle *= 0.9 
        
    driver.setCruisingSpeed(speed)
    driver.setSteeringAngle(steering_angle)

    if speed != last_speed:
        print(f"Vitesse actuelle : {speed:.1f} km/h")

    image_data = camera.getImage()
    
    if image_data:
        img_array = np.frombuffer(image_data, np.uint8).reshape((camera_height, camera_width, 4))
        img_cv2 = img_array[:, :, :3]
        
        img_to_detector = img_cv2.copy()
        #height,width = img_to_detector.shape[0:2]
        #img_affichage = img_to_detector[int(height/4):int((3*height)/4),int(width/4):int(3*(width)/4),:]
        

        if frame_counter % 5 == 0:
            img_affichage, liste_panneaux = detector.detect_and_draw(img_to_detector)
            
            if liste_panneaux:
                for panneau in liste_panneaux:
                    Sign = Fr_Classifier(panneau)
                    print(f"Panneau en vue : {Sign}")
                    
                    if panneau in ['Stop_Sign', 'No Entry']:
                        if speed > 0.0:
                            print(f"\nDANGER ({Sign}) : Freinage d'urgence automatique !")
                            speed = 0.0
                            driver.setCruisingSpeed(0.0)
                            driver.setBrakeIntensity(1.0)
                            print("Vous pouvez accelerer pour répartir.\n")
                    if panneau == "50 mph speed limit" :
                        while speed > 50:
                            speed =- 5
                            driver.setCruisingSpeed(speed)
                            print("Freinage! Vitesse élevée > 50")
                            print(f"Vitesse actuelle : {speed:.1f} km/h")
                    if panneau == "Speed Limit 20 KMPh" :
                        while speed > 20:
                            speed =- 10
                            driver.setCruisingSpeed(speed)
                            print("Freinage! Vitesse élevée > 20")
                            print(f"Vitesse actuelle : {speed:.1f} km/h")
                    if panneau == "Speed Limit 30 KMPh" :
                        while speed > 30:
                            speed =- 10
                            driver.setCruisingSpeed(speed)
                            print("Freinage! Vitesse élevée > 30")
                            print(f"Vitesse actuelle : {speed:.1f} km/h")
        cv2.imshow("Camera Webots", img_affichage)
        cv2.waitKey(1)
        frame_counter += 1

cv2.destroyAllWindows()