import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 데이터 리스트 텍스트 파일 읽어오기
file_path = 'data_list.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

data_list = [line.strip() for line in lines]


csv_file = pd.read_csv('CSV-example.csv')

# 데이터를 저장할 데이터프레임 생성
result_df = pd.DataFrame({'200-LOAD': csv_file['200-LOAD']})

for data in data_list:
    y = csv_file['200-LOAD']
    x = csv_file[data]

    # 그래프 생성
    fig, ax = plt.subplots()
    ax.plot(x, y, '-o')
    ax.set_title(data)
    
    # 초기 상태 저장 (클릭 취소용)
    initial_x = x.copy()
    initial_y = y.copy()

    # 클릭 이벤트 처리 함수 정의
    def on_click(event):
        global x, y  # 클로저에서 x, y 변수 변경을 위해 nonlocal 선언

        if event.button == 1:  # 좌클릭 버튼인 경우
            # 클릭한 지점의 좌표 가져오기
            clicked_x = event.xdata
            clicked_y = event.ydata

            # 클릭한 데이터의 인덱스 찾기 (일정한 오차 범위 내에서)
            data_index = np.argwhere(np.isclose(x, clicked_x, atol=0.15))

            if data_index.size > 0:
                data_index = data_index[0, 0]

                # 클릭한 데이터를 포함한 새로운 x와 y 배열 생성
                new_x = x[:data_index]
                new_y = y[:data_index]

                # 그래프 업데이트
                ax.clear()  # 현재 그래프 지우기
                ax.plot(new_x, new_y, '-o')  # 새로운 그래프 그리기
                ax.set_title(data)
                fig.canvas.draw()

                # 클릭한 데이터 이후의 데이터 제거
                x = new_x
                y = new_y

    # 클릭 이벤트 핸들러 등록
    fig.canvas.mpl_connect('button_press_event', on_click)

    # 'z' 키를 누를 때 초기 상태로 복원하고 데이터프레임에 데이터 추가
    def on_key(event):
        global x, y  # 클로저에서 x, y 변수 변경을 위해 nonlocal 선언
        
        if event.key == 'z':  # 'z' 키가 눌린 경우
            # 초기 상태로 복원
            x = initial_x.copy()
            y = initial_y.copy()
            
            # 그래프 업데이트
            ax.clear()  # 현재 그래프 지우기
            ax.plot(x, y, '-o')  # 초기 그래프로 복원
            ax.set_title(data)
            fig.canvas.draw()
        
        if event.key == 'c':
            global result_df
            result_df[data] = x
            plt.close(fig)  # 현재 그래프 창 닫기
            return True

    # 키 이벤트 핸들러 등록
    fig.canvas.mpl_connect('key_press_event', on_key)

    # 그래프 표시
    plt.show()


# 결과 데이터프레임을 엑셀 파일로 저장
result_df.to_excel('2122.xlsx', index=False)
