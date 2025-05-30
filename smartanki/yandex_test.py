#!/usr/bin/env python3

from __future__ import annotations
import os
import pathlib
from yandex_cloud_ml_sdk import YCloudML
from dotenv import load_dotenv
load_dotenv()

f = os.getenv("FOLDER_ID")
k = os.getenv("Y_S_K")


message = "узор из цветных пастельных суккулентов разных сортов, hd full wallpaper, четкий фокус, множество сложных деталей, глубина кадра, вид сверху"


def g():
    sdk = YCloudML(
        folder_id=f,
        auth=k,
    )

    model = sdk.models.image_generation("yandex-art")

    # configuring model
    model = model.configure(width_ratio=2, height_ratio=1, seed=1863)

    path = pathlib.Path("./image.jpeg")
    operation = model.run_deferred(message)
    result = operation.wait()
    path.write_bytes(result.image_bytes)



g()

