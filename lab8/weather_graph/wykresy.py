import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import PySide6

def get_data():
    latitude = 51.25
    longitude = 22.57

    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&daily=sunrise,sunset"
        f"&hourly=temperature_2m,apparent_temperature,precipitation"
        f"&start_date={start_date}&end_date={end_date}"
        f"&timezone=Europe/Warsaw"
    )

    response = requests.get(url)
    data = response.json()
    return data["hourly"], data["daily"]

    # print(data["daily"])
    # print(data["hourly"])

def draw_line(data):
    # tabx = []
    # for i in range(len(data["temperature_2m"])):
    #     tabx.append(i)

    hourly, daily = data
    format = "%Y-%m-%dT%H:%M"
    hours = [datetime.strptime(i, format) for i in hourly["time"]]
    temp_fig, (temp_ax) = plt.subplots(1, 1, figsize=(6, 4), sharex=True, dpi = 300)
    rain_fig, rain_ax = plt.subplots(1, 1, figsize=(6, 4), sharex=True, dpi=300)
    # plt.figure(figsize=(6,4))
    for time, sunrise, sunset in zip(daily["time"], daily["sunrise"], daily["sunset"]):
        midnight = datetime.strptime(time, "%Y-%m-%d")
        sunrise = datetime.strptime(sunrise, format)
        sunset = datetime.strptime(sunset, format)
        temp_ax.axvspan(sunrise, sunset, color="yellow")
        temp_ax.axvspan(midnight, sunrise, color="black", alpha=0.1)
        temp_ax.axvspan(sunset, midnight + timedelta(days=1), color="black", alpha=0.1)
    temp_ax.plot(hours, hourly["temperature_2m"], label="temperatura", color="red")
    temp_ax.plot(hours, hourly["apparent_temperature"], label="temperatura odczuwalna")
    rain_ax.bar(hours, hourly["precipitation"])
    for ax in [temp_ax, rain_ax]:
        ax.grid()
        ax.set_xlabel("Czas")
    temp_ax.set_ylabel("Temperatura")
    temp_ax.legend()

    rain_ax.set_ylabel("Wysokosc opadow")

    plt.title("wykres")
    temp_ax.tick_params(axis="x",labelrotation = 45)
    rain_ax.tick_params(axis="x",labelrotation = 45)

    # plt.show()
    temp_fig.savefig("temp.png")
    rain_fig.savefig("rain.png")

if __name__ == '__main__':
    data = get_data()
    draw_line(data)