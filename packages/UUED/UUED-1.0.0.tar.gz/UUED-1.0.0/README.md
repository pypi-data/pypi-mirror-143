# uued
UUED is rails way of generating unique and trackable ids.

UUED is based off of twitter's snowflake id.

## example

```py
import uued

gen = uued.Generator(1230249600000)  # rails epoch

print(str(gen))
```