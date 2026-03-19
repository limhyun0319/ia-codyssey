# main.py
import sys


def read_mission_logs(file_path):
    '''
    미션 컴퓨터의 로그 파일을 읽어 화면에 출력하고, 
    시간의 역순으로 정렬한 리스트와 오류 로그를 반환합니다.
    '''
    logs = []
    try:
        # UTF-8 인코딩으로 파일 열기
        with open(file_path, 'r', encoding = 'utf-8') as file:
            # 첫 번째 줄(헤더) 제외
            header = file.readline()
            if not header:
                print('로그 파일이 비어 있습니다.')
                return
            
            print('--- 전체 로그 내용 출력 ---')
            for line in file:
                line = line.strip()
                if line:
                    print(line)
                    logs.append(line)
            print('---------------------------\n')

    except FileNotFoundError:
        print(f'오류: {file_path} 파일을 찾을 수 없습니다.')
        sys.exit(1)
    except Exception as e:
        print(f'예기치 못한 오류가 발생했습니다: {e}')
        sys.exit(1)

    return logs


def save_reverse_and_errors(logs, error_file):
    '''
    로그를 시간의 역순으로 출력하고, 
    문제가 되는 로그(WARNING, ERROR)를 별도 파일로 저장합니다.
    '''
    if not logs:
        return

    # 보너스 과제 1: 시간의 역순 정렬 출력
    print('--- 시간 역순 정렬 출력 ---')
    reversed_logs = logs[::-1]
    for log in reversed_logs:
        print(log)
    
    # 보너스 과제 2: 문제가 되는 부분만 파일로 저장
    try:
        with open(error_file, 'w', encoding = 'utf-8') as f:
            for log in logs:
                # INFO를 제외한 이벤트(WARNING, ERROR 등) 추출
                if 'INFO' not in log:
                    f.write(log + '\n')
        print(f'\n문제 로그가 {error_file}에 저장되었습니다.')
    except IOError as e:
        print(f'파일 저장 중 오류 발생: {e}')


if __name__ == '__main__':
    log_file = 'mission_computer_main.log'
    issue_file = 'problem_logs.txt'
    
    all_logs = read_mission_logs(log_file)
    save_reverse_and_errors(all_logs, issue_file)