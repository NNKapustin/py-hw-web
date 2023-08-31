import cv2
import numpy
from celery import Celery
from cv2 import dnn_superres

from tools import singleton

celery_app = Celery(backend="redis://127.0.0.1:6379/1", broker="redis://127.0.0.1:6379/2")


@singleton
def get_scaler() -> cv2.dnn_superres.DnnSuperResImpl:
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel("ml_models/EDSR_x2.pb")
    scaler.setModel("edsr", 2)
    return scaler


def upscale(image_bytes: bytes) -> bytes:
    """
    :param input_path: байты изображеня
    :return:
    """
    file_bytes = numpy.asarray(bytearray(image_bytes), dtype=numpy.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    scaler = get_scaler()

    image = scaler.upsample(image)
    _, image = cv2.imencode(".jpg", image)
    return image.tobytes()
