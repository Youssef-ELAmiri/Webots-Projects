"""
Contrôleur de Perception Automobile pour Webots
------------------------------------------------
- Contrôle au clavier (Avance, Recul, Direction, Frein)
- Capture OpenCV avec fenêtre redimensionnable
- Création automatique du Dataset
"""

from vehicle import Driver
from controller import Keyboard
import numpy as np
import cv2
import os
from ultralytics import YOLO

# Chargement du modèle YOLO (Utilise "yolov8n.pt" pour tester, ou ton "best.pt" si tu as déjà entraîné ton modèle)
print("[INFO] Chargement du modèle YOLO...")
model = YOLO("yolov8n.pt")

# ==========================================
# 1. INITIALISATION DE LA SIMULATION
# ==========================================
driver = Driver()
timestep = int(driver.getBasicTimeStep())

# Initialisation de la caméra
camera = driver.getDevice("camera")
camera.enable(timestep)
camera_width = camera.getWidth()
camera_height = camera.getHeight()
print(f"Camera resolution : {camera_width} / {camera_height}")
# Initialisation du clavier
keyboard = Keyboard()
keyboard.enable(timestep)

# Configuration de l'état initial
autodrive = False       # On commence en manuel pour te laisser le contrôle
speed = 0.0             # Vitesse à l'arrêt au démarrage
steering_angle = 0.0
frame_counter = 0

# Création du dossier pour le Dataset
dataset_dir = "dataset"
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)
    print(f"[INFO] Dossier '{dataset_dir}' créé avec succès.")

# Éclairage
driver.setHazardFlashers(True)
driver.setDippedBeams(True)

# Configuration de la fenêtre OpenCV pour qu'elle soit redimensionnable à la souris
cv2.namedWindow("Camera Webots", cv2.WINDOW_NORMAL)
# Optionnel : Forcer une taille d'affichage de départ plus grande (ex: 800x600)
cv2.resizeWindow("Camera Webots", 800, 600)

print("\n" + "="*40)
print(" VÉHICULE PRÊT - COMMANDES CLAVIER :")
print("="*40)
print(" [ A ]         : Activer / Désactiver l'Auto-Pilote")
print(" [ HAUT ]      : Accélérer (Marche Avant)")
print(" [ BAS ]       : Ralentir / Marche Arrière")
print(" [ G/D ]       : Tourner le volant")
print(" [ ESPACE ]    : Frein à main (Arrêt d'urgence)")
print("="*40 + "\n")

# ==========================================
# 2. BOUCLE PRINCIPALE
# ==========================================
while driver.step() != -1:
    
    # --- GESTION DES COMMANDES ---
    key = keyboard.getKey()
    
    if key == ord('A'):
        autodrive = not autodrive
        print(f"\n>>> MODE AUTO : {'ACTIVÉ' if autodrive else 'DÉSACTIVÉ'} <<<")
        # Si on repasse en manuel, on remet le volant droit
        if not autodrive:
            driver.setSteeringAngle(0.0)
            
    if not autodrive:
        # Relâcher le frein par défaut
        driver.setBrakeIntensity(0.0) 
        
        if key == Keyboard.UP:
            speed = min(speed + 2.0, 100.0) # Vitesse max : 100 km/h
            driver.setCruisingSpeed(speed)
            print(f"Vitesse : {speed} km/h")
            
        elif key == Keyboard.DOWN:
            speed = max(speed - 2.0, -30.0) # Marche arrière max : -30 km/h
            driver.setCruisingSpeed(speed)
            if speed < 0:
                print(f"Marche Arrière : {speed} km/h")
            else:
                print(f"Vitesse : {speed} km/h")
                
        elif key == Keyboard.RIGHT:
            steering_angle = max(steering_angle + 0.05, +0.5)
            driver.setSteeringAngle(steering_angle)
            
        elif key == Keyboard.LEFT:
            steering_angle = min(steering_angle - 0.05, -0.5)
            driver.setSteeringAngle(steering_angle)
            
        elif key == ord(' '): # Barre d'espace
            speed = 0.0
            driver.setCruisingSpeed(speed)
            driver.setBrakeIntensity(1.0) # Freinage max
            print("!!! FREINAGE D'URGENCE !!!")
            
    else:
        # --- LOGIQUE DU MODE AUTOMATIQUE ---
        # Pour l'instant, la voiture roule tout droit à 30 km/h
        # C'est ici que tu brancheras YOLO plus tard pour qu'elle s'arrête au Stop
        driver.setBrakeIntensity(0.0)
        driver.setCruisingSpeed(30.0)
        driver.setSteeringAngle(0.0)


    # --- GESTION DE LA CAMÉRA & DATASET ---
    # --- GESTION DE LA CAMÉRA & DÉTECTION ---
    image_data = camera.getImage()
    
    if image_data:
        # Conversion Webots -> OpenCV
        img_array = np.frombuffer(image_data, np.uint8).reshape((camera_height, camera_width, 4))
        img_cv2 = img_array[:, :, :3]
        
        # Copie de l'image pour dessiner dessus sans modifier l'originale
        img_affichage = img_cv2.copy()
        
       # --- OPTIMISATION : On ne lance YOLO que 1 fois sur 5 (Frame Skipping) ---
        if frame_counter % 5 == 0:
            
            # imgsz=320 force YOLO à travailler sur une plus petite image pour aller plus vite
            resultats = model.predict(img_cv2, imgsz=320, verbose=False) 
            
            # 2. ANALYSER LES RÉSULTATS
            for r in resultats:
                boites = r.boxes 
                
                for boite in boites:
                    class_id = int(boite.cls[0])
                    
                    if class_id == 11: # Panneau STOP
                        x1, y1, x2, y2 = boite.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        
                        cv2.rectangle(img_affichage, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(img_affichage, "PANNEAU", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        
                        panneau_rogne = img_cv2[y1:y2, x1:x2]
                        if panneau_rogne.size > 0:
                            cv2.imshow("Panneau Detecte (Rogne)", panneau_rogne) 
        
        # 2. ANALYSER LES RÉSULTATS
        for r in resultats:
            boites = r.boxes # Récupère toutes les boîtes détectées
            
            for boite in boites:
                # Récupérer l'ID de la classe détectée (converti en entier)
                class_id = int(boite.cls[0])
                
                # --- FILTRE : On ne garde que les panneaux ---
                # NOTE : Dans le modèle yolov8n de base (COCO), le panneau STOP est la classe 11.
                # Si tu utilises ton propre modèle, remplace 11 par ton ID (souvent 0).
                if class_id == 11: 
                    
                    # Récupérer les coordonnées exactes
                    x1, y1, x2, y2 = boite.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Dessiner un rectangle rouge autour du panneau sur l'image principale
                    cv2.rectangle(img_affichage, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(img_affichage, "PANNEAU", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    
                    # --- LE ROGNAGE (CROP) ---
                    # Attention à bien faire y1:y2 en premier (lignes), puis x1:x2 (colonnes)
                    panneau_rogne = img_cv2[y1:y2, x1:x2]
                    
                    # Vérifier que le crop n'est pas vide (évite les crashs)
                    if panneau_rogne.size > 0:
                        # Afficher l'image rognée dans une petite fenêtre à part
                        cv2.imshow("Panneau Detecte (Rogne)", panneau_rogne)
                        
                        # (Optionnel) Tu pourrais sauvegarder ce panneau rogné ici :
                        # cv2.imwrite("panneau_trouve.jpg", panneau_rogne)
                        
        
        # 3. Affichage de la vue globale
        cv2.imshow("Camera Webots", img_affichage)
        cv2.waitKey(1)
            
        frame_counter += 1

# ==========================================
# 3. NETTOYAGE
# ==========================================
cv2.destroyAllWindows()