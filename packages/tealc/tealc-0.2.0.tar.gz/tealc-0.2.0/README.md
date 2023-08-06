## tealc

`tealc` is a command-line **T**ension **E**stimate c**ALC**ulator for stringed
instruments. Users can calculate tensions for single strings or string sets.
Estimates are available for most common string materials for acoustic and
electric instruments. Tension estimates are based on published data from major
US string manufacturers.

Tensions estimates should be regarded as just that: *estimates* only,
approximate tensions under ideal conditions. Variations in acutal string length
due to bridge compensation, environmental conditions, string age, and and
manufacturing tolerances all affect the actual tension of a string. Use
estimates from `tealc` as a guide only.

## Requirements
The principal requirement is a working Python 3 installation or virtual
environment.

Officially, _only Linux and Windows are supported_. However, `tealc` can run on
other systems can run on other platforms such as the BSDs and macOS, provided:
1. the user has write permissions to the platform's (or environment's) Python
install directory (generally Scripts/), and
2. the install directory is on the user's `PATH`.

## Installation
```
python -m pip install -U tealc
```

## Usage
`tealc` contains these subcommands:
- `tealc string`: Calucate tension estimate for a single string.
- `tealc set`: Calculate tension estimates for a string set.
- `tealc file`: Calculate string set tension estimates from a file.
- `tealc materials`: Print a chart of string material codes and descriptions.
- `tealc help`: Open the tealc manual.

### tealc string
Usage: `tealc string [OPTIONS] GAUGE MATERIAL PITCH LENGTH`

#### REQUIRED
<dl>
  <dt>GAUGE</dt>
  <dd>
  String gauge in inches, 1/1000in, or mm with the <code>--si</code> flag. Inch gauges may
  optionally be in thousandths of an inch: <code>11</code> or <code>.011</code> are both valid and
  produce the same output.
  </dd>

  <dt>MATERIAL</dt>
  <dd>
  Short code for string construction material. Options:
    
  | code | material |
  | ---: | :------- |
  | ps | plain steel |
  | nps |  nickel plated steel wound |
  | pb | phosphor bronze wound |
  | 8020 | 80/20 bronze wound |
  | 8515 | 85/15 bronze wound |
  | ss | stainless steel roundwound |
  | fw | stainless steel flatwound |
  | pn | pure nickel wound |
  </dd>

  <dt>PITCH</dt>
  <dd>
  Tuned pitch of string in scientific pitch notation, from A0-E5.  Middle C is C4, and A440 is A4. Octaves change at C: A2, B2 is followed by C3, D3, ..., A3, B3, C4, ...

  Examples of open-string pitches in standard tunings:
  - Guitar: E2, A2, D3, G3, B3, E4
  - Bass: (B0), E1, A1, D2, G2
  - Mandolin/violin: G3, D4, A4, E5
  - Banjo: G4, D3, G3, B3, D4
  </dd>

  <dt>LENGTH</dt>
  <dd>
  Scale length of the instrument in inches, 1/1000in, or mm with the <code>--si</code> flag.
  </dd>
</dl>

#### OPTIONAL
<dl>
  <dt>--si</dt>
  <dd>
  Supply </code>gauge</code> and </code>length</code> arguments in millimenters.
  Tension is returned in kilograms (converted from pounds; used in place of Newtons.)
  </dd>
</dl>

#### EXAMPLES
```
tealc string .011 ps E4 25.5
```

```
tealc string --si 1.37 pb E2 632.5
```

### tealc set
usage: `tealc set [OPTIONS]

#### REQUIRED
<dl>
  <dt>-l, --length</dt>
  <dd>
  Scale length, just as in `tealc string`
  </dd>

  <dt>-s, --string &lt;GAUGE MATERIAL PITCH&gt;...</dt>
  <dd> 
  Repeated option, per string for the entire set. Requiremnts for the sub-arguments in `&lt;GAUGE MATERIAL PITCH&gt;` are just as in "tealc string".
  </dd>
</dl>

#### OPTIONAL
<dl>
  <dt>--si</dt>
  <dd>
  Supply set-wide --length and per-string GAUGE arguments in millimenters inctead of inches. Tension is returned in kilograms.
  </dd>

  <dt>--title TEXT</dt>
  <dd>
  An optional title for the output chart.
  </dd>
</dl>

#### EXAMPLES
```
tealc set -l 25.5 -s 10 ps e4 13 -s 13 ps b3 -s 17 ps g3 -s 26 nps d3 \
    -s 36 nps a3 46 -s 46 nps e2
```

```
tealc set -l 34 -s 45 bfw g2 -s 60 bfw d2 -s 80 bfw a1 -s 105 bfw e1 \
    --title "Bass Flatwound Mediums"
```

### tealc file
usage: `tealc file SETFILE`

#### REQUIRED:
<dl>
  <dt>SETFILE</dt>
  <dd>
  A file formatted using the format:
  ```
  length = LENGTH
  GAUGE MATERIAL PITCH
  [GAUGE MATERIAL PITCH]
  [...]
  [si = True or False]
  ```  
  
  An example SETFILE for a common set of light gauge ("10's") electric guitar strings on a Fender-scale instrument, with nickel plated steel wound strings, would look like this:
  ```
  length = 25.5
  10 ps e4
  13 ps b3
  17 ps g3
  26 nps d3
  36 nps a2
  46 nps e2
  ```

  The "length = ..." line and at least one "GAUGE MATERIAL PITCH" line are required.
  
  "si = False" is not required, and the SetFileParser.si attribute defaults to False if no "si = ..." line is included.
  </dd>
</dl>

#### OPTIONAL:
<dl>
  <dt>--si</dt>
  <dd>Show output chart units in mm/kg.</dd>
  <dt>--title TEXT</dt>
  <dd>An optional title for the output chart.</dd>
</dl>

#### EXAMPLE:
```
tealc file ~/path/to/setfile
```

### tealc materials
Print a chart of material codes and their descriptions.

### tealc help
Print a man page style help manual to the terminal (a formatted version of this
**Usage** section).

