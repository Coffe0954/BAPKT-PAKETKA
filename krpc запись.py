import krpc
import json
import time
import traceback

try:
    conn = krpc.connect(name='Atmospheric Data Logger')
    vessel = conn.space_center.active_vessel
    body = vessel.orbit.body
    flight = vessel.flight()

    sampling_interval = 1  # Initial sampling interval (seconds) - will be adjusted
    atmospheric_pressure_data = {}
    air_density_data = {}
    start_time = time.time()
    last_recorded_altitude_km = -1  # Initialize to a value outside the range

    print("Начало сбора данных...")
    print(f"Текущее положение: {vessel.position}")

    atmosphere_depth = body.atmosphere_depth

    try:
        while True:
            altitude = flight.surface_altitude
            altitude_km = altitude / 1000
            print(f"Текущая высота: {altitude:.2f} м ({altitude_km:.2f} км)")

            if altitude < 0 or altitude > atmosphere_depth:
                time.sleep(sampling_interval)
                continue

            # Record data only when altitude changes by at least 1 km
            if abs(altitude_km - last_recorded_altitude_km) >= 1:
                air_density = flight.atmosphere_density
                atm_pressure = flight.static_pressure

                if air_density is not None and atm_pressure is not None:
                    atmospheric_pressure_data[altitude] = atm_pressure
                    air_density_data[altitude] = air_density
                    print(f"Высота: {altitude:.2f} м, Плотность: {air_density} кг/м³, Давление: {atm_pressure} Па")
                    last_recorded_altitude_km = altitude_km  # update last recorded altitude
                else:
                    print(f"Ошибка: плотность или давление равны None на высоте {altitude}")


            time.sleep(sampling_interval)
            if altitude < 150:  # прерываем сбор на высоте больше 10000 метров
                break
    except krpc.error.RPCError as e:
        print(f"KRPC Error: {e}")
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")
        traceback.print_exc()

    end_time = time.time()
    elapsed_time = end_time - start_time

    try:
        with open('flight_atmosphere_pressure.json', 'w', encoding='utf-8') as f:
            json.dump(atmospheric_pressure_data, f, indent=4, ensure_ascii=False)
        print("\nДанные о давлении сохранены в flight_atmosphere_pressure.json")
    except Exception as e:
        print(f"\nОшибка при записи в flight_atmosphere_pressure.json: {e}")
        traceback.print_exc()

    try:
        with open('flight_atmosphere_density.json', 'w', encoding='utf-8') as f:
            json.dump(air_density_data, f, indent=4, ensure_ascii=False)
        print("Данные о плотности сохранены в flight_atmosphere_density.json")
    except Exception as e:
        print(f"\nОшибка при записи в flight_atmosphere_density.json: {e}")
        traceback.print_exc()

    print(f"Время сбора данных: {elapsed_time:.2f} сек")

except Exception as e:
    print(f"\nПроизошла глобальная ошибка: {e}")
    traceback.print_exc()
finally:
    if 'conn' in locals():
        conn.close()