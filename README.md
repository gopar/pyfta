Pyfta
=====

Create fixtures from type annotations!

```python
from pyfta import Pyfta

class World():
    def __init__(self, c: float, d: Text) -> None:
        self.c = c
        self.d = d


class Hello():
    def __init__(self, a: int, b: str, c: World) -> None:
        self.a = a
        self.b = b
        self.c = c


class HelloFactory(Pyfta):
    class Meta:
        model = Hello

hw = HelloFactory()
# Will output the following
print(hw.a,   # 17
      hw.b,   # ajvumVRiMV
      hw.c.c, # 52.70540728114681
      hw.c.d) # gJzmUnmsIP
```

The more detailed your type annotations, the better
