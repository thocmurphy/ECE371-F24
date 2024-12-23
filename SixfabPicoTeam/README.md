# UMass Amherst - ECE 371 Honors Project:

## Measuring LTE Board Time Drift

Assignment given by Professor Taqi Raza and supervized by teaching assistant Shayan Nazeer

Goal: Synchronize time of Sixfab Pico LTE with an NTP server and measure board time drift.

## Project Guide/Progression

The board we chose to use was the [Sixfab Pico LTE](https://sixfab.com/product/sixfab-pico-lte/?aelia_cs_currency=USD&gad_source=1). Coding and analysis was performed in micropython.

The initial setup was done following the [documentation and startup guides on the Sixfab Pico website](https://docs.sixfab.com/docs/sixfab-pico-lte-introduction). It is highly encouraged that you read the startup guide in addition to watching the [video](https://drive.google.com/file/d/1mRsmOIFTTY4yG91iCcDXVeBcQCoU7H8K/view?usp=sharing) included in the project for a comprehensive understanding of the project. This included activating the SIM card with the network provider (found by scanning the QR code on the board), installing the [Pico LTE SDK](https://github.com/sixfab/pico_lte_micropython-sdk), and installing [Thonny](https://thonny.org/), the recommended IDE for the board. Additional instructions on how to properly install the SDK can be found in the [video](https://drive.google.com/file/d/1mRsmOIFTTY4yG91iCcDXVeBcQCoU7H8K/view?usp=sharing). We first wrote and ran boardBlink.py to ensure that setup was performed properly.

Our first deliverable was connecting the board to the internet. Our group used the built-in PicoLTE micropython module that came with the SDK and [webhook.site](webhook.site) to send HTTP GET, PUT, and POST requests from the board and confirm an internet connection. The Pico LTE documentation has multiple pages on how to accomplish this along with pre-written micropython scripts included in the SDK, these can also be found in the initialTesting folder. 

Our second deliverable was to connect to an NTP server and sync the board’s time to it. In our research, we found that NTP servers require a UDP connection and that the PicoLTE module does not include functions that support such a protocol. Our way to circumvent this was to use AT commands, commands used to establish and configure a network connection, with the PicoLTE module and the send_at_comm() function. Examples of our AT command attempts can be found in the networkTesting folder. The first thing we noticed was that upon powering up the board, the Pico LTE automatically synchronized its time with the network. From there we found multiple AT commands that create and confirm a network connection as well pull the time from the board’s 4G network. See SyncTimeWithAT.py in the networkTesting folder for an example. 

There was a problem with our AT command method. The network time is only given a precision of seconds and the time drift of the Pico LTE is too minor to be analysed in such a resolution. This led us to continue using AT commands in an attempt to create a UDP connection with an actual NTP server through the network. However, this is the point we got stuck. Regardless of forming connections with the network and ensuring their validity, forming a link with a NTP server or even creating a UDP socket led to errors. We also attempted to use python modules socket and ntptime (including custom ones for pico boards) along with the PicoLTE module, but those methods did not work for us either.

After struggling, we decided to shift to finding drift through connecting through WiFi instead of using the 4G network. We were able to find success utilizing home WiFi, we figured eduroam or other school networks would cause problems with the additional authentication but did not test this. Utilizing [code written by aallan](https://gist.github.com/aallan/581ecf4dc92cd53e3a415b7c33a1147c), the connection was swift and the NTP server returned the time with millisecond accuracy. We used this to perform our analysis on the board’s time drift.

We wrote [ntp_utils.py](https://github.com/sasha351/NTPdrift/blob/main/ntp_utils.py) to take advantage of aallan's code and also write our own functions to get the time from the NTP server and set the board's time with it. Next, we wrote [ntp_drift.py](https://github.com/sasha351/NTPdrift/blob/main/ntp_drift.py), which uses ntp_utils.py to connect to the network, set the board's time, and then runs in an infinite loop calculating the drift over 5 minute intervals and outputting to a csv file. You can view some of our data from different NTP servers in the repo.

## Results and Analysis

After running ntp_utils.py twice for two difference NTP servers (each run lasting a little more than 14 hours), a significant drift of about 51 seconds was observed on each server. The drift appears accumulate linearly as time progresses, as seen in [pool_ntp_org.png](https://github.com/sasha351/NTPdrift/blob/main/pool_ntp_org.png) and [time1_google_com.png](https://github.com/sasha351/NTPdrift/blob/main/time1_google_com.png). These graphs were plotted from the data in [test1_raw.txt](https://github.com/sasha351/NTPdrift/blob/main/test1_raw.txt) and [test2_raw.txt](https://github.com/sasha351/NTPdrift/blob/main/test2_raw.txt), respectively.

## Associated Links

- [Sixfab Pico](https://sixfab.com/product/sixfab-pico-lte/?aelia_cs_currency=USD&gad_source=1)
- [Sixfab Pico Documentation](https://docs.sixfab.com/docs/sixfab-pico-lte-introduction)
- [Sixfab Pico LTE SDK/micropython module](https://github.com/sixfab/pico_lte_micropython-sdk)
- [Thonny IDE](https://thonny.org/)
- [webhook.site](https://webhook.site/#!/view/668411be-19ef-49e1-85cf-9ccfb0d3f7c3)
- [Pool NTP](https://www.ntppool.org/en/)

## Authors

- [Owen Raftery](https://github.com/realraft)
- [Sasha Shikhanovich](https://github.com/sasha351)
- [Thomas Murphy](https://github.com/thocmurphy)
- [Kyle Belanger](https://github.com/kfb-123)

