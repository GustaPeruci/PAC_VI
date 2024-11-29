import cv2
import json
import os
import numpy as np
import requests
import time

# Configuração do servidor Flask
FLASK_URL = "http://127.0.0.1:5000/api/receber_dados"

# Caminhos de arquivos
video_file_path = "C:\\Users\\Gustavo\\Documents\\Projetos\\PAC_VI\\video\\video_canarinho_curto.mp4"
local_data_file = "passenger_data.json"

# Haar Cascade para detecção de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Verificar se o modelo foi carregado
if face_cascade.empty():
    print("Erro: Não foi possível carregar o modelo 'haarcascade_frontalface_default.xml'.")
    exit()

# Limites e parâmetros de detecção
min_face_area = 4000
entry_zone_top = 0
entry_zone_bottom = 200

# Variável de contagem de passageiros
passenger_count = 0

# Função para enviar dados ao servidor Flask
def send_data_to_flask(count):
    data = {"passenger_count": count}
    try:
        response = requests.post(FLASK_URL, json=data)
        if response.status_code == 200:
            print(f"Dados enviados com sucesso: {data}")
        else:
            print(f"Erro ao enviar dados: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

# Função principal para processar o vídeo
def process_video(video_path):
    global passenger_count
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        for (x, y, w, h) in faces:
            if w * h > min_face_area and entry_zone_top <= y <= entry_zone_bottom:
                passenger_count += 1
                send_data_to_flask(passenger_count)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Detecção de Passageiros", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Fluxo principal
if __name__ == "__main__":
    process_video(video_file_path)
