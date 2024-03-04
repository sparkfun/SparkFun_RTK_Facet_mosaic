/*
  SparkFun RTK Facet mosaic Test Sketch

  This sketch can be used to test mosaic PPS and EventA
  * Upload the sketch
  * Connect Data Connector TX pin to RX pin - this connects PPS to EventA
  * If desired, monitor PPS with a logic analyzer
  * Open RxTools: RxControl; Tools; Expert Console; ExEvent
  * Check EventA seen at 1Hz with incrementing ToW

  Select ESP32 Wrover Module as the board

  License: MIT. Please see LICENSE.md for more details

  ESP32-WROVER-E Pin Allocations:
  D0  : Boot
  D1  : Serial TX (CH340 RX)
  D2  : 
  D3  : Serial RX (CH340 TX)
  D4  : Serial1 RX - Connected to mosaic-X5 COM4 TX
  D5  : 
  D12 : 
  D13 : Serial2 RX - Connected to mosaic-X5 COM1 TX
  D14 : Serial2 TX - Connected to mosaic-X5 COM1 TX
  D15 : 
  D16 : N/A
  D17 : N/A
  D18 : Mux A
  D19 : Mux B
  D21 : I2C SDA
  D22 : I2C SCL
  D23 : mosaic On Off
  D25 : Serial1 TX - Connected to mosaic-X5 COM4 RX
  D26 : DAC (via Mux)
  D27 : Peripheral Power
  D32 : Power Control
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

const int muxA = 18; // 74HC4052 Multiplexer. Note: this will move to pin 2 on the next PCB rev
const int muxB = 19; // 74HC4052 Multiplexer. Note: this will move to pin 12 on the next PCB rev
const int SDA_1 = 21;
const int SCL_1 = 22;
const int mosaicOnOff = 23; // Drive low for >= 50ms to toggle from on to off and vice versa
const int muxDAC = 26; // Analog out - via multiplexer
const int peripheralPower = 27; // Pull high to enable power for the mosaic-X5, microSD, multiplexer and main board Qwiic connector
const int powerControl = 32; // Default to input pull-up. Low indicates power button is being held. Change to output and drive low for power off
const int fastOff = 33; // Default to input. Change to output and drive low for fast power off
const int chargeLED = 34; // Connected to charger STAT1
const int mosaicReady = 36; // High when module is ready
const int muxADC = 39; // Analog in - via multiplexer

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

void setup()
{
  // Init pins
  pinMode(muxA, OUTPUT); // Set Mux to mosaic PPS & EventA
  digitalWrite(muxA, HIGH);
  pinMode(muxB, OUTPUT);
  digitalWrite(muxB, LOW);

  pinMode(mosaicOnOff, OUTPUT); // Pull On/Off high
  digitalWrite(mosaicOnOff, HIGH);

  pinMode(powerControl, INPUT_PULLUP);
  pinMode(fastOff, INPUT);

  pinMode(mosaicReady, INPUT);

  pinMode(peripheralPower, OUTPUT); // Now enable power for the mosaic-X5
  digitalWrite(peripheralPower, HIGH);


  delay(1000);

  Serial.begin(115200);
  Serial.println("SparkFun RTK mosaic - Test Sketch");
}

void loop()
{
}
