# Keyset Creation Guide
Here are my tips I created in case you want a quick guide on how to set up or modify a keyset.
If you run into problems, there is a chance that you will find a hint here.

**I strongly recommend learning by the pre-created ZIBO configuration** 

## DataRefTool and How To

Use DataRefTool or similar to find names of the commands and datarefs.

*Do not forget* - each command consists of `begin`, `continue` and `end` phase.

Use the DataRefTool tool to find out if it needs to be commanded once, or commanded continuously.

Note that some buttons even not supposed to be momentary can also need those 2 handlers.

Often a momentary switch is pressed by the `begin` phase, and released by `end` phase.

Or rotary switch starts to rotate by `begin` phase, and the rotation ends with calling the `end` phase.

**USE `command` and `command-release` together with LUA handler for that.**

**Keysets / Directories**
- actions.yaml is the root, your main screen will be here
- each .yaml preset cfg starts with `actions:` at the first line, 
followed by a set of keys
- xyz.yaml, ABC.yaml, 123.yaml... *.yaml resembles the keysets (directories)
- keyset can be left unreferenced, it will be simply ignored and NOT loaded into memory

**Basics**
- the order of attributes doesn't matter
- you must define: `index` - 0-31 on Stream Deck XL
- `name` - you can name your button however you want, it should in
most cases be unique across all .yaml presets
- `type` - **dual** if it supports on/off commands, **single** if it is only command, **dir** if it should open
another directory
- `icon` for static (directories, simple buttons) or if it follows the `dataref-states` logic
- `dataref-states` is set to *0.0* and *1.0* if not specified otherwise
- alternative to `icon` is `file-names`
- **the order of `file-names` matters!** For each `dataref-states` key will be taken `file-names` entry, both of course
must be the same size and correct order
- `file-names` doesn't have to be specified if the images are stored as
  `apuswitch.0.0.png`, `apuswitch.1.0.png`, `apuswitch.2.0.png` for equal `dataref-states` 
of *0.0*, *1.0*, *2.0* (if the `name` of the button is `apuswitch`)
- if the `dataref` is left blank, the `apuswitch.png` will be taken by the `icon` parameter 
  (`icon` is used for **dirs** too)

**More Basics of Buttons**
- `command-release` is for **single** type command
- if it is not supposed to be pushed (annunciator), set the type **none**
- if the button is type of **dir**, the preset to be opened is specified under the name of the button
- `return` set as a `name` of a **dir** will close the directory and switch back to its previous directory
 from which was the current one opened from

**Important Rounding Quirk of xplane-streamdeck**
- **although each dataref state is float, it is always rounded toward the smaller integer value (4.9 -> 4.0)**
- the datarefs taken from sim can be for processing **multiplied** by `dataref-multiplier`
- storing a dataref image as `apuswitch.0.5.png` if the dataref for middle position is `0.5` doesn't make sense.
Use `dataref-multiplier` of `2` and store it as `apuswitch.1.0.png` (rounding down!!!)
- for example: annunciators (that are **on**) in ZIBO 737 start around 0.75, then proceed to rise to 1.0
... the files are though named as *0.0* and *1.0*, and I want to 0.75 display as on (1.0)! 
So I use `dataref-multiplier` of 1.5. 
- 0.75 * 1.5 = 1,125 -> (floored) -> **1.0**
- 1.00 * 1.5 = 1.5 -> (floored) -> **1.0**
- 0.00 * 1.5 = 0 -> (floored) -> 0.0
- Can be used for gauges too, *I use it for Zibo flaps*
****
- if it is scrolling/holding button, it will most probably need a LUA handler (more in the main README.md)
 and `command` and `command-release` button
- you can exec multiple commands at once by `commands` (for `type` **single**) 
- `commands-on` and `commands-off` (for `type` **dual**)
- **dir** can have its `icon` `file-names` `dataref-states` too (can look like any button)!
- the order of buttons doesn't matter, last item in .yaml can have index of 0
- you can set labels, which will be displayed under the icon (this is where the unique naming of button comes important)
- labels follow predefined font in `config.yaml`. Displays use custom font.

#### Lua Handler Explained
A lot of buttons in the flight deck are momentary switches and buttons, which are expected to be held in position.
For that purpose, I have built a small LUA file with custom commands in `misc/streamdeck_handlers.lua`.
The momentary switches work on a way that the `command_begin` executes the `begin` part of the command, 
which switches it into the desired position, and `command_end` which returns the switch/button back into its 
stable position (also known as the `end` part of the command). 

So, the bad news is that you have to create two commands for your each `begin` and `end` action everytime.

The X-Plane UDP protocol is limited in this way, the UDP protocol is able to execute only all 3 parts of the
command (yes, 3.. begin, continue, end), so I recommend solving it this way. You will map those two commands 
from the LUA handler in the`command` and `command-release` YAML configuration. 
Look for examples in `actions.yaml`, where it is used on fire warning or master caution of the 737 etc.

#### Gauge Example
```
gauge:
  name: name it however you want, i recommend the same name for same configurations 
        (to pregenerate the graphics only once for same graphic set)
  needle-center:
    x: x center of needle
    y: y center of needle
  background: background image name without containing folder and .png suffix
  needle: needle image name without containing folder and .png suffix
  range-degrees: how much will it rotate in degrees?
  min: minimal value of the dataref
  max: maximum value of the dataref
  step: how precise should it be? 1-(infinity) allowed. Smaller number = more precise.
```
If the dataref is e.g. from 0.0 to 1.0, use dataref-multiplier of 100, remember how every dataref value is rounded down

#### Display Example
```
display:
  name: name it however you want, i recommend the same name for same configurations 
        (to pregenerate the graphics only once for same graphic set)
  text-center:
    x: 'center' or number (0-96) NOTE: center doesnt have to centered, font's have height that offsets it
    y: 'center' or number (0-96) NOTE: center doesnt have to centered, font's have height that offsets it
  font-path: I recommend consola.ttf as the MS33558 doesn't support '-' before negative numbers
  font-size: ....
  zero-pad: how much should the dataref number be zero padded? number of characters total
  min: minimum number for which the display will be generated
  max: maximum number for which the display will be generated
  step: steps between numbers...
        can be 1 for speed and heading selector, 100 for altitude selectors, 50 for V/S etc.
  color: CSS color name of the text
  keep-decimal: keep the decimal point? True / False
  background: background image name without containing folder and .png suffix
```
Can be used together with `dataref-multiplier`, too.
## YAML tips
- the horizontal spacing matters a lot
- the order of attributes doesn't matter
- try to follow the syntax flow of the original 
- or find examples/tutorials using your favorite search engine

## End of The Day Tips
- creating configurations should be fun! you can do it in long haul cruise or as I did - on the ground
- learning from examples is one, if not the best, learning method.. check out the original Zibo one!
- developers of the planes can be quirky, sometimes their names doesn't make sense, simple buttons need handlers, 
they need to be multiplied by *1.5* or *-1.0* to make sense in the program's round down logic
- this program can be quirky too, configurate few buttons and try to launch it before continuing...
to save yourself finding the problematic one. Wrong configuration can cause crashes with poor error descriptions :/
- muscle memory will do its thing, fly the plane with the stream deck a few times and you will get used to it ;)
- if you create a handy configuration, submit a pull request, and let others fly it too!