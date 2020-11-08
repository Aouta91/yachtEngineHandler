# Схема

![Alt text](staff/schema.bmp?raw=true "Title")
    
    En1 - бесколлекторный двигатель 1;
    En2 - бесколлекторный двигатель 2;
    D1 -  драйвер для En1;
    D2 -  драйвер для En2;
    PI - raspberry Pi
    
# prepare
```bash
pip3 install -r requirements.txt
```

# run

```bash
sh ./run_server.py
```

# TODO
:black_square_button: 1) Модернизировать скрипт, чтобы в index.html добавлялись координаты
:black_square_button: 2) Определиться с подключением GPS
:black_square_button: 3) Попробовать переделать фронтенд на что-то рендарящее html фрагменты типа jquery или react:
