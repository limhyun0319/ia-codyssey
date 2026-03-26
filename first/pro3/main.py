import csv
import pickle

def read_file_and_list(file_path):
    data_list = []

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            content = file.read()
            print('---- 파일 전채 내용 출력 ----')
            print(content)

            file.seek(0)
            reader = csv.reader(file)
            for row in reader:
                data_list.append(row)
        return data_list

    except FileNotFoundError:
        print(f"에러: '{file_path}' 파일을 찾을 수 없습니다.")
    except PermissionError:
        print(f"에러: '{file_path}' 파일에 접근할 권한이 없습니다.")
    except Exception as e:
        print(f'알 수 없는 에러가 발생했습니다: {e}')
    
    return []

def process_danger_items(list, output_path):
    header = list[0]
    rows = list[1:]

    try:
        rows.sort(key=lambda x: float(x[-1]), reverse=True)

        danger_list = [row for row in rows if float(row[-1]) >= 0.7]

        print('---- 인화성 0.7 이상 목록 (높은순) ----')
        for item in danger_list:
            print(item)
        
        with open(output_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(danger_list)
        print(f"\n성공: '{output_path}' 파일 저장 완료.")

        return danger_list
    
    except Exception as e:
        print(f'처리 중 에러 발생: {e}')
    
    return []

def binary_file(list, file_path):
    rows = list[1:]
    try:
        rows.sort(key=lambda x: float(x[-1]), reverse=True)
        with open(file_path, 'wb') as f:
            pickle.dump(rows, f)
        print(f"성공: '{file_path}'에 이진 데이터 저장 완료.")
    except Exception as e:
        print(f'이진 저장 중 에러 발생: {e}')

def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            print('---- 이진 파일 출력 ----')
            print(content)
    except FileNotFoundError:
        print(f"에러: '{file_path}' 파일을 찾을 수 없습니다.")
    except PermissionError:
        print(f"에러: '{file_path}' 파일에 접근할 권한이 없습니다.")
    except Exception as e:
        print(f'알 수 없는 에러가 발생했습니다: {e}')



if __name__ == '__main__':
    file_path = 'Mars_Base_Inventory_List.csv'
    danger = 'Mars_Base_Inventory_danger.csv'
    binary = 'Mars_Base_Inventory_danger.bin'

    list_file = read_file_and_list(file_path)
    danger_list = process_danger_items(list_file, danger)
    binary_file(list_file, binary)
    read_binary_file(binary)
