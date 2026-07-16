def Fr_Classifier(Sign_classe):
    match Sign_classe:
        case "-Road narrows on right":
            return "Chaussée rétrécie à droite"

        case "50 mph speed limit":
            return "Limitation de vitesse à 50 Km/h"

        case "Attention Please-":
            return "Attention"

        case "Beware of children":
            return "Attention aux enfants"

        case "CYCLE ROUTE AHEAD WARNING":
            return "Piste cyclable à venir"

        case "Dangerous Left Curve Ahead":
            return "Virage dangereux à gauche"

        case "Dangerous Rright Curve Ahead":
            return "Virage dangereux à droite"

        case "End of all speed and passing limits":
            return "Fin de toutes les limitations de vitesse et de dépassement"

        case "Give Way":
            return "Cédez le passage"

        case "Go Straight or Turn Right":
            return "Tout droit ou à droite"

        case "Go straight or turn left":
            return "Tout droit ou à gauche"

        case "Keep-Left":
            return "Contourner par la gauche"

        case "Keep-Right":
            return "Contourner par la droite"

        case "Left Zig Zag Traffic":
            return "Succession de virages (premier à gauche)"

        case "No Entry":
            return "Sens interdit"

        case "No_Over_Taking":
            return "Dépassement interdit"

        case "Overtaking by trucks is prohibited":
            return "Dépassement interdit aux poids lourds"

        case "Pedestrian Crossing":
            return "Passage pour piétons"

        case "Round-About":
            return "Rond-point"

        case "Slippery Road Ahead":
            return "Chaussée glissante"

        case "Speed Limit 20 KMPh":
            return "Limitation de vitesse à 20 km/h"

        case "Speed Limit 30 KMPh":
            return "Limitation de vitesse à 30 km/h"

        case "Stop_Sign":
            return "Stop"

        case "Straight Ahead Only":
            return "Direction obligatoire tout droit"

        case "Traffic_signal":
            return "Feux de signalisation"

        case "Truck traffic is prohibited":
            return "Circulation des poids lourds interdite"

        case "Turn left ahead":
            return "Tourner à gauche"

        case "Turn right ahead":
            return "Tourner à droite"

        case "Uneven Road":
            return "Chemin déformée"

        case _:
            return "Panneau inconnu"