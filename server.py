from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from fake_boat import FakeBoat


class Item(BaseModel):
    speed: int
    angle: int
    led1: bool
    led2: bool


boat = FakeBoat()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    page = ""
    with open("index.html") as f:
        page = f.read()
    return HTMLResponse(content=page)


@app.post("/control")
async def root(item: Item):
    data = item
    boat.set_led(data.led1, 0)
    boat.set_led(data.led2, 1)
    boat.set_speed(data.speed)
    boat.set_angle(data.angle)
    return {"message": "Set: "+str(boat)}


@app.get("/telemetry")
async def root():
    response = {"speed": boat.get_speed(),
                "angle": boat.get_angle(),
                "led1": boat.get_led(0),
                "led2": boat.get_led(1)}
    print("sending telemetry: ", response)
    return JSONResponse(content=jsonable_encoder(response))
