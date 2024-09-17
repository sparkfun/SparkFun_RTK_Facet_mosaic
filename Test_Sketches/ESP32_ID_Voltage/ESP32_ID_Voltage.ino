/*
  SparkFun RTK Facet mosaic Test Sketch

  This sketch reads the voltage on the Board Detect / Device ID pin

  Select ESP32 Wrover Module as the board

  License: MIT. Please see LICENSE.md for more details

  ESP32-WROVER-E Pin Allocations:
  D0  : Boot
  D1  : Serial TX (CH340 RX)
  D2  : Mux A
  D3  : Serial RX (CH340 TX)
  D4  : Serial1 RX - Connected to mosaic-X5 COM4 TX
  D5  : N/C
  D12 : Mux B
  D13 : Serial2 RX - Connected to mosaic-X5 COM1 TX
  D14 : Serial2 TX - Connected to mosaic-X5 COM1 RX
  D15 : N/C
  D16 : N/A
  D17 : N/A
  D18 : GNSS Event - Connected to mosaic-X5 EventB
  D19 : Charger STAT2
  D21 : I2C SDA
  D22 : I2C SCL
  D23 : mosaic On Off
  D25 : Serial1 TX - Connected to mosaic-X5 COM4 RX
  D26 : DAC (via Mux)
  D27 : Peripheral Power Control
  D32 : Power Sense & Control
  D33 : Fast Off
  A34 : Charger STAT1 - Charge LED
  A35 : Board Detect (2.72V)
  A36 : mosaic Ready
  A39 : ADC (via Mux)

  NMEA / Data Multiplexer:
  B A : Mode
  0 0 : mosaic-X5 COM3 TX & RX
  0 1 : PPS & EventA
  1 0 : SCL & SDA
  1 1 : DAC (26) & ADC (39)

*/

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Hardware specifics for the SparkFun RTK mosaic

#include <driver/uart.h>      //Required for uart_set_rx_full_threshold() on cores <v2.0.5
const int serialTxPin = 14;
const int serialRxPin = 13;
HardwareSerial serialGNSS(2); // UART2: TX on 14, RX on 13. Connected to mosaic-X5 COM1
const int lbandRxPin = 4;
const int lbandTxPin = 25;
HardwareSerial lbandSerial(1);  // UART1: TX on 25, RX on 4. Connected to mosaic-X5 COM4

const int muxA = 2; // 74HC4052 Multiplexer
const int muxB = 12; // 74HC4052 Multiplexer
const int SDA_1 = 21;
const int SCL_1 = 22;
const int mosaicOnOff = 23; // Drive low for >= 50ms to toggle from on to off and vice versa
const int muxDAC = 26; // Analog out - via multiplexer
const int peripheralPower = 27; // Pull high to enable power for the mosaic-X5, microSD, multiplexer and main board Qwiic connector
const int powerControl = 32; // Default to input pull-up. Low indicates power button is being held
const int fastOff = 33; // Default to input. Change to output and drive high for fast power off
const int chargeLED = 34; // Connected to charger STAT1
const int boardDetect = 35; // Should be 2.72V
const int mosaicReady = 36; // High when module is ready
const int muxADC = 39; // Analog in - via multiplexer

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

void setup()
{
  // Init pins
  pinMode(muxA, OUTPUT); // Set Mux to DAC and ADC
  digitalWrite(muxA, HIGH);
  pinMode(muxB, OUTPUT);
  digitalWrite(muxB, HIGH);

  pinMode(mosaicOnOff, OUTPUT); // Pull On/Off high
  digitalWrite(mosaicOnOff, HIGH);

  pinMode(powerControl, INPUT_PULLUP);
  pinMode(fastOff, INPUT);

  pinMode(mosaicReady, INPUT);

  pinMode(peripheralPower, OUTPUT); // Now enable power for the mosaic-X5
  digitalWrite(peripheralPower, HIGH);

  pinMode(boardDetect, INPUT);

  delay(1000);

  Serial.begin(115200);
  Serial.println("SparkFun RTK mosaic - Test Sketch");
}

void loop()
{
  float id = analogRead(boardDetect);
  id /= 4095.0;
  id *= 3.3;

  Serial.print("ID Voltage is ");
  Serial.println(id, 2);

  delay(100);
}
