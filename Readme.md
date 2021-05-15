Small reverse engineering effort on controlling the Cooler Master Small ARGB Controller using python.

Notes are in reverse-engineer-argb.txt

This only works on firmware version v004 as of yet.

I am not sure what changed in firmware v008 as the new masterplus software does not support addressable rgb control


For firmware version v12:

Setting the amount of leds
======
`800d0201{checksum}{amount of leds}`
the checksum is calculated by doing `ceil(48/{amount of leds})`
eg: 8 leds: 48/8 = 6
So the command for 8 leds is: `800d02010608`


Setting a mode
======
- first the pc sends:
  `0801010002`
- The controller confirms with
  `0801010003`
- The pc sends:
  `080b0201{mode}`
where mode:
 - 0= motherboard
 - 1= spectrum
 - 2= reload
 - 3= recoil
 - 4= breathing
 - 5= refill
 - 6= demo
 - 7= custom (individual control)
 - 8= off
 - 9= static
- The controller confirms with
  `080b0300{mode}`

Setting individual leds
======
- First the mode is set to 7
- The pc sends:
  `0010020030{r1}{g1}{b1}....{r20}{g20}`
- The controller confirms with
  `0801010003`
- The pc sends:
  `01{b20}{r21}{g21}{b21}....{r41}{g41}`
- The pc sends:
  `82{b41}{r42}{g42}{b42}....{r48}{g48}{b48}`