import cv2
import numpy as np  # Adicione esta linha
import os
from PIL import Image

# Caminho onde as imagens de rostos estão armazenadas
dataset_path = "C:\\Users\\Gustavo\\Documents\\Projetos\\PAC_VI\\faces_dataset"
# Caminho onde o modelo treinado será salvo
model_output_path = "C:\\Users\\Gustavo\\Documents\\Projetos\\PAC_VI\\haarcascade_trained.xml"

# Lista de imagens e seus labels
faces = []
labels = []

# Iterar sobre as imagens no dataset e extrair rostos
def prepare_training_data(dataset_path):
    for filename in os.listdir(dataset_path):
        img_path = os.path.join(dataset_path, filename)
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Adicionar a imagem à lista de rostos e o label (ID) correspondente
        faces.append(gray)
        labels.append(0)  # Label fixo, pois estamos detectando rostos individuais por enquanto
    
    return faces, labels

# Carregar dados de treino
faces, labels = prepare_training_data(dataset_path)

# Treinar o classificador Haar Cascade
print("Iniciando o treinamento do classificador Haar...")
face_cascade = cv2.face.LBPHFaceRecognizer_create()
face_cascade.train(faces, np.array(labels))

# Salvar o modelo treinado
face_cascade.save(model_output_path)
print(f"Modelo treinado e salvo em {model_output_path}")
