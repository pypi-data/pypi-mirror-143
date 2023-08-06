# PyHuTool
Python版HuTool

#### Setup
`pip install pyhutool`

#### Example Usage
Keyboard and Mouse Control
```
from pyhutool import Mouse
from pyhutool import Keybord
from pyhutool import Screenshot
from pyhutool import QRCode

# Mouse.click(500, 500)
# size = Mouse.size()
# position = Mouse.position()
# Mouse.leftClick(500, 500)

# Keybord.keyDown('h')
# Keybord.keyUp('h')
# Keybord.hotkey('ctrl', 'c')
# Keybord.press('h')
# Keybord.typewrite('hello world')
```

#### Screenshot Functions
```
# Screenshot.screenshot('test.png')
# locate = Screenshot.locateOnScreen('img_1.png')
```
#### QR Code
```
# QRCode.createQrcode('test', 'qrcode.png')
```