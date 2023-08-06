## Install package

```bash
pip install .
```

## Build documentation

```bash
python setup.py build-sphinx
```

## Basic Usage

```python
from pyManson import manson
ps = manson('/dev/ttyUSB0', 0)
ps.begin_session()
ps.output_on()
for voltage in range(1,10):
  ps.set_volts(voltage)
ps.output_off()
ps.end_session()
```

## Example script

```python
python ./examples/increments.py
```

## Troubleshooting

If you are using i.e. HCS-3202 with an USB connection using a CP210X USB-to-UART adapter. Sometimes is not presented in /dev/. 
If this is the case add a file ``12-synaptic.rules`` in ``/etc/udev/rules.d/`` which contains

```
    SUBSYSTEMS=="usb", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE="0666"
```

Execute 
```
udevadm control --reload
udevadm trigger
```

and reconnect the device. Now you should see the device in ``/dev/``.
Also make sure that ``brltty`` does not claim the device. If oyu do not need ``brltty`` remove it using
`` sudo apt remove brltty ``



## Documentation:

``` bash
doc/
```

**Author**
* Konstantin Niehaus

**Contributors**
* Robin Barta
