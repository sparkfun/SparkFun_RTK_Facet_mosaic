/*
  SparkFun RTK Facet mosaic Test Sketch

  This sketch can be used to test I2C / OLED connectivity:
  * The micro OLED on the Display Board
  * A micro OLED connected to the Connector Board Data connector (TX = SCL, RX = SDA)
  * A micro OLED connected to the Connector Board Qwiic connector
  * A micro OLED connected to the Main Board Qwiic connector

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

#include <SparkFun_Qwiic_OLED.h> //http://librarymanager/All#SparkFun_Qwiic_OLED
QwiicMicroOLED myOLED; // 64x48

TwoWire I2C_1 = TwoWire(1);

int width;
int height;

void setup()
{
  // Init pins
  pinMode(muxA, OUTPUT); // Set Mux to I2C - test Data Connector with a micro OLED
  digitalWrite(muxA, LOW);
  pinMode(muxB, OUTPUT);
  digitalWrite(muxB, HIGH);

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

  I2C_1.begin((int)SDA_1, (int)SCL_1, (uint32_t)400000);

  // Initalize the OLED device and related graphics system
  if (myOLED.begin(I2C_1) == false)
  {
      Serial.println("OLED begin failed. Freezing...");
      while (true)
          ;
  }

  width = myOLED.getWidth();
  height = myOLED.getHeight();
}

void loop()
{
    pixelExample();
    lineExample();
    shapeExample();
}

void pixelExample()
{
    myOLED.erase();
    for (int i = 0; i < 512; i++)
    {
        myOLED.pixel(random(width), random(height));
        myOLED.display();
        delay(10);
    }
}

void lineExample()
{
    int middleX = width / 2;
    int middleY = height / 2;
    int xEnd, yEnd;
    int lineWidth = min(middleX, middleY);

    myOLED.erase();
    int deg;

    for (int i = 0; i < 3; i++)
    {

        for (deg = 0; deg < 360; deg += 15)
        {

            xEnd = lineWidth * cos(deg * PI / 180.0);
            yEnd = lineWidth * sin(deg * PI / 180.0);

            myOLED.line(middleX, middleY, middleX + xEnd, middleY + yEnd);
            myOLED.display();
            delay(10);
        }

        for (deg = 0; deg < 360; deg += 15)
        {

            xEnd = lineWidth * cos(deg * PI / 180.0);
            yEnd = lineWidth * sin(deg * PI / 180.0);

            myOLED.line(middleX, middleY, middleX + xEnd, middleY + yEnd, 0);
            myOLED.display();
            delay(10);
        }
    }
}

void shapeExample()
{
    // Silly pong demo. It takes a lot of work to fake pong...
    int paddleW = 3;  // Paddle width
    int paddleH = 15; // Paddle height

    // Paddle 0 (left) position coordinates
    int paddle0_Y = (height / 2) - (paddleH / 2);
    int paddle0_X = 2;

    // Paddle 1 (right) position coordinates
    int paddle1_Y = (height / 2) - (paddleH / 2);
    int paddle1_X = width - 3 - paddleW;
    int ball_rad = 4; // Ball radius

    // Ball position coordinates
    int ball_X = paddle0_X + paddleW + ball_rad;
    int ball_Y = random(1 + ball_rad, height - ball_rad); // paddle0_Y + ball_rad;
    int ballVelocityX = 1;                                // Ball left/right velocity
    int ballVelocityY = 1;                                // Ball up/down velocity
    int paddle0Velocity = -1;                             // Paddle 0 velocity
    int paddle1Velocity = 1;                              // Paddle 1 velocity

    // Draw the Pong Field
    myOLED.erase();

    // Draw an outline of the screen:
    myOLED.rectangle(0, 0, width - 1, height);

    // Draw the center line
    myOLED.rectangleFill(width / 2 - 1, 0, 2, height);

    bool firstLoop = true;

    while ((ball_X - ball_rad > 1) && (ball_X + ball_rad < width - 2))
    {

        if (!firstLoop)
        {

            // Erase the old ball. In XOR mode, so just draw old values again!
            // Draw the Paddles:
            myOLED.rectangleFill(paddle0_X, paddle0_Y, paddleW, paddleH);
            myOLED.rectangleFill(paddle1_X, paddle1_Y, paddleW, paddleH);
            // Draw the ball: - use rect - xor and circle fails b/c of circle algorithm overdraws
            myOLED.rectangleFill(ball_X, ball_Y, ball_rad, ball_rad);
        }
        // Increment ball's position
        ball_X += ballVelocityX;
        ball_Y += ballVelocityY;

        // Check if the ball is colliding with the left paddle
        if (ball_X - ball_rad < paddle0_X + paddleW)
        {

            // Check if ball is within paddle's height
            if ((ball_Y > paddle0_Y) && (ball_Y < paddle0_Y + paddleH))
            {

                ball_X++;                       // Move ball over one to the right
                ballVelocityX = -ballVelocityX; // Change velocity
            }
        }

        // Check if the ball hit the right paddle
        if (ball_X + ball_rad > paddle1_X)
        {

            // Check if ball is within paddle's height
            if ((ball_Y > paddle1_Y) && (ball_Y < paddle1_Y + paddleH))
            {

                ball_X--;                       // Move ball over one to the left
                ballVelocityX = -ballVelocityX; // change velocity
            }
        }

        // Check if the ball hit the top or bottom
        if ((ball_Y <= 1) || (ball_Y >= (height - ball_rad - 1)))
        {

            // Change up/down velocity direction
            ballVelocityY = -ballVelocityY;
        }

        // Move the paddles up and down
        paddle0_Y += paddle0Velocity;
        paddle1_Y += paddle1Velocity;

        // Change paddle 0's direction if it hit top/bottom
        if ((paddle0_Y <= 1) || (paddle0_Y > height - 2 - paddleH))
            paddle0Velocity = -paddle0Velocity;

        // Change paddle 1's direction if it hit top/bottom
        if ((paddle1_Y <= 1) || (paddle1_Y > height - 2 - paddleH))
            paddle1Velocity = -paddle1Velocity;

        // Draw the Paddles:
        myOLED.rectangleFill(paddle0_X, paddle0_Y, paddleW, paddleH);
        myOLED.rectangleFill(paddle1_X, paddle1_Y, paddleW, paddleH);

        // Draw the ball:
        myOLED.rectangleFill(ball_X, ball_Y, ball_rad, ball_rad);

        // Actually draw everything on the screen:
        myOLED.display();

        // Once the first loop is done, switch to XOR mode. So we just update our
        // moving parts
        if (firstLoop)
        {
            firstLoop = false;
            myOLED.setDrawMode(grROPXOR);
        }

        delay(25); // Delay for visibility
    }
    delay(1000);
    myOLED.setDrawMode(grROPCopy);
}
