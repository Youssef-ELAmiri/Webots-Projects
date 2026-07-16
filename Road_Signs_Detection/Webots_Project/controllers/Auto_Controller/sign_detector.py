from ultralytics import YOLO
import cv2
import numpy as np

class Detector:
    def __init__(self, model_path="best.pt"):
        print(f"[INFO] Chargement du modèle {model_path}...")
        self.model = YOLO(model_path)

    def find_potential_signs(self, frame):

        zones_interet = []
        
        height,width = frame.shape[0:2]
        
        #img_croped = frame[int(height/4):int((3*height)/4),int(width/4):int(3*(width)/4),:]
        img_croped = frame
        gray = cv2.cvtColor(img_croped, cv2.COLOR_BGR2GRAY)
        
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        edges = cv2.Canny(blurred, 80, 200)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 400 :
                continue
                
            perimetre = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * perimetre, True)
            nb_cotes = len(approx)

            if nb_cotes == 3 or nb_cotes >= 6:
                x, y, w, h = cv2.boundingRect(cnt)
                
                marge = 5
                y1 = max(0, y - marge)
                y2 = min(img_croped.shape[0], y + h + marge)
                x1 = max(0, x - marge)
                x2 = min(img_croped.shape[1], x + w + marge)
                
                crop = img_croped[y1:y2, x1:x2]
                
                if crop.size > 0:
                    zones_interet.append({
                        'crop': crop,
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2 })
                  
        return zones_interet

    def detect_and_draw(self, frame):

        #img_affichage = frame.copy()
        height,width = frame.shape[0:2]
        img_croped = frame[int(height/3):int((2*height)/3),int(width/3):int(2*(width)/3),:]
        
        panneaux_detectes = []
        
        zones = self.find_potential_signs(img_croped)
        
        for zone in zones:
            cv2.rectangle(img_croped, (zone['x1'], zone['y1']), (zone['x2'], zone['y2']), (255, 200, 0), 1)
            

            resultats = self.model.predict(zone['crop'], imgsz=256, verbose=False) 
            
            for r in resultats:
                for boite in r.boxes:
                    confiance = float(boite.conf[0])
                    if confiance < 0.75:
                        continue

                    class_id = int(boite.cls[0])
                    nom_du_panneau = self.model.names[class_id]
                    
                    cv2.rectangle(img_croped, (zone['x1'], zone['y1']), (zone['x2'], zone['y2']), (0, 0, 255), 2)
                    cv2.putText(img_croped, f"{nom_du_panneau} ({confiance:.2f})", (zone['x1'], zone['y1'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    panneaux_detectes.append(nom_du_panneau)
                    
        return img_croped, panneaux_detectes