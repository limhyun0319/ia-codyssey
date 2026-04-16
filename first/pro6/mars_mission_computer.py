import random
from datetime import datetime
import time
import json
import platform
import os

# 외부 라이브러리 예외 처리 (설치되지 않았을 경우를 대비)
try:
    import psutil
except ImportError:
    print('경고: psutil 라이브러리가 설치되지 않았습니다. 터미널에서 pip install psutil을 실행해주세요.')

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
    

class MissionComputer:
    '''
    미션 컴퓨터의 센서 데이터를 수집하고, 시스템 상태 및 부하를 모니터링하는 클래스입니다.
    '''
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        # DummySensor 클래스를 ds라는 이름으로 인스턴스화
        self.ds = DummySensor()
        
        # 보너스 과제: 5분 평균 계산을 위한 데이터 누적 리스트 초기화
        self.history_values = {key: [] for key in self.env_values.keys()}
        self.loop_count = 0

        # 문제8 보너스과제: setting.txt에서 필터링할 항목 불러오기
        self.display_settings = self.load_settings()

    def load_settings(self):
        '''setting.txt 파일을 읽어 출력할 키(항목) 리스트를 반환합니다.'''
        settings = []
        try:
            with open('setting.txt', 'r', encoding = 'utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        settings.append(line)
        except FileNotFoundError:
            # 설정 파일이 없으면 빈 리스트 반환 (모두 출력)
            pass
        return settings
    
    def filter_data(self, data):
        '''display_settings에 정의된 항목만 필터링하여 반환합니다.'''
        if not self.display_settings:
            return data
        
        filtered = {}
        for key, value in data.items():
            if key in self.display_settings:
                filtered[key] = value
        return filtered

    def get_mission_computer_info(self):
        '''미션 컴퓨터의 기본 시스템 정보를 가져와 JSON으로 출력합니다.'''
        sys_info = {}
        try:
            sys_info['os'] = platform.system()
            sys_info['os_version'] = platform.version()
            sys_info['cpu_type'] = platform.processor()
            sys_info['cpu_cores'] = os.cpu_count()
            
            # psutil을 사용하여 메모리 크기 추출 (GB 단위 변환)
            mem = psutil.virtual_memory()
            sys_info['memory_size_gb'] = round(mem.total / (1024 ** 3), 2)
        except Exception as e:
            print(f'시스템 정보를 가져오는 중 예기치 못한 오류가 발생했습니다: {e}')

        filtered_info = self.filter_data(sys_info)
        print('\n--- [미션 컴퓨터 시스템 정보] ---')
        print(json.dumps(filtered_info, ensure_ascii = False, indent = 4))
        
        return filtered_info

    def get_mission_computer_load(self):
        '''미션 컴퓨터의 실시간 CPU 및 메모리 부하를 가져와 JSON으로 출력합니다.'''
        load_info = {}
        try:
            # interval=1을 주어 1초 동안의 CPU 사용률을 정확히 측정합니다.
            load_info['cpu_usage_percent'] = psutil.cpu_percent(interval = 1.0)
            mem = psutil.virtual_memory()
            load_info['memory_usage_percent'] = mem.percent
        except Exception as e:
            print(f'시스템 부하를 측정하는 중 예기치 못한 오류가 발생했습니다: {e}')

        filtered_load = self.filter_data(load_info)
        print('\n--- [미션 컴퓨터 실시간 부하 상태] ---')
        print(json.dumps(filtered_load, ensure_ascii = False, indent = 4))
        
        return filtered_load

    def get_sensor_data(self):
        '''
        5초마다 센서 데이터를 가져와 JSON 형태로 출력하고, 5분마다 평균을 계산합니다.
        특정 키(Ctrl+C) 입력 시 작동을 멈춥니다.
        '''
        print('미션 컴퓨터가 가동되었습니다. (종료하려면 Ctrl+C를 누르세요)\n')
        
        try:
            while True:
                # 1. 센서의 값을 가져와서(set_env 후 get_env) env_values에 담는다.
                self.ds.set_env()
                sensor_data = self.ds.get_env()
                self.env_values.update(sensor_data)

                # 5분 평균 계산을 위해 현재 값을 history에 누적
                for key, value in self.env_values.items():
                    self.history_values[key].append(value)

                # 2. env_values의 값을 json 형태로 화면에 출력한다.
                # json.dumps를 사용하여 사전 객체를 JSON 문자열로 변환합니다.
                json_output = json.dumps(self.env_values, ensure_ascii = False, indent = 4)
                print(f'[현재 센서 데이터]\n{json_output}\n')

                # 보너스 과제: 5분에 한 번씩(5초 x 60번 = 300초 = 5분) 평균값 출력
                self.loop_count += 1
                if self.loop_count == 60:
                    print('=' * 40)
                    print('--- [알림] 최근 5분 환경 데이터 평균 ---')
                    avg_data = {}
                    for key, values in self.history_values.items():
                        # 평균 계산 후 소수점 3자리까지 반올림
                        avg = sum(values) / len(values)
                        avg_data[key] = round(avg, 3)
                    
                    print(json.dumps(avg_data, ensure_ascii = False, indent = 4))
                    print('=' * 40 + '\n')
                    
                    # 평균 출력 후 다음 5분을 위해 기록과 카운트 초기화
                    self.history_values = {k: [] for k in self.env_values.keys()}
                    self.loop_count = 0

                # 3. 위의 두 가지 동작을 5초에 한 번씩 반복한다.
                time.sleep(5)

        except KeyboardInterrupt:
            # 보너스 과제: 특정 키(Ctrl+C) 입력 시 출력 중단 및 메시지 출력
            print('\nSytem stoped....')

if __name__ == '__main__':
    runComputer = MissionComputer()

    runComputer.get_mission_computer_info() #시스템 기본 정보 출력
    runComputer.get_mission_computer_load() #실시간 시스템 부하 출력
    runComputer.get_sensor_data()   #센서 데이터 모니터링