---
icon: material/tools
---

The RTK Facet mosaic was designed to work with low-cost, off the shelf equipment. The RTK Facet mosaic is designed to use corrections provided via u-blox's PointPerfect system, therefore, a Base/Rover setup is not needed. However, if the service is not available the RTK Facet mosaic can still be used in a traditional Base/Rover setup. Here we’ll describe how to assemble a Rover and Base.

## Surveying (Rover Mode)

<figure markdown>
[![Basic RTK Facet mosaic setup](https://cdn.sparkfun.com/r/600-600/assets/learn_tutorials/2/1/8/8/SparkFun_RTK_Facet_-_On_Monopod.jpg)](https://cdn.sparkfun.com/assets/learn_tutorials/2/1/8/8/SparkFun_RTK_Facet_-_On_Monopod.jpg)
<figcaption markdown>
Basic RTK Facet mosaic Rover setup with RTCM over Bluetooth
</figcaption>
</figure>

Shown above is the most common RTK Rover setup. A monopole designed for cameras is used. The ¼” camera thread of the monopole is [adapted to ⅝” 11-TPI](https://www.sparkfun.com/products/17546) and the RTK Facet mosaic is mounted on top. No radio is needed because RTCM correction data is provided by a phone over Bluetooth.

!!! tip
	If you’re shopping for a monopole (aka monopod), get one that is 65” in length or greater to ensure that the antenna will be above your head. We’ve had good luck with the [Amazon Basics](https://www.amazon.com/AmazonBasics-WT1003-67-Inch-Monopod/dp/B00FAYL1YU) brand.

	If you prefer to mount your tablet or cell phone to the monopole be sure to get a clamp that is compatible with the diameter of your monopole and has a knob to increase clamp pressure. Our monopole is 27mm in diameter so a device clamp would need to be able to handle that diameter.

## Radio Link

<figure markdown>
[![RTK Facet mosaic setup with radio](https://cdn.sparkfun.com/r/600-600/assets/learn_tutorials/2/1/8/8/SparkFun_RTK_Facet_-_External_Radio.jpg)](https://cdn.sparkfun.com/assets/learn_tutorials/2/1/8/8/SparkFun_RTK_Facet_-_External_Radio.jpg)
<figcaption markdown>
2nd most common setup with a 915MHz Radio providing RTCM
</figcaption>
</figure>

If you are receiving RTCM correction data over a radio link it’s recommended that you attach a radio to the bottom of the RTK Facet mosaic.

<figure markdown>
[![Serial Telemetry Radio mounted to the back of RTK Facet mosaic](https://cdn.sparkfun.com/r/600-600/assets/learn_tutorials/2/1/8/8/SparkFun_RTK_Facet_-_External_Radio_Positioning.jpg)](https://cdn.sparkfun.com/assets/learn_tutorials/2/1/8/8/SparkFun_RTK_Facet_-_External_Radio_Positioning.jpg)
<figcaption markdown>
</figcaption>
</figure>

[Picture hanging strips](https://www.amazon.com/gp/product/B073XS3CHW) from 3M make a nice semi-permanent mount. Plug the 4-pin to 6-pin JST cable included with the RTK Facet mosaic from the **Radio** port to either of the [Serial Telemetry Radios](https://www.sparkfun.com/products/19032) (shipped in pairs). We really love these radios because they are paired out of the box, either can send or receive (so it doesn't matter which radio is attached to base or rover) and they have remarkable range. We achieved over a mile range (nearly 1.5 miles or 2.4km) with the 100mW radios and a [big 915MHz antenna](https://www.sparkfun.com/products/retired/14868) on the base (see [this tutorial](https://learn.sparkfun.com/tutorials/how-to-build-a-diy-gnss-reference-station#mini-computer-setup) for more info).

## Temporary Base

A temporary or mobile base setup is needed when you are in the field too far away from a correction source and/or cellular reception. A 2nd RTK Facet mosaic is mounted to a tripod and it is configured to complete a survey-in (aka, locate itself), then begin broadcasting RTCM correction data. This data (~1000 bytes a second) is sent to the user's connected radio of choice. For our purposes, the 915MHz 100mW telemetry radios are used because they provide what is basically a serial cable between our base and rover.

<figure markdown>
[![Temporary RTK Facet mosaic Base setup](https://cdn.sparkfun.com/assets/learn_tutorials/2/1/8/8/SparkFun_RTK_Facet_-_Base_Tripod.jpg)](https://cdn.sparkfun.com/assets/learn_tutorials/2/1/8/8/SparkFun_RTK_Facet_-_Base_Tripod.jpg)
<figcaption markdown>
Temporary RTK Facet mosaic Base setup
</figcaption>
</figure>

Any tripod with a ¼” camera thread will work. The [Amazon Basics tripod](https://www.amazon.com/AmazonBasics-Lightweight-Camera-Mount-Tripod/dp/B00XI87KV8) works well enough but is a bit light weight and rickety. The ¼” camera thread is [adapted to ⅝” 11-TPI](https://www.sparkfun.com/products/17546) and the RTK Facet mosaic is attached on top.

Once the base has been setup with a clear view of the sky, turn on the RTK Facet mosaic. Once on, press the *Setup* button to put the device in Base mode. The display will show the Survey-In screen for 60-120 seconds. Once the survey is complete the display will show the 'Xmitting' display and begin producing RTCM correction data. You can verify this by viewing the LEDs on the telemetry radio (a small red LED will blink when serial data is received from the RTK Facet mosaic). The RTK Facet mosaic is designed to follow the u-blox recommended survey-in of 60s and a mean 3D standard deviation of 5m of all fixes. If a survey fails to achieve these requirements it will auto-restart after 10 minutes.

!!! tip
	A mobile base station works well for quick trips to the field. However, the survey-in method is not recommended for the highest accuracy measurements because the positional accuracy of the base will directly translate to the accuracy of the rover. Said differently, if your base's calculated position is off by 100cm, so will every reading your rover makes. If you’re looking for maximum accuracy consider installing a [static base with fixed antenna](https://learn.sparkfun.com/tutorials/how-to-build-a-diy-gnss-reference-station#static-base-setup--lasers). We were able to pinpoint the antenna on the top of SparkFun with an incredible accuracy [+/-2mm of accuracy](https://cdn.sparkfun.com/assets/learn_tutorials/1/4/6/3/SparkFun_PPP_Results.png) using PPP!
