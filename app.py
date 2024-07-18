import gradio as gr
import numpy as np
from loading import load_model

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
    img = load_model(input_img, float(pos), int(confidence))
    return img

# Definición de los sliders para la interfaz de Gradio
pos_slider = gr.Slider(minimum=MIN_CONF, maximum=MAX_CONF, value=0.5, step=0.1, label="Confianza de Detección", interactive=True)
confidence_slider = gr.Slider(minimum=MIN_POS, maximum=MAX_POS, value=3, step=1, label="Número de Poses", interactive=True)

# Creación de la interfaz de Gradio
demo = gr.Interface(fn=process_image, 
                          inputs=[gr.Image(), pos_slider, confidence_slider], 
                          outputs=gr.Image(),
                          title="Pose Detection App",
                          description="Ajusta los parámetros y carga una imagen para detectar poses.",
                          allow_flagging="never")

demo.queue().launch()


# # Iniciar la aplicación FastAPI
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# Dependencias necesarias:
# pip install fastapi uvicorn
# pip install --upgrade gradio

# Para ejecutar la aplicación:
# uvicorn main:app --reload
