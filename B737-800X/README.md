# Keyset Creation Guide
Here are my tips I created in case you want a quick guide on how to set up or modify a keyset.
If you run into problems, there is a chance that you will find a hint here.

**I strongly reccomend learning by the pre-created ZIBO configuration** 

Use DataRefTool or similar to find names of the commands and datarefs.

*Do not forget* - each command consists of `begin`, `continue` and `end` phase.

Often a momentary switch is pressed by the `begin` phase, and released by `end` phase.

Or rotary switch is began rotating by `begin` phase, and the rotation ends with calling the `end` phase.

**USE `command` and `command-release` together with LUA handler for that.**

- actions.yaml is the root, your main screen will be here
- each .yaml preset cfg starts with `actions:` at the first line, 
followed by a set of keys
- the order of attributes doesn't matter
- you must define: `index` - 0-31 on Stream Deck XL
- `name` - you can name your button however you want, it should in
most cases be unique across all .yaml presets
- `type` - **dual** if it supports on/off commands, **single** if it is only command, **dir** if it should open
another directory
- `command-release` is for **single** type command
- if it is not supposed to be pushed (annunciator), set the type **none**
- if the button is type of **dir**, the preset to be opened is specified under the name of the button
- `return` set as a `name` of a **dir** will close the directory and switch back to its previous directory
 from which was the current one opened from
- `dataref-states` is by default set as 0.0 and 1.0
- if it is multi position, or simply the possible dataref position are different, then
set them as the dataref and button's images requires
- **the order matters!** for each `dataref-states` key will be taken `file-names` entry, both of course
must be the same size and correct order
- `file-names` doesn't have to be specified if the images are stored as
  `apuswitch.0.0.png`, `apuswitch.1.0.png`, `apuswitch.2.0.png` for equal `dataref-states` 
of *0.0*, *1.0*, *2.0* (if the `name` of the button is `apuswitch`)
- if the `dataref` is left blank, the `apuswitch.png` will be taken or the icon from `icon` parameter will be taken
  (`icon` is used for **dirs** too)
- although each dataref state is float, it is always rounded toward the smaller integer value (4.9 -> 4.0)
- the datarefs taken from game can be for processing **multiplied** by `dataref-multiplier`
- storing a dataref image as `apuswitch.0.5.png` if the dataref for middle position is `0.5` doesn't make sense.
Use `dataref-multiplier` of `2` and store it as `apuswitch.1.0.png`
- for example: annunciators (that are **on**) in ZIBO 737 start around 0.75, then proceed to rise to 1.0
... the files are though named as *0.0* and *1.0*, and i want to 0.75 display as on (1.0)! 
So I use `dataref-multiplier` of 1.5. 
- 0.75 * 1.5 = 1,125 -> (floored) -> **1.0**
- 1.00 * 1.5 = 1.5 -> (floored) -> **1.0**
- 0.00 * 1.5 = 0 -> (floored) -> 0.0
- Can be used for gauges too
- if it is scrolling/holding button, it will most probably need a LUA handler (more in the main README.md)
 and `command` and `command-release` button
- you can exec multiple commands by `commands` `commands-on` and `commands-off`!
- **dir** can have its icons as dataref too!
- the order of buttons doesn't matter, last item in .yaml can have index of 0
- you can set labels, which will be displayed under the icon (this is where the unique naming of button comes important)

## YAML tips
- the horizontal spacing matters a lot
- the order of attributes doesn't matter
