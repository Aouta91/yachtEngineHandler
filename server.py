from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import io
from pydantic import BaseModel

from fake_boat import FakeBoat
from webcamera import WebCamera


class Item(BaseModel):
    speed: int
    angle: int
    led1: bool
    led2: bool


boat = FakeBoat()
app = FastAPI()
cam = WebCamera(0)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    page = ""
    with open("index.html") as f:
        page = f.read()
    return HTMLResponse(content=page)


@app.post("/control")
async def root(item: Item):
    boat.set_led(item.led1, 0)
    boat.set_led(item.led2, 1)
    boat.set_speed(item.speed)
    boat.set_angle(item.angle)
    return {"message": "Set: " + str(boat)}


@app.get("/telemetry")
async def root():
    response = {"speed": boat.get_speed(),
                "angle": boat.get_angle(),
                "led1": boat.get_led(0),
                "led2": boat.get_led(1)}
    return JSONResponse(content=jsonable_encoder(response))


@app.get("/camera")
async def root():
    img = cam(color_format="bgr", data_format="encoded")
    if img is not None:
        io_buf = io.BytesIO(img)
        io_buf.seek(0)
        return StreamingResponse(io_buf, media_type="image/jpeg",
                                 headers={'Content-Disposition': 'inline; filename="frame.jpg"'})
