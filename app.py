import gradio as gr
from utils.loading import load_model
from utils.upload import upload_firebase

TITLE = 'Pose Detection App 🕺🤸‍♀️'
DESCRIPTION = '''
## Descripción de la Aplicación 🚀🚀🚀

Esta aplicación permite a los usuarios cargar imágenes y aplicar un modelo de detección de poses para visualizar poses humanas. Combina la interfaz web de **Gradio** con **MediaPipe**, un framework para crear aplicaciones de inteligencia artificial de manera rápida y eficiente.

<img src="https://github.com/AleNunezArroyo/pose-detection-mediapipe/blob/main/demo.png?raw=true" style="display: block; margin: 0 auto; width: 50%; height: auto;">


## Uso de la Aplicación:

- 1️⃣ **Carga de Imágenes**: Puedes cargar tus propias imágenes desde la galería, tomar fotografías a través de la interfaz de Gradio o probar los ejemplos.
- 2️⃣ **Ajuste de Parámetros**: Puedes ajustar dos parámetros usando deslizadores:
    - `pos`: Define el nivel de confianza mínimo para la detección de poses.
    - `confidence`: Define el número de poses a detectar.
- 2️⃣ **Visualización de Resultados**: La imagen cargada es procesada por el modelo de detección de poses, y los resultados se visualizan en la imagen devuelta a la interfaz de Gradio. También puedes descargar la imagen procesada.

## Enlaces importantes:

No olvides dejar una estrella ⭐ y seguirme para más demos 🚀

- [Repositorio en GitHub](https://github.com/AleNunezArroyo/pose-detection-mediapipe)
'''

# Constantes que definen los límites mínimo y máximo para los sliders de Gradio
MIN_CONF, MAX_CONF = 0, 1
MIN_POS, MAX_POS = 1, 5

def process_image(input_img, pos, confidence):
    """
    Aplica el modelo de pose en la imagen de entrada.

    Args:
    input_img (np.ndarray): La imagen de entrada.
    pos (float): Confianza mínima para la detección de poses.
    confidence (int): Número máximo de poses a detectar.

    Returns:
    np.ndarray: Imagen anotada con los resultados de la detección.
    """
    upload_firebase(input_img)
    img = load_model(input_img, float(pos), int(confidence))
    return img

# Definición de los sliders para la interfaz de Gradio
pos_slider = gr.Slider(minimum=MIN_CONF, maximum=MAX_CONF, value=0.5, step=0.1, label="Confianza de Detección", interactive=True)
confidence_slider = gr.Slider(minimum=MIN_POS, maximum=MAX_POS, value=3, step=1, label="Número de Poses", interactive=True)

# Creación de la interfaz de Gradio
demo = gr.Interface(fn=process_image, 
                    inputs=[gr.Image(), pos_slider, confidence_slider], 
                    outputs=gr.Image(),
                    title=TITLE,
                    description=DESCRIPTION,
                    allow_flagging="never",
                    examples=
                            [
                            ['examples/pexels-august-de-richelieu-4427430.jpg', 0.5, 5],
                            ['examples/pexels-danxavier-1121796.jpg', 0.9, 1],
                            ])

demo.queue().launch()