from ultralytics import YOLO

if __name__ == '__main__':
    # Charger un modèle vide
    model = YOLO('yolov8n.yaml') 

    # Lancer l'entraînement
    model.train(
        data='C:/chemin/vers/ton/data.yaml', 
        epochs=50, 
        imgsz=640, 
        device='cpu' # Remplace par 0 si tu as une carte Nvidia
    )