## 1.1.3

* I/O logging for future replay functionality. RX frames that pass CRC and all
 TX frames are logged at info level.
* Added loggers `telemetry.rx` and `telemetry.tx`

## 1.1.2

* Indexed topics are now supported [`topic:2`, 123] -> [topic, 2], 123
