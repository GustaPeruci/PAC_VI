import cv2
import os

# Caminho para o novo vídeo para treinamento
new_video_file_path = "C:\\Users\\Gustavo\\Documents\\Projetos\\PAC_VI\\video_canarinho_completo.mp4"
# Pasta onde as imagens de rostos serão armazenadas
dataset_path = "C:\\Users\\Gustavo\\Documents\\Projetos\\PAC_VI\\faces_dataset"

# Criação da pasta de dataset se não existir
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# Inicializar a captura de vídeo
video_capture = cv2.VideoCapture(new_video_file_path)

# Verificar se o vídeo foi carregado corretamente
if not video_capture.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Carregar o modelo Haar Cascade para detecção de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Contador de rostos e a ID para as imagens
face_id = 0

# Definir intervalo de tempo para processar apenas uma parte do vídeo (em segundos)
start_time = 180  # Tempo de início em segundos
end_time = 240  # Tempo de fim em segundos

# Definir a taxa de quadros por segundo (FPS) do vídeo
fps = video_capture.get(cv2.CAP_PROP_FPS)

# Definir o número do frame inicial
start_frame = int(start_time * fps)
end_frame = int(end_time * fps)

# Ajustar para pular diretamente para o frame de início
video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# Função para extrair rostos e salvar as imagens durante o intervalo de tempo
def extract_faces_and_save(video_capture, face_cascade, dataset_path, start_frame, end_frame):
    global face_id
    print(f"Iniciando a extração de rostos do vídeo entre {start_time}s e {end_time}s...")
    
    frame_count = start_frame

    while True:
        ret, frame = video_capture.read()
        if not ret or frame_count >= end_frame:
            break  # Fim do vídeo ou alcançou o tempo final

        # Definir a região de interesse (ROI) para a parte superior da imagem
        height, width, _ = frame.shape
        roi_height = int(height * 0.4)  # Pega 40% da altura do vídeo (ajustável)
        roi = frame[0:roi_height, 0:width]  # Captura a parte superior do vídeo

        # Converter a ROI para escala de cinza
        gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Detectar rostos no frame (somente na região de interesse)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

        # Filtragem de falsos positivos: Aspect ratio e validação do tamanho do rosto
        valid_faces = []
        for (x, y, w, h) in faces:
            aspect_ratio = w / h
            # Usar um critério de aspecto (valor esperado para rostos humanos)
            if 0.75 < aspect_ratio < 1.5 and w > 50 and h > 50:  # Ignorar áreas muito pequenas
                valid_faces.append((x, y, w, h))

        # Para cada rosto válido, salve a imagem
        for (x, y, w, h) in valid_faces:
            face_image = roi[y:y + h, x:x + w]
            face_filename = os.path.join(dataset_path, f"face_{face_id}.jpg")
            cv2.imwrite(face_filename, face_image)
            face_id += 1
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Exibir a imagem com os rostos detectados
        cv2.imshow("Rostos detectados", roi)

        # Aguardar a tecla 'q' para finalizar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    video_capture.release()
    cv2.destroyAllWindows()
    print(f"Total de {face_id} rostos extraídos entre {start_time}s e {end_time}s.")

# Extrair rostos do vídeo no intervalo de tempo especificado
extract_faces_and_save(video_capture, face_cascade, dataset_path, start_frame, end_frame)
