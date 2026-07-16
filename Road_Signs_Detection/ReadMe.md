# Vision-Based Road Signs Detection & Control in Webots

Ce projet pratique met en œuvre un système complet d'assistance active à la conduite (ADAS) au sein du simulateur Webots. En combinant des techniques de traitement d'images classiques (OpenCV) pour l'attention visuelle et un modèle de Deep Learning embarqué (YOLOv8n) pour la classification en temps réel, le véhicule est capable de détecter 29 classes de panneaux et d'adapter sa conduite de manière autonome.

L'objectif principal de ce projet est de pratiquer l'intégration de bout en bout d'un pipeline d'IA : de la préparation des données et l'entraînement du modèle à l'implémentation de filtres de vision et de boucles de contrôle physique en simulation.

---

## 🚀 Architecture Globale du Système

Le système fonctionne en boucle fermée au sein du contrôleur principal de la simulation :

1. **Capture & Simulation (`Auto_Controller.py`)** : Acquisition du flux vidéo de la caméra embarquée sous Webots et conversion des trames en matrices NumPy.
2. **Prétraitement d'image & ROI (`sign_detector.py` avec OpenCV)** :
   * Focalisation sur le tiers central de l'image (zone d'apparition naturelle des panneaux).
   * Application d'un flou gaussien (noyau 5x5) pour réduire le bruit.
   * Détection de contours de Canny (seuils 80/200)[cite: 8].
   * Approximation polygonale (`approxPolyDP`) pour filtrer géométriquement les formes candidates (3 côtés pour les panneaux triangulaires, >= 6 côtés pour les ronds/octogones)[cite: 8].
3. **Inférence ciblée (YOLOv8n)** : Seules les régions d'intérêt (ROI) géométriquement validées sont envoyées à notre réseau YOLOv8n (redimensionnées en 256x256), réduisant drastiquement la charge CPU[cite: 8].
4. **Contrôle ADAS & Actionnement** : Traduction sémantique de la détection et déclenchement des actions physiques[cite: 8].

---

## 📊 Modèle YOLOv8 : Dataset & Performance

* **Dataset** : 10 000 images issues du dataset *Traffic and Road Signs* (Roboflow) réparties sur 29 classes fonctionnelles[cite: 8].
* **Entraînement** : Réalisé sur Google Colab avec un GPU NVIDIA Tesla T4 pendant 100 époques (taille d'image d'entrée : 416x416)[cite: 8].
* **Métriques obtenues** :
  * **mAP50** : 97.7 % (atteint à l'époque 63)[cite: 8].
  * **Précision (P)** : 97.7 %[cite: 8].
  * **Rappel (R)** : 94.3 %[cite: 8].

### Classes & Logiques de Contrôle Associées

| Catégorie Fonctionnelle | Classes Principales Détectées | Action ADAS Implémentée |
| :--- | :--- | :--- |
| **Arrêt & Interdiction** | Stop_Sign, No Entry, No_Over_Taking... | **AEB** (Freinage d'urgence automatique) à 0 km/h[cite: 8]. |
| **Limitations de Vitesse** | Speed Limit 20/30/50, End of limits... | **ISA** (Régulation intelligente de la vitesse) par décréments de -10 km/h[cite: 8]. |
| **Dangers & Priorités** | Pedestrian Crossing, Give Way, Attention Please... | Alerte visuelle & préparation à la réduction de vitesse[cite: 8]. |

---

## 🛠️ Installation et Utilisation

### Prérequis
* Webots (dernière version recommandée)
* Python 3.9+
* OpenCV (`opencv-python`)
* Ultralytics YOLOv8 (`ultralytics`)

### Configuration de l'environnement
1. Clonez ce dépôt :
   ```bash
   git clone [https://github.com/votre-username/votre-nom-de-repo.git](https://github.com/votre-username/votre-nom-de-repo.git)
   cd votre-nom-de-repo
