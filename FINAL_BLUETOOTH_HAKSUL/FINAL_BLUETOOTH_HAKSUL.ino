#include <SoftwareSerial.h> // 시리얼 통신 라이브러리

// 아두이노 디지털 핀 지정
#define RXD 8  // 아두이노 디지털 8번핀 RX로 지정 (블루투스 TX와 연결)
#define TXD 7  // 아두이노 디지털 7번핀 TX로 지정 (블루투스 RX와 연결)
SoftwareSerial BTSerial(RXD, TXD); // 시리얼 통신 핀 지정

// 압력 센서 핀 번호
const int pressurePins[6] = {A0, A1, A2, A3, A4, A5};
int pressureValues[6]; // 각 센서의 압력 값을 저장할 배열

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);
  BTSerial.setTimeout(5000);
  delay(1000);

  // 압력 센서 핀 설정
  for (int i = 0; i < 6; i++) {
    pinMode(pressurePins[i], INPUT);
  }
}

void loop() {

  // 각 센서에서 압력 값 읽기
  for (int i = 0; i < 6; i++) {
    pressureValues[i] = analogRead(pressurePins[i]);
  }

  // 압력 값 블루투스로 전송  --> 결과) sensor1:200,sensor2:200.... 이런 식으로 전송함. 근데 전송 수신을 못하는딩?
  String sensorData = ""; 
  for (int i = 0; i < 6; i++) {
    sensorData += "sen" + String(i + 1) + ":" + String(pressureValues[i]) + " ";
    if (i < 5) sensorData += ",";
  }
  Serial.println(sensorData); // 시리얼 모니터에 출력
  BTSerial.println(sensorData); // 전송하는 데이터 값

  // 1000ms 간격으로 값 전송
  delay(1000);
}