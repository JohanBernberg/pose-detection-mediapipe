import numpy as np
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Crear un objeto PoseLandmarker
model_asset_path = 'pose_landmarker_heavy.task'
base_options = python.BaseOptions(model_asset_path, delegate=python.BaseOptions.Delegate.CPU)

def draw_landmarks_on_image(rgb_image, detection_result):
    """
    Dibuja los puntos de referencia de la pose en la imagen.

    Args:
    rgb_image (np.ndarray): Imagen RGB de entrada.
    detection_result: Resultado de la detección de pose.

    Returns:
    np.ndarray: Imagen anotada con los puntos de referencia de la pose.
    """
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)
    # Recorrer las poses detectadas para visualizarlas
    for pose_landmarks in pose_landmarks_list:
        # Dibujar los puntos de referencia de la pose
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image

def load_model(input_img, pos, confidence):
    """
    Carga el modelo de detección de pose y lo aplica a la imagen de entrada.

    Args:
    input_img (np.ndarray): La imagen de entrada.
    pos (float): Confianza mínima para la detección de poses.
    confidence (int): Número máximo de poses a detectar.

    Returns:
    np.ndarray: Imagen anotada con los resultados de la detección de poses.
    """
    # Configuración del objeto PoseLandmarker con parámetros própios    
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        num_poses=confidence,
        min_pose_detection_confidence=pos,
        min_pose_presence_confidence=pos,
        min_tracking_confidence=pos)
    detector = vision.PoseLandmarker.create_from_options(options)

    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=input_img)

    # Detectar los puntos de referencia de la pose en la imagen de entrada
    detection_result = detector.detect(rgb_frame)

    # Procesar el resultado de la detección y visualizarlo
    annotated_image = draw_landmarks_on_image(rgb_frame.numpy_view(), detection_result)
    
    return annotated_image
