#/src/sound/pik.py
#from pyaudio import PyAudio, paFloat32
#from numpy import pi,sin,linspace,float32

def pik(frequency=6000.0,  volume=0.25,duration=0.05, sample_rate=44100):
    return
    # Генерируем сигнал с заданными параметрами
    t = linspace(0, duration, int(duration * sample_rate), endpoint=False)
    signal = volume * sin(2 * pi * frequency * t)

    # Создаем PyAudio объект
    p = PyAudio()

    # Открываем звуковое устройство для воспроизведения
    stream = p.open(format=paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # Воспроизводим сигнал
    stream.write(signal.astype(float32).tobytes())

    # Закрываем звуковое устройство и PyAudio объект
    stream.stop_stream()
    stream.close()
    p.terminate()
