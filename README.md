SparkPNT RTK Facet mosaic
========================================

[![SparkPNT RTK Facet mosaic](https://cdn.sparkfun.com/r/600-600/assets/parts/2/5/1/9/5/24903-RTK-Facet-Mosaic-L-Band-Feature-2.jpg)](https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic.html)

[*SparkPNT RTK Facet mosaic (GPS-29688)*](https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic.html)

Designed and manufactured in Boulder, Colorado, USA, and utilizing the multi-band mosaic-X5 from Septentrio, the [SparkPNT RTK Facet mosaic](https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic.html) is *the* top of the line receiver for high precision geolocation and surveying needs. For basic users, it's incredibly easy to get up and running; for advanced users, the RTK Facet mosaic is a flexible and powerful tool. With just the press of a button, the RTK Facet mosaic is the fastest way to take centimeter-grade measurements. With a [subscription to the PointPerfect Flex NTRIP/RTCM service](https://www.sparkfun.com/rtk_facet_mosaic_registration) or any other corrections service, 10mm Real Time Kinematic fixes are less than a minute away. By connecting your phone to the RTK Facet mosaic over Bluetooth®, your phone or tablet can receive the NMEA output and work with most GIS software programs. This is exactly how $10,000 surveying devices have been operating for the past decade - we just made it faster, more precise, and a lot more economical.

The RTK Facet mosaic works with common GIS software for Android and iOS including SW Maps [Android](https://sparkfun.github.io/SparkFun_RTK_Firmware/gis_software/#sw-maps) / [iOS](https://apps.apple.com/us/app/sw-maps/id6444248083), [Field Genius](https://www.microsurvey.com/products/fieldgenius-for-android/), [SurvPC](https://www.carlsonsw.com/product/carlson-survce), [Survey Master](https://docs.sparkfun.com/SparkFun_RTK_Firmware/gis_software/#survey-master), [Vespucci](https://play.google.com/store/apps/details?id=de.blau.android&hl=en_US&gl=US), [QGIS](https://qgis.org/), [QField](https://docs.qfield.org/get-started/), and any GIS software that supports NMEA over Bluetooth.

Under the hood of the SparkPNT RTK Facet mosaic is an ESP32-WROVER-E connected to a mosaic-X5 GNSS multi-band receiver, and a variety of peripheral hardware (LiPo fuel gauge, microSD, etc). Additionally, housed under the dome of the RTK Facet mosaic is a surveyor grade L1/L2/L5 antenna. This antenna is a unique combination of elements designed to receive the GNSS signals (L1/L2/L5). The RTK Facet mosaic is programmed in Arduino and can be tailored by you to fit whatever your needs may be.

This device can be used in five modes:

- GNSS Positioning (~30cm accuracy) - also known as **Rover**
- GNSS Positioning with RTK (1.4cm accuracy) - also known as **Rover with RTK Fix**
- GNSS **Base Station**
- GNSS **Base Station NTRIP Server**

At *Power On* the device will enter **Rover** or **Base** mode; whichever state the device was in at the last power down. When the POWER/SETUP button is pressed momentarily, a menu is presented to change the RTK Facet mosaic from *Rover to Base mode* or vice-versa. The display will indicate the change with a small car *(Rover)* or flag *(Base)* icon.

In **Rover mode** the RTK Facet mosaic will receive `L1`, `L2`, and `L5` GNSS signals from the four constellations (GPS, GLONASS, Galileo, and BeiDou) and calculate the position based on these signals. Similar to a standard grade GPS receiver, the RTK Facet mosaic will output industry standard NMEA sentences at 4Hz and broadcast them over any paired Bluetooth® device. The end user will need to parse the NMEA sentences using commonly available mobile apps, GIS products, or embedded devices (there are many open source libraries). Unlike standard grade GPS receivers that have **2500mm** accuracy, the accuracy in this mode is approximately **300mm** horizontal positional accuracy. When RTCM correction data is sent over Bluetooth® or into the radio port, the device will automatically enter Positioning with RTK mode. In this mode RTK Facet mosaic will receive `L1`/`L2`/`L5` signals from the antenna and correction data from a base station. The receiver will quickly (within a second) obtain an RTK float, then fix. The NMEA sentences will have increased accuracy of 10mm horizontal and 10mm vertical accuracy. The RTCM correction data is most easily obtained over the Internet using a free app on your phone (see our SW Maps *([Android](http://docs.sparkfun.com/SparkFun_RTK_Everywhere_Firmware/gis_software_android/#sw-maps)/[iOS](http://docs.sparkfun.com/SparkFun_RTK_Everywhere_Firmware/gis_software_ios/#sw-maps))* or [Lefebure NTRIP](http://docs.sparkfun.com/SparkFun_RTK_Everywhere_Firmware/gis_software_android/#lefebure) instructions) and sent over Bluetooth® to the RTK Facet mosaic. However, RTCM correction data can also be received over an external cellular or radio link from a 2nd RTK Torch, Postcard, Facet mosaic, Surveyor, Express, etc. that is setup as a base station.

In **Base mode** the device will enter Base Station mode. This is used when the device is mounted to a fixed position (like a tripod or roof). The RTK Facet mosaic will initiate a survey. After 60 to 120 seconds the survey will complete and the RTK Facet mosaic will begin transmitting RTCM correction data out the radio port. A base is often used in conjunction with a second RTK Facet mosaic (or RTK Surveyor, Express, Express Plus, etc) unit set to *Rover* to obtain the 10mm accuracy. Said differently, the Base sits still and sends correction data to the Rover, so that the Rover can output really accurate position data for its location.

In addition to supplying position data, the RTK Facet mosaic is capable of logging NMEA, RAWX, and SFRBX for post processing making it ideal for research and advanced positioning applications.

The RTK Facet mosaic is an open source hardware product meaning you can fully obtain, see, and even modify the electrical and mechanical design files. This allows for easier maintenance and repair over time.

The SparkPNT RTK Facet mosaic kit includes everything you need: the enclosed device, thread adapter, charger, data cables, and carrying case. It does **NOT** include a [surveying pole](https://www.sparkfun.com/telescopic-surveying-pole.html) *(any additional items will need to be purchased separately)*.

> [!IMPORTANT]
> The SparkPNT RTK Facet mosaic is not designed for permanent outdoor mounting. Please use the [RTK mosaic-X5](https://www.sparkfun.com/sparkfun-rtk-mosaic-x5.html) or the [RTK Reference Station](https://www.sparkfun.com/products/22429) that is located inside or protected from the elements. Or, for a DIY solution, the [ESP32](https://www.sparkfun.com/sparkfun-thing-plus-esp32-wroom-micro-b.html) attached to our [ZED-F9P breakout](https://www.sparkfun.com/sparkfun-gps-rtk-sma-breakout-zed-f9p-qwiic.html) is a great way to go. See our [How to Build a DIY GNSS Reference Station](https://learn.sparkfun.com/tutorials/how-to-build-a-diy-gnss-reference-station) tutorial for more information.

> [!NOTE]
> The [RTK Everywhere firmware](https://github.com/sparkfun/SparkFun_RTK_Everywhere_Firmware) is open-source, so users can obtain, check, and even modify the device's functionality. This allows for easier feature expansion, bug maintenance, and longer device longevity.


Documentation
--------------

- **[Hookup Guide (mkdocs)](http://docs.sparkfun.com/SparkFun_RTK_Facet_mosaic/)** - The hookup guide for the SparkPNT RTK Facet mosaic hosted by GitHub pages.<br>
  [![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/) [![GitHub Pages Deploy](https://github.com/sparkfun/SparkFun_RTK_Facet_mosaic/actions/workflows/generate_documentation.yml/badge.svg)](https://github.com/sparkfun/SparkFun_RTK_Facet_mosaic/actions/workflows/generate_documentation.yml)
- [User Manual - RTK Everywhere Firmware](https://docs.sparkfun.com/SparkFun_RTK_Everywhere_Firmware/) - Documentation for the [RTK Everywhere firmware](https://github.com/sparkfun/SparkFun_RTK_Everywhere_Firmware)

*Need to download or print our hookup guide?*

- [Print *(Print to PDF)* from Single-Page View](http://docs.sparkfun.com/SparkFun_RTK_Facet_mosaic/print_view)

Repository Contents
-------------------

- **[/docs](/docs/)** - Online documentation files
	- [assets](/docs/assets/) - Assets files
		- [3d_model](/docs/assets/3d_model/) - Files for the 3D models
			- [3D CAD Models](/docs/assets/3d_model/step_files.zip) (.step)
		- [board_files](/docs/assets/board_files/) - Files for the product design
			- [KiCad Design Files](/docs/assets/board_files/kicad_files.zip) (.zip)
			- [Schematics](/docs/assets/board_files/schematics.zip) (.pdf)
			<!-- - [Dimensions](/docs/assets/board_files/dimensions.pdf) (.pdf) -->
		- [component_documentation](/docs/assets/component_documentation/) - Datasheets for hardware components
		- [img/hookup_guide/](/docs/assets/img/hookup_guide/) - Images for hookup guide documentation
- **[/Enclosure](/Enclosure/)** - CAD model for an enclosure
- **[/Hardware](/Hardware/)** - Hardware design files (.brd, .sch)
	- **[/Production](/Production/)** - Production files

Product Variants
----------------

- [GPS-24903](https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic-l-band.html) - v1.0, Initial Release
- [GPS-29688](https://www.sparkfun.com/sparkpnt-rtk-facet-mosaic.html) - Rename the product to remove "L-Band" from the name. This is due to u-blox's choice to discontinue the L-Band service to North America starting on December 31st, 2025.

- Facet Product Line
	- [GPS-20000](https://www.sparkfun.com/sparkfun-rtk-facet-l-band.html) - SparkFun RTK Facet L-Band
	- [GPS-19984](https://www.sparkfun.com/sparkfun-rtk-facet.html) - SparkFun RTK Facet
	- [GPS-19029](https://www.sparkfun.com/products/19029) - SparkFun RTK Facet *(Initial Release)*
- mosaic-`XX` GNSS Module
	- [GPS-26289](https://www.sparkfun.com/products/26289) - SparkPNT GNSS Disciplined Oscillator
	- [GPS-23748](https://www.sparkfun.com/sparkfun-rtk-mosaic-x5.html) - SparkFun RTK mosaic-X5
	- [GPS-23088](https://www.sparkfun.com/sparkfun-triband-gnss-rtk-breakout-mosaic-x5.html) - SparkFun Triband GNSS RTK Breakout - mosaic-X5

License Information
-------------------

This product is ***open source***!

Please review the [`LICENSE.md`](./LICENSE.md) file for license information.

If you have any questions or concerns about licensing, please contact technical support on our [SparkFun forums](https://forum.sparkfun.com/viewforum.php?f=152).

Distributed as-is; no warranty is given.

- Your friends at SparkPNT.
