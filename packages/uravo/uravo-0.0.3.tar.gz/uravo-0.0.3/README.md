# python-uravo

A python interface to the (still theoretical) [Uravo](https://github.com/minorimpact/uravo) monitoring system.

## Installation

    $ pip3 install uravo

## Usage

```
    from uravo import uravo
    import random

    def test_thing():
        return True if (random.randint(1,100) % 2) else False
        
    if test_thing():
        uravo.alert(Severity="green", AlertGroup="thing", Summary="Thing is good.")
    else:
        uravo.alert(Severity="red", AlertGroup="thing", Summary="Thing is bad.")

```
This is mostly just a placeholder for early testing, at this point.  Since Uravo doesn't really exist, as such, this module will fail silently if it can't connect or if it's not installed.


