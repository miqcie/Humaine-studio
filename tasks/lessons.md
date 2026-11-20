# Lessons

## 2026-11-19: Virginia bird icons (design-system/birds)

- **Do not draw animal anatomy from coordinates.** 30 birds drawn as SVG primitives from memory read as one template: a circle head on a separate hump. The Kestrel failed four times. Get the form from a raster draft (image model), then trace it into the palette with potrace (`design-system/birds/trace_icon.py`, the same method as `trace_curlew.py`).
- **Measure proportions on reference photos before drawing.** The Black Skimmer's bill was about twice the head length. A photo shows about 1.3 to 1.5 times. Use photos to measure only. Do not trace them or commit them.
- **Read the brief's color rule literally.** It says to favor navy silhouettes. The first set used blue, red, grey and yellow bodies.
- **Do not add rules that are not in the brief.** "Pale plumage never touches the field" added keylines and rings. The brief does not ask for it, and negative-space white lines read better.
- **Checks prove compliance, not likeness.** Palette, clearance and label asserts passing is not progress on the art. Look at the images at 96 px against references before reporting.
- **Show the style pilots before scaling up.** Style is the user's decision. Present 3 to 6 pilots, then draw the rest.
- **An image judge ranks better than it gates.** TypeSafe Jev put Chris's blind best pick first for 5 of 5 birds, but as a gate it flags 16 of 30 icons: 9 of 10 flags outside the known errors were false alarms or the brand palette ("colors not true to species"), and it missed 4 of 5 minor errors. Sort variations with it; verify any flag by eye before calling it a false alarm or a catch.
- **Keep calibration questions generic.** The "avoid" lists were written from the review of the known errors, so hits on them are partly built in. Report the verdict without them too (5 of 6 versus 6 of 6).
