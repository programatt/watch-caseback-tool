# Watch case-back tool generator

A dependency-free Python CLI that creates printable STL opening disks for evenly
spaced, rectangular case-back notches, plus a reusable handle. OpenSCAD performs
the final solid export.

## Measurement convention

The **notch circle diameter** is the pitch-circle diameter through the centre of
each notch footprint. Looking down at the case back:

- `notch-length` is radial.
- `notch-width` is tangential.
- `notch-depth` is axial (how far the tooth enters the case-back notch).
- `notch-count` assumes equal angular spacing.

Measure the watch itself with calipers. Printed fit varies by printer and
material, so make a low-infill test disk before applying torque to a watch.

## Run

Requires Python 3.10+ and OpenSCAD on `PATH`. No Python packages are required:

```bash
cd /home/matt/watch-caseback-tool
./caseback-tool --help
```

An optional editable installation provides the command globally on systems with
setuptools available:

```bash
python3 -m pip install -e .
```

## Generate a disk

```bash
./caseback-tool disk \
  --notch-circle-diameter 31.0 \
  --notch-count 6 \
  --notch-depth 1.2 \
  --notch-length 1.6 \
  --notch-width 2.4 \
  --disk-diameter 34.6 \
  --output skx_caseback_disk.stl
```

The command writes both `skx_caseback_disk.stl` and its editable parametric
source, `skx_caseback_disk.scad`.

## Generate the handle

```bash
./caseback-tool handle --output caseback_handle.stl
```

All disks and the default handle use the same 12 mm across-flats hex drive. The
hex carries opening and closing torque in both directions. The disk has a 5.6 mm
pilot pocket, 5.5 mm deep, for a common M4 heat-set insert; an M4 x 6 mm
button-head screw through the handle provides positive retention. Confirm the
recommended pilot diameter for your particular insert. Adjust `--fit-clearance`
if your printer makes the socket too tight or loose.

## Seiko SKX fit-check example

```bash
./caseback-tool skx-example --output-dir examples/skx
```

This creates the disk STL, handle STL, editable SCAD sources, and JPG renders.
The sample starts from a 33 mm SKX case-back outside diameter and six-notch
layout, but the exact notch footprint is an engineering fit assumption:

- 31.0 mm notch pitch circle
- 6 notches
- 1.2 mm axial depth
- 1.6 mm radial length
- 2.4 mm tangential width

Seiko's service literature confirms the six-notch screw-back arrangement, but
does not publish this notch footprint. Verify these five values on your own
case back before use; aftermarket SKX-compatible backs can differ.

## Printing and use

- Print the disk with the teeth on the build plate and the handle flat.
- Use PETG, nylon, or a filled engineering polymer; 5+ perimeters and high infill
  around the drive are recommended.
- Deburr the teeth, test engagement by hand, and keep the tool square to the back.
- Secure the watch in a proper case holder. Mask polished surfaces if needed.
- After opening a water-resistant watch, inspect/lubricate the gasket and pressure
  test the watch before relying on its water resistance.
- This is a printable shop aid, not a calibrated torque tool.

## License

MIT
