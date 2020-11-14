from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
import random
from pydantic import BaseModel

from gps_track import GpsTrack
from raspberryApi.boat_hardware import BoatHardware
from webcamera import WebCamera


class Item(BaseModel):
    speed: int
    angle: int
    led1: bool
    led2: bool


class MapRequest(BaseModel):
    set_home: bool
    clear_track: bool


track = GpsTrack(gps_accuracy=1e-5, track_limit=128)
boat = BoatHardware()
cam = WebCamera(0)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Это все для примера, как можно использовать шаблонизацию. Конечный вариант передаваемых параметров обсуждаем.
    return templates.TemplateResponse("index.html", {
        "request": request,
        "telemetry_url": "/telemetry",
        "control_url": "/control",
        "video_url": "/video",
        "telemetry_period": 1000,
        "angle": {"type": "range", "label": "Angle", "def": 0.0, "min": -90, "max": 90, "step": 1},
        "speed": {"type": "range", "label": "Speed", "def": 0.0, "min": -20, "max": 20, "step": 1},
        "led1": {"type": "switch", "label": "Led 1", "def": False},
        "led2": {"type": "switch", "label": "Led 2", "def": False}
    })


@app.post("/control")
async def control(item: Item):
    leds = boat.leds
    if len(leds) >= 2:
        boat.set_led(leds['led1']['pin'], item.led1)
        boat.set_led(leds['led2']['pin'], item.led2)

    boat.set_steering_wheel(item.angle)

    boat.set_speed(item.speed, 'left')
    boat.set_speed(item.speed, 'right')

    return {"message": "Set: " + str(boat)}


def gen_route(start_point):
    current = start_point
    while True:
        dx = random.random() * 0.01 - 0.005
        dy = random.random() * 0.01 - 0.005
        current = (current[0]+dx, current[1]+dy)
        yield current


point_generator = gen_route((55.82995, 37.4783))


@app.get("/telemetry")
async def telemetry():
    leds = boat.leds
    track(next(point_generator))
    curent_point = track.get_current()
    dist_to_home, dist_total = track.get_distance()
    response = {"speed": boat.motors['left']['speed'],
                "angle": boat.steering_wheel['angle'],
                "led1": leds['led1']['state'],
                "led2": leds['led2']['state'],
                "current_lat_lng": curent_point if curent_point else (55.82995, 37.4783),
                "home_lat_lng": track.get_home(),
                "route_lat_lng": track.get_track(),
                "dist_to_home": dist_to_home,
                "dist_total": dist_total}
    return JSONResponse(content=jsonable_encoder(response))


@app.post("/map")
async def map_(request: MapRequest):
    if request.set_home or request.clear_track:
        track.clear()
    response = {'ok': True}
    return JSONResponse(content=jsonable_encoder(response))


@app.get("/photo")
async def photo():
    img = cam(color_format="bgr", data_format="encoded")
    if img is not None:
        io_buf = io.BytesIO(img)
        io_buf.seek(0)
        return StreamingResponse(io_buf, media_type="image/jpeg",
                                 headers={'Content-Disposition': 'inline; filename="frame.jpg"'})


def gen_stream(camera):
    while True:
        frame = camera(color_format="bgr", data_format="encoded")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


@app.get('/video')
async def video():
    return StreamingResponse(gen_stream(cam), media_type='multipart/x-mixed-replace; boundary=frame')
