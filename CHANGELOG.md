## 1.1.3

* I/O logging for future replay functionality. RX frames that pass CRC and all
 TX frames are logged at info level.
* Added loggers `telemetry.rx` and `telemetry.tx`
* Adding Appveyor support
* Support Python 3.3, 3.4 and 3.5
* Fixed README.md not displayed on pypi

## 1.1.2

* Indexed topics are now supported [`topic:2`, 123] -> [topic, 2], 123
