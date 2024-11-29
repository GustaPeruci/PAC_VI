import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time
from mtcnn.mtcnn import MTCNN

# Configuração MQTT
BROKER_ADDRESS = "localhost"  # Endereço do broker MQTT (use 'localhost' para rodar localmente)
MQTT_TOPIC = "iot/passenger_count"

# Caminhos de arquivos
video_file_path = "C:\\Users\\Gustavo\\Documents\\Projetos\\PAC_VI\\videos\\video_canarinho_curto.mp4"

# Inicializando o detector MTCNN para detecção de rostos
detector = MTCNN()

# Variáveis para controle de detecção e contagem de passageiros
passenger_count = 0
entry_zone_top = 0
entry_zone_bottom = 200
min_face_area = 4000  # Limite de tamanho do rosto para considerar como válido

# Configuração do cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER_ADDRESS)

# Função para reduzir a taxa de quadros e tornar o sistema mais lento
def reduce_frame_rate():
    time.sleep(0.5)  # Atraso de 0.5 segundos entre os quadros para diminuir o FPS

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

        # Reduzir a taxa de quadros para tornar o sistema mais lento
        reduce_frame_rate()

        # Detecção de rostos com MTCNN
        result = detector.detect_faces(frame)

        # Lista para armazenar rostos detectados no quadro atual
        current_faces = []

        for face in result:
            x, y, w, h = face['box']
            # Verifica se a área do rosto é maior que o limite mínimo
            if w * h > min_face_area and entry_zone_top <= y <= entry_zone_bottom:
                # Validando que realmente é um rosto humano, baseado na probabilidade de cada face
                if face['confidence'] > 0.9:  # Considera rostos com alta confiança
                    # Adiciona à lista de rostos detectados
                    current_faces.append((x, y, w, h))
                    passenger_count += 1
                    # Publica a contagem de passageiros no tópico MQTT
                    mqtt_client.publish(MQTT_TOPIC, str(passenger_count))
                    print(f"Contagem de passageiros enviada via MQTT: {passenger_count}")
                else:
                    print("Detecção de objeto não confiável, ignorado.")

        # Exibe os rostos detectados na imagem
        for (x, y, w, h) in current_faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Detecção de Passageiros", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Fluxo principal
if __name__ == "__main__":
    print("Simulador IoT iniciado. Enviando dados via MQTT...")
    process_video(video_file_path)
