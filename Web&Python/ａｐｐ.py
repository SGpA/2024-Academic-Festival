from flask import Flask, render_template, jsonify # flask 서버 구축 및, jsonify와 html 파일 사용 위해
import serial   # 시리얼 통신 위함
import threading # 블르투스 데이터 수신 및 비동기 작업 수행

app = Flask(__name__) # 웹 애플리케이션 인스턴스 생성

# 블루투스 연결 설정 (COM 포트와 보드레이트에 맞게 조정)
bluetooth = serial.Serial('COM9', 9600)  # 기기에 맞는 포트 번호, 보드레이트로 교체해야함
data_buffer = []  # 수신한 데이터를 저장할 리스트

def read_bluetooth():  
    while True:
        if bluetooth.in_waiting > 0: # 데이터 보유 시(값>0이면 데이터를 읽고 출력 및 저장)
            data = bluetooth.readline().decode('utf-8').rstrip()  # 바이트 데이터 -> uft-8 변환 -> 공백 제거 / 수신 데이터 읽기
            print("Received from Bluetooth:", data)  # 수신한 데이터 출력
            data_buffer.append(data)  # 데이터를 리스트에 저장

# 블루투스 데이터 수신 스레드 시작
threading.Thread(target=read_bluetooth, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', data=data_buffer)

@app.route('/data')
def get_data():
    # data_buffer가 비어있지 않으면 마지막 데이터를 반환
    if data_buffer:
        return jsonify(data_buffer[-1])  # JSON 형식으로 마지막 데이터 반환
    return jsonify("")  # 데이터가 없을 경우 빈 문자열 반환

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 모든 IP에서 접근 가능하도록 서버 실행
    #http://localhost:5000
