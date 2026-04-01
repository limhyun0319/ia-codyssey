import random
from datetime import datetime

class DummySensor:

    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0, #화성기지내부온도
            'mars_base_external_temperature': 0, #화성기지외부온도
            'mars_base_internal_humidity': 0, #화성기지내부습도
            'mars_base_external_illuminance': 0, #화성기지외부광량
            'mars_base_internal_co2': 0, #화성기지내부이산화탄소농도
            'mars_base_internal_oxygen': 0, #화성기지내부산소농도
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    def get_env(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = (
            f"{now}, "
            f"{self.env_values['mars_base_internal_temperature']}°C, "
            f"{self.env_values['mars_base_external_temperature']}°C, "
            f"{self.env_values['mars_base_internal_humidity']}%, "
            f"{self.env_values['mars_base_external_illuminance']}W/m2, "
            f"{self.env_values['mars_base_internal_co2']}%, "
            f"{self.env_values['mars_base_internal_oxygen']}%\n"
        )
        try:
            with open('sensor_log.txt', 'a', encoding = 'utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f'로그 기록 중 오류 발생: {e}')

        return self.env_values
    

ds = DummySensor()

ds.set_env()
data = ds.get_env()

print('---- 현재 센서 데이터 ----')
for key, value in data.items():
    print(f'{key}: {value}')
print('---------------------------------------')
print('측정값이 sensor_log.txt에 기록되었습니다.')