# PyHuTool
Python版HuTool

#### Setup
`pip install pyhutool`

#### Example Usage
Keyboard and Mouse Control
```
    >>> import pyhutool
    >>> screenWidth, screenHeight = pyhutool.size() # Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
    >>> currentMouseX, currentMouseY = pyhutool.position() # Returns two integers, the x and y of the mouse cursor's current position.
    >>> pyhutool.moveTo(100, 150) # Move the mouse to the x, y coordinates 100, 150.
    >>> pyhutool.click() # Click the mouse at its current location.
    >>> pyhutool.click(200, 220) # Click the mouse at the x, y coordinates 200, 220.
    >>> pyhutool.move(None, 10)  # Move mouse 10 pixels down, that is, move the mouse relative to its current position.
    >>> pyhutool.doubleClick() # Double click the mouse at the
    >>> pyhutool.moveTo(500, 500, duration=2, tween=pyhutool.easeInOutQuad) # Use tweening/easing function to move mouse over 2 seconds.
    >>> pyhutool.write('Hello world!', interval=0.25)  # Type with quarter-second pause in between each key.
    >>> pyhutool.press('esc') # Simulate pressing the Escape key.
    >>> pyhutool.keyDown('shift')
    >>> pyhutool.write(['left', 'left', 'left', 'left', 'left', 'left'])
    >>> pyhutool.keyUp('shift')
    >>> pyhutool.hotkey('ctrl', 'c')
```

#### Screenshot Functions
