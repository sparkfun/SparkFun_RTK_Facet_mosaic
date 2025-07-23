---
icon: material/book-open-page-variant
---

# Introduction
<div class="grid cards desc" markdown>

-   <a href="https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic.html">
	**SparkPNT RTK Facet mosaic**<br>
	**SKU:** GPS-24903

	---

	<figure markdown>
	
	![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/2/5/1/9/5/24903-RTK-Facet-Mosaic-L-Band-Feature-2.jpg)
	</figure></a>


	<center>
	<article class="video-500px">
	<iframe src="https://www.youtube.com/embed/e3OKRtJDPgw" title="Product Showcase Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
	![QR code to product video](./assets/img/qr_code/product_video.png){ .qr width=100 }
	</article>
	</center>


-	Designed and manufactured in Boulder, Colorado, USA, and utilizing the multi-band mosaic-X5 from Septentrio, the [SparkPNT RTK Facet mosaic](https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic.html) is *the* top of the line receiver for high precision geolocation and surveying needs. For basic users, it's incredibly easy to get up and running; for advanced users, the RTK Facet mosaic is a flexible and powerful tool. With just the press of a button, the RTK Facet mosaic is the fastest way to take centimeter-grade measurements. With a [subscription to the PointPerfect Flex NTRIP/RTCM service](https://www.sparkfun.com/rtk_facet_mosaic_registration) or any other correction service, 10mm Real Time Kinematic fixes are less than a minute away. By connecting your phone to the RTK Facet mosaic over Bluetooth®, your phone or tablet can receive the NMEA output and work with most GIS software programs. This is exactly how $10,000 surveying devices have been operating for the past decade - we just made it faster, more precise, and a lot more economical.

	The RTK Facet mosaic works with common GIS software for Android and iOS including SW Maps [Android](https://sparkfun.github.io/SparkFun_RTK_Firmware/gis_software/#sw-maps) / [iOS](https://apps.apple.com/us/app/sw-maps/id6444248083), [Field Genius](https://www.microsurvey.com/products/fieldgenius-for-android/), [SurvPC](https://www.carlsonsw.com/product/carlson-survce), [Survey Master](https://docs.sparkfun.com/SparkFun_RTK_Firmware/gis_software/#survey-master), [Vespucci](https://play.google.com/store/apps/details?id=de.blau.android&hl=en_US&gl=US), [QGIS](https://qgis.org/), [QField](https://docs.qfield.org/get-started/), and any GIS software that supports NMEA over Bluetooth.

	Under the hood of the SparkPNT RTK Facet mosaic is an ESP32-WROVER-E connected to a mosaic-X5 GNSS multi-band receiver, and a variety of peripheral hardware (LiPo fuel gauge, microSD, etc). Additionally, housed under the dome of the RTK Facet mosaicis a surveyor grade L1/L2/L5 antenna. This antenna is a unique combination of elements designed to receive the GNSS signals (L1/L2/L5). The RTK Facet mosaic is programmed in Arduino and can be tailored by you to fit whatever your needs may be.

	This device can be used in five modes:

	- GNSS Positioning (~30cm accuracy) - also known as **Rover**
	- GNSS Positioning with RTK (1.4cm accuracy) - also known as **Rover with RTK Fix**
	- GNSS **Base Station**
	- GNSS **Base Station NTRIP Server**

	At *Power On* the device will enter **Rover** or **Base** mode; whichever state the device was in at the last power down. When the POWER/SETUP button is pressed momentarily, a menu is presented to change the RTK Facet mosaic from *Rover to Base mode* or vice-versa. The display will indicate the change with a small car *(Rover)* or flag *(Base)* icon.

	In **Rover mode** the RTK Facet mosaic will receive `L1`, `L2`, and `L5` GNSS signals from the four constellations (GPS, GLONASS, Galileo, and BeiDou). The device will calculate the position based on the combination of GNSS. If the device has been registered with PointPerfect or any other correction service, the receiver will quickly (within 60 seconds) obtain an RTK float, then fix. Similar to a standard grade GPS receiver, the RTK Facet mosaic will output industry standard NMEA sentences at 4Hz and broadcast them to any paired Bluetooth® device. The end user will need to parse the NMEA sentences using commonly available mobile apps, GIS products, or embedded devices (there are many open source libraries). Unlike standard grade GPS receivers that have 2500mm accuracy, the accuracy in this mode is approximately 10 to 60mm horizontal positional accuracy.

	In **Base mode** the device will enter Base Station mode. This is used when the device is mounted to a fixed position (like a tripod or roof). The RTK Facet mosaic will initiate a survey. After 60 to 120 seconds the survey will complete and the RTK Facet mosaic will begin transmitting RTCM correction data out the radio port. A base is often used in conjunction with a second RTK Facet mosaic (or RTK Torch, Facet, Surveyor, Express, Express Plus, etc) unit set to *Rover* to obtain the 10mm accuracy. Said differently, the Base sits still and sends correction data to the Rover, so that the Rover can output really accurate position data for its location.

	In addition to supplying position data, the RTK Facet mosaic is capable of logging NMEA and raw GNSS satellite data for post processing making it ideal for research and advanced positioning applications.

	The RTK Facet mosaic is an open-source hardware product meaning you can fully obtain, see, and even modify the electrical and mechanical design files. This allows for easier maintenance and repair over time.

	The SparkPNT RTK Facet mosaic kit includes everything you need: the enclosed device, thread adapter, charger, data cables, and carrying case. It does **NOT** include a [surveying pole](https://www.sparkfun.com/telescopic-surveying-pole.html) *(any additional items will need to be purchased separately)*.


	<center>
	
	[&nbsp;![QR code to product page](./assets/img/qr_code/product-low.png){ .tinyqr }&nbsp;&nbsp;Purchase from SparkFun :fontawesome-solid-cart-plus:{ .heart }&nbsp;&nbsp;&nbsp;](https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic.html){ .md-button .md-button--primary }
	</center>

</div>

!!! failure "Permanent Installation"
	
	The SparkPNT RTK Facet mosaic is not designed for permanent outdoor mounting. Please use the [RTK mosaic-X5](https://www.sparkfun.com/sparkfun-rtk-mosaic-x5.html) or the [RTK Reference Station](https://www.sparkfun.com/products/22429) that is located inside or protected from the elements. Or, for a DIY solution, the [ESP32](https://www.sparkfun.com/sparkfun-thing-plus-esp32-wroom-micro-b.html) attached to our [ZED-F9P breakout](https://www.sparkfun.com/sparkfun-gps-rtk-sma-breakout-zed-f9p-qwiic.html) is a great way to go. See our [How to Build a DIY GNSS Reference Station](https://learn.sparkfun.com/tutorials/how-to-build-a-diy-gnss-reference-station) tutorial for more information.


!!! note "Completely Open-Source"
	- The [RTK Everywhere firmware](https://github.com/sparkfun/SparkFun_RTK_Everywhere_Firmware) is open-source, so users can obtain, check, and even modify the device's functionality. This allows for easier feature expansion, bug maintenance, and longer device longevity.
	- Additionally, the hardware is also open-source, so users can obtain, check, and even modify the device's design.

## :fontawesome-solid-list-check: Required Materials
To get started, users will need a few items. Some users may already have a few of these items, feel free to adjust accordingly.

<div class="annotate" markdown>

- Computer or mobile device with Bluetooth® and WiFi capabilities
- [SparkPNT RTK Facet mosaic](https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic.html)
- [Telescopic Surveying Pole](https://www.sparkfun.com/telescopic-surveying-pole.html)
- [PointPerfect Registration](https://www.sparkfun.com/rtk_facet_mosaic_registration)

</div>

<div class="grid cards products" markdown>

-   <a href="https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic.html">
	<figure markdown>
	![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/2/5/1/9/5/24903-RTK-Facet-Mosaic-L-Band-Feature-2.jpg)
	</figure>

	---

	**SparkPNT RTK Facet mosaic**<br>
	GPS-29688</a>

-   <a href="https://www.sparkfun.com/telescopic-surveying-pole.html">
	<figure markdown>
	![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/2/6/4/8/2/25795-Telescopic-Surveying-Pole-Front.jpg)
	</figure>

	---

	**Telescopic Surveying Pole**<br>
	GPS-25795</a>

</div>

???+ note "Serial Transceivers, UART Adapters, and USB Cables"
	To configure the UART ports that are broken out on the board, users will need a [UART adapter](https://www.sparkfun.com/categories/349). Once configured, the UART ports can utilize one of our RF transceivers to send/receive RTCM messages.

	=== "Transceivers"

		<div class="grid cards" markdown>

		-   <a href="https://www.sparkfun.com/products/19032">
			<figure markdown>
			![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/1/8/6/3/4/19032-SiK_Telemetry_Radio_V3_-_915MHz__100mW-01.jpg)
			</figure>

			---

			**SiK Telemetry Radio V3 - 915MHz, 100mW**<br>
			WRL-19032</a>

		-   <a href="https://www.sparkfun.com/products/20029">
			<figure markdown>
			![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/1/9/7/9/0/SparkFun_LoRaSerial_Enclosed_-_20029-1.jpg)
			</figure>

			---

			**SparkFun LoRaSerial Kit - 915MHz (Enclosed)**<br>
			WRL-20029</a>

		-   <a href="https://www.sparkfun.com/products/17854">
			<figure markdown>
			![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/1/7/0/3/4/17854-GHR-04V-S_to_GHR-06V-S_Cable_-_50mm-01.jpg)
			</figure>

			---

			**GHR-04V-S to GHR-06V-S Cable - 100mm**<br>
			CAB-17854</a>

		</div>


	=== "USB Cables"

		<div class="grid cards" markdown>

		-   <a href="https://www.sparkfun.com/products/14743">
			<figure markdown>
			![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/1/2/9/7/2/14743-USB_3.1_Cable_A_to_C_-_3_Foot-01.jpg)
			</figure>

			---

			**USB 3.1 Cable A to C - 3 Foot**<br>
			CAB-14743</a>

		-   <a href="https://www.sparkfun.com/products/21271">
			<figure markdown>
			![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/2/1/0/4/9/21271-_CAB-_01.jpg)
			</figure>

			---

			**SparkFun 4-in-1 Multi-USB Cable - USB-C Host**<br>
			CAB-21271</a>

		-   <a href="https://www.sparkfun.com/products/21272">
			<figure markdown>
			![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/2/1/0/5/0/21272-_CAB-_01.jpg)
			</figure>

			---

			**SparkFun 4-in-1 Multi-USB Cable - USB-A Host**<br>
			CAB-21272</a>

		</div>



??? note "Jumper Modification"
	To modify the [jumpers](./hardware_overview.md/#jumpers), users will need [soldering equipment](https://www.sparkfun.com/categories/49) and/or a [hobby knife](https://www.sparkfun.com/categories/379).


	!!! tip "New to jumper pads?"
		Check out our [Jumper Pads and PCB Traces Tutorial](https://learn.sparkfun.com/tutorials/664) for a quick introduction!

		<div class="grid cards" markdown align="center">

		-   <a href="https://learn.sparkfun.com/tutorials/664">
			<figure markdown>
			![Tutorial thumbnail](https://cdn.sparkfun.com/c/264-148/assets/learn_tutorials/6/6/4/PCB_TraceCutLumenati.jpg)
			</figure>

			---

			**How to Work with Jumper Pads and PCB Traces**</a>

		</div>


	<div class="grid cards" markdown>

	-   <a href="https://www.sparkfun.com/products/24063">
		<figure markdown>
		![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/2/4/3/8/5/KIT-24063-PINECIL-Soldering-Iron-Kit-Feature.jpg)
		</figure>

		---

		**PINECIL Soldering Iron Kit**<br>
		KIT-24063</a>

	-   <a href="https://www.sparkfun.com/products/9200">
		<figure markdown>
		![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/2/6/4/6/09200-Hobby_Knife-01.jpg)
		</figure>

		---

		**Hobby Knife**<br>
		TOL-09200</a>

	-   <a href="https://www.sparkfun.com/products/14579">
		<figure markdown>
		![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/1/2/7/2/5/14579-Chip_Quik_No-Clean_Flux_Pen_-_10mL-01.jpg)
		</figure>

		---

		**Chip Quik No-Clean Flux Pen - 10mL**<br>
		TOL-14579</a>

	-   <a href="https://www.sparkfun.com/products/9327">
		<figure markdown>
		![Product Thumbnail](https://cdn.sparkfun.com/assets/parts/2/8/7/5/09327-Solder_Wick__2_5ft._-_Generic-01.jpg)
		</figure>

		---

		**Solder Wick #2 5ft. - Generic**<br>
		TOL-09327</a>

	</div>



## :material-bookshelf: Suggested Reading

As a more sophisticated product, we will skip over the more fundamental tutorials (i.e. [**Ohm's Law**](https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law) and [**What is Electricity?**](https://learn.sparkfun.com/tutorials/what-is-electricity)). However, below are a few tutorials that may help users familiarize themselves with various aspects of the board.

!!! tip
	Check out the [www.gps.gov](https://www.gps.gov/) website to learn more about the U.S.-owned [Global Positioning System (GPS)](https://www.gps.gov/systems/gps/) and the [Global Navigation Satellite Systems (GNSS) of other countries](https://www.gps.gov/systems/gnss/).


<div class="grid cards" markdown align="center">

-   <a href="https://learn.sparkfun.com/tutorials/9">
	<figure markdown>
	![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/parts/5/9/7/4/10890-01.jpg)
	</figure>

	---

	**GPS Basics**</a>

-   <a href="https://learn.sparkfun.com/tutorials/813">
	<figure markdown>
	![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/learn_tutorials/8/1/3/Location-Wandering-GPS-combined.jpg)
	</figure>

	---

	**What is GPS RTK?**</a>

-   <a href="https://docs.sparkfun.com/SparkFun_RTK_Everywhere_Firmware">
	<figure markdown>
	![Tutorial Thumbnail](https://docs.sparkfun.com/SparkFun_RTK_Everywhere_Firmware/img/thumbnail.jpg)
	</figure>

	---

	**SparkFun RTK Everywhere Product Manual**</a>

-   <a href="https://learn.sparkfun.com/tutorials/1362">
	<figure markdown>
	![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/learn_tutorials/1/3/6/2/GNSS_RTK_DIY_Surveying_Tutorial.jpg)
	</figure>

	---

	**Setting up a Rover Base RTK System**</a>

-   <a href="https://learn.sparkfun.com/tutorials/1363">
	<figure markdown>
	![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/learn_tutorials/1/3/6/3/Roof_Enclosure.jpg)
	</figure>

	---

	**How to Build a DIY GNSS Reference Station**</a>

-   <a href="https://learn.sparkfun.com/tutorials/2583">
	<figure markdown>
	![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/learn_tutorials/2/5/8/3/SparkFun_RTK_Facet_-_Hookup_Guide_Preview.jpg)
	</figure>

	---

	**SparkFun RTK Facet L-Band Hookup Guide**</a>

-   <a href="https://learn.sparkfun.com/tutorials/8">
	<figure markdown>
	![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/7/d/f/9/9/50d24be7ce395f1f6c000000.jpg)
	</figure>

	---

	**Serial Communication**</a>

-   <a href="https://learn.sparkfun.com/tutorials/112">
	<figure markdown>
	![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/learn_tutorials/1/1/2/thumb.jpg)
	</figure>

	---

	**Serial Terminal Basics**</a>

-   <a href="https://learn.sparkfun.com/tutorials/82">
	<figure markdown>
	![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/learn_tutorials/8/2/I2C-Block-Diagram.jpg)
	</figure>

	---

	**I2C**</a>


</div>

??? info "Related Blog Posts"
	Additionally, users may be interested in these blog post articles on GNSS technologies:

	<div class="grid cards" markdown align="center">

	-   <a href="https://www.sparkfun.com/news/4276">
		<figure markdown>
		![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/home_page_posts/4/2/7/6/GPSvGNSSHomepageImage4.png)
		</figure>

		---

		**GPS vs GNSS**</a>

	-   <a href="https://www.sparkfun.com/news/7138">
		<figure markdown>
		![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/home_page_posts/7/1/3/8/SparkFun_RTK_Facet_-_Surveying_Monopod.jpg)
		</figure>

		---

		**What is Correction Data?**</a>

	-   <a href="https://www.sparkfun.com/news/7533">
		<figure markdown>
		![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/home_page_posts/7/5/3/3/rtk-blog-thumb.png)
		</figure>

		---

		**Real-Time Kinematics Explained**</a>

	-   <a href="https://www.sparkfun.com/news/7401">
		<figure markdown>
		![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/home_page_posts/7/4/0/1/Screen_Shot_2023-06-26_at_8.30.22_PM.png)
		</figure>

		---

		**New Video: Unlocking High-Precision RTK Positioning**</a>

	-   <a href="https://www.sparkfun.com/news/9514">
		<figure markdown>
		![Tutorial Thumbnail](https://cdn.sparkfun.com/c/264-148/assets/home_page_posts/9/5/1/4/DIY-Surveying-Blog__1_.jpg)
		</figure>

		---

		**DIY RTK Surveying**</a>

	</div>
