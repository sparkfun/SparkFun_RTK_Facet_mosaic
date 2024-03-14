/*
  SparkFun RTK Facet mosaic Test Sketch

  This sketch will turn the board off via the Fast Off pin if Power Control is not low at start-up.
  It also monitors the Power Control pin and will turn the soft power circuit off if the button is
  held for 2 seconds.
  It also displays information from the fuel gauge and the status of the charger STAT1 pin.

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

#include <Wire.h> // Needed for I2C

TwoWire I2C_1 = TwoWire(1);

#include <SparkFun_MAX1704x_Fuel_Gauge_Arduino_Library.h> // Click here to get the library: http://librarymanager/All#SparkFun_MAX1704x_Fuel_Gauge_Arduino_Library

SFE_MAX1704X lipo(MAX1704X_MAX17048); // Create a MAX17048

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Hardware specifics for the SparkFun RTK mosaic

#include <driver/uart.h>      //Required for uart_set_rx_full_threshold() on cores <v2.0.5
const int serialTxPin = 14;
const int serialRxPin = 13;
HardwareSerial serialGNSS(2); // UART2: TX on 14, RX on 13. Connected to mosaic-X5 COM1
const int lbandRxPin = 4;
const int lbandTxPin = 25;
HardwareSerial lbandSerial(1);  // UART1: TX on 25, RX on 4. Connected to mosaic-X5 COM4

const int serial2Tx = 14;
const int muxA = 18; // 74HC4052 Multiplexer. Note: this will move to pin 2 on the next PCB rev
const int muxB = 19; // 74HC4052 Multiplexer. Note: this will move to pin 12 on the next PCB rev
const int SDA_1 = 21;
const int SCL_1 = 22;
const int mosaicOnOff = 23; // Drive low for >= 50ms to toggle from on to off and vice versa
const int serial1Tx = 25;
const int muxDAC = 26; // Analog out - via multiplexer
const int peripheralPower = 27; // Pull high to enable power for the mosaic-X5, microSD, multiplexer and main board Qwiic connector
const int powerControl = 32; // Default to input pull-up. Low indicates power button is being held. Change to output and drive low for power off
const int fastOff = 33; // Default to input. Change to output and drive low for fast power off
const int chargeLED = 34; // Connected to charger STAT1
const int mosaicReady = 36; // High when module is ready
const int muxADC = 39; // Analog in - via multiplexer

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

void flushRX(unsigned long timeout = 0); // Header
void flushRX(unsigned long timeout)
{
  if (timeout > 0)
  {
    unsigned long startTime = millis();
    while (millis() < (startTime + timeout))
      if (serialGNSS.available())
        serialGNSS.read();
  }
  else
  {
    while (serialGNSS.available())
      serialGNSS.read();
  }
}

bool sendWithResponse(const char *message, const char *reply, unsigned long timeout = 1000, unsigned long wait = 100); // Header
bool sendWithResponse(const char *message, const char *reply, unsigned long timeout, unsigned long wait)
{
  if (strlen(reply) == 0) // Reply can't be zero-length
    return false;

  if (strlen(message) > 0)
    serialGNSS.write(message, strlen(message)); // Send the message

  unsigned long startTime = millis();
  size_t replySeen = 0;
  bool keepGoing = true;

  while ((keepGoing) && (replySeen < strlen(reply))) // While not timed out and reply not seen
  {
    if (serialGNSS.available()) // If a char is available
    {
      uint8_t chr = serialGNSS.read(); // Read it
      if (chr == *(reply + replySeen)) // Is it a char from reply?
        replySeen++;
      else
        replySeen = 0; // Reset replySeen on an unexpected char
    }

    // If the reply has started to arrive at the timeout, allow extra time
    if (millis() > (startTime + timeout)) // Have we timed out?
      if (replySeen == 0)                 // If replySeen is zero, don't keepGoing
        keepGoing = false;

    if (millis() > (startTime + timeout + wait)) // Have we really timed out?
      keepGoing = false;                         // Don't keepGoing
  }

  if (replySeen == strlen(reply)) // If the reply was seen
  {
    flushRX(wait); // wait and flush
    return true;
  }

  return false;
}

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Put the X5 into standby

bool x5Standby(int reattempts) // Zero reattempts == one attempt
{
  if (reattempts == 0)
    return sendWithResponse("epwm, standby\n\r", "PowerMode");

  int attempt = 0;

  while (!sendWithResponse("epwm, standby\n\r", "PowerMode") && (attempt <= reattempts))
  {
    if (attempt < reattempts) // Don't send the escape on the final try
    {
      Serial.println(F("No response from mosaic-X5. Retrying - with escape sequence..."));
      sendWithResponse("SSSSSSSSSSSSSSSSSSSS\n\r", "COM2>"); // Send escape sequence
    }
    attempt++;
  }

  return (attempt <= reattempts);
}

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Power Down

void powerDown(void)
{
  // Tell the X5 to standby
  x5Standby(1); // Allow one retry

  delay(100);

  pinMode(peripheralPower, OUTPUT); // Power off the X5
  digitalWrite(peripheralPower, LOW);
  
  pinMode(fastOff, OUTPUT); // Power off the soft power switch
  digitalWrite(fastOff, LOW);

  pinMode(powerControl, OUTPUT);
  digitalWrite(powerControl, LOW);

  while(1);
}

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Buttons - Interrupt driven and debounce

#include <JC_Button.h>      //http://librarymanager/All#JC_Button v2.1.2
Button *powerBtn = nullptr;

TaskHandle_t ButtonCheckTaskHandle = nullptr;
const uint8_t ButtonCheckTaskPriority = 1; // 3 being the highest, and 0 being the lowest
const int buttonTaskStackSize = 2000;

const int shutDownButtonTime = 2000;      // ms press and hold before shutdown

// Monitor Power Control button
void ButtonCheckTask(void *e)
{
  if (powerBtn != nullptr)
      powerBtn->begin();

  while (true)
  {
    if (powerBtn != nullptr)
        powerBtn->read();

    if (powerBtn != nullptr && powerBtn->pressedFor(shutDownButtonTime))
    {
      // Power down
      powerDown();
    }

    delay(1); // Poor man's way of feeding WDT. Required to prevent Priority 1 tasks from causing WDT reset
    taskYIELD();
  }
}

//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

void setup()
{
  // Init pins
  pinMode(muxA, OUTPUT); // Set Mux to mosaic COM3
  digitalWrite(muxA, LOW);
  pinMode(muxB, OUTPUT);
  digitalWrite(muxB, LOW);

  pinMode(mosaicOnOff, INPUT_PULLUP); // Pull On/Off high using a pull-up, so we can short to GND if needed

  pinMode(powerControl, INPUT_PULLUP);
  pinMode(fastOff, INPUT);

  pinMode(mosaicReady, INPUT);

  pinMode(chargeLED, INPUT);

  pinMode(serial1Tx, INPUT_PULLUP); // Not needed. Pull up
  pinMode(serial2Tx, INPUT_PULLUP); // Not needed. Pull up

  pinMode(peripheralPower, OUTPUT); // Enable power for the X5
  digitalWrite(peripheralPower, HIGH);

  I2C_1.begin((int)SDA_1, (int)SCL_1, (uint32_t)400000); // Begin I2C

  delay(350); // Wait for the X5 to start up

  serialGNSS.begin(115200, SERIAL_8N1, serialRxPin, serialTxPin); // UART2 on pins 16/17.

  delay(650);

  Serial.begin(115200);
  Serial.println("SparkFun RTK mosaic - Test Sketch");

  // Check if the power button is _not_ being held
  if (digitalRead(powerControl) == HIGH)
  {
    Serial.println("Button not held. Powering off...");
    Serial.flush();
    powerDown();
  }

  // Now start our button task
  powerBtn = new Button(powerControl); // Create a Power Button object

  // Start a task for monitoring button presses
  if (ButtonCheckTaskHandle == nullptr)
      xTaskCreate(ButtonCheckTask,
                  "BtnCheck",          // Just for humans
                  buttonTaskStackSize, // Stack Size
                  nullptr,             // Task input parameter
                  ButtonCheckTaskPriority,
                  &ButtonCheckTaskHandle); // Task handle

  // Set up the MAX17048 LiPo fuel gauge:
  if (lipo.begin(I2C_1) == false) // Connect to the MAX17048
  {
    Serial.println(F("MAX17048 not detected. Please check wiring. Freezing."));
    while (1)
      ;
  }

}

void loop()
{
  // lipo.getVoltage() returns a voltage value (e.g. 3.93)
  double voltage = lipo.getVoltage();
  // lipo.getSOC() returns the estimated state of charge (e.g. 79%)
  double soc = lipo.getSOC();

  // Print the variables:
  Serial.print("Voltage: ");
  Serial.print(voltage);  // Print the battery voltage
  Serial.print("V");

  Serial.print("  SOC: ");
  Serial.print(soc); // Print the battery state of charge
  Serial.print("%");

  Serial.print("  STAT1: ");
  Serial.println(digitalRead(chargeLED)); // Print the state of STAT1 (Charge LED)

  delay(250);
}
