## tealc

`tealc` is a command-line tension estimator for stringed instruments. Users
can calculate tensions for single strings or string sets. Estimates are
available for most common string materials for acoustic and electric
instruments. Tension estimates are based on published data from major US string
manufacturers.

Tensions estimates should be regarded as just that: *estimates* only,
approximate tensions under ideal conditions. Variations in acutal string length
due to bridge compensation, environmental conditions, string age, and and
manufacturing tolerances all affect the actual tension of a string. Use
estimates from `tealc` as a guide only.

## Requirements
The principal requirement is a working Python 3 installation or virtual
environment.

Officially, _only Linux and Windows are supported_. However,
`tealc` can run on other systems can run on other platforms such as the BSDs
and macOS, provided:
1. the user has write permissions to the platform's (or
environment's) Python install directory (generally Scripts/), and
2. the install directory is on the user's `PATH`.

## Installation

### From PyPI
```
python3 -m pip install -U tealc
```
### From source
[Download a source
archive](https://github.com/davidelambert/tealc/archive/refs/heads/main.zip)
and unzip it or clone the GitHub repository with:
```
git clone https://github.com/davidelambert/tealc.git
```

In a terminal, navigate to the source code directory and run:
```
python3 -m pip install .
```

Note that source code installations may not be official releases and may be
more unstable than PyPI releases.

## Usage
tealc contains three primary subcommands: `tealc string`, `tealc set`,
and `tealc help`.

### tealc string
Estimate tension for a single string.

#### REQUIRED ARGUMENTS
<dl>
  <dt>gauge</dt>
  <dd>
  String gauge in inches, 1/1000in, or mm with the `--si` flag. Inch gauges may
  optionally be in thousandths of an inch: `11` or `.011` are both valid and
  produce the same output.
  </dd>

  <dt>material</dt>
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

  <dt>pitch</dt>
  <dd>
  Tuned pitch of string in scientific pitch notation, from A0-E5. Middle C is
  C4, and A440 is A4.
  
  Examples of open-string pitches in standard tunings:
  - Guitar: E2, A2, D3, G3, B3, E4
  - Bass: (B0), E1, A1, D2, G2
  - Mandolin/violin: G3, D4, A4, E5
  - Banjo: G4, D3, G3, B3, D4
  </dd>

  <dt>length</dt>
  <dd>
  Scale length of the instrument in inches, 1/1000in, or mm with the `--si`
  flag.
  </dd>
</dl>

#### OPTIONAL ARGUMENTS
<dl>
  <dt>--si</dt>
  <dd>
  Supply `gauge` and `length` arguments in millimenters. Tension is returned in
  kilograms (converted from pounds; used in place of Newtons.)
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
Estimate individual and total tensions for a string set. String sets may either
be entered on the command line or read from a "set file".

Set files use the following format:
```
[set]
length = LENGTH
gauges = G [G ...]
materials = M [M ...]
pitches = P [str ...]
si = true OR false (optional)
```

The `[set]` section header and all keys are required. Any other sections or
keys are ignored. Lists for gauges, materials, and pitches keys must be of
equal length. List items are space-separated. An example set file for a set of
medium-gauge electric guitar strings on a Fender-scale instrument, with nickel
plated steel wound strings, might look like:
```
[set]
length = 25.5
gauges = 11 15 18 26 36 50
materials = ps ps ps nps nps nps
pitches = e4 b3 d3 g3 a2 e2
```

When entering sets on the command line, `--gauges`, `--materials`, and
`--pitches` must have the same number of arguments.

#### ARGUMENTS
<dl>
  <dt>--file FILE</dt>
  <dd>
  A path to a valid set file. Any arguments other than `--title` are ignored if
  `--file` is present.
  </dd>

  <dt>--length LENGTH</dt>
  <dd> 
  Scale length of instrument in inches, 1/1000in, or mm with the `--si` flag.
  </dd>

  <dt>--gauges [G ...]</dt>
  <dd>
  List of string gauges in inches, 1/1000in, or mm with the `--si` flag.
  </dd>

  <dt>--materials [M ...]</dt>
  <dd>
  List of valid string material codes. Options: `ps`, `nps`, `pb`, `8020`,
  `8515`, `ss`, `fw`, `pn`
  </dd>

  <dt>--pitches [P ...]</dt>
  <dd>
  List of pitches in scientific pitch notation, from A0-E5. Middle C is C4, and
  A440 is A4.
  </dd>

  <dt>--si</dt>
  <dd>
  Supply --length and --gauges arguments in millimeters. String and set total
  tensions are returned in kilograms.
  </dd>

  <dt>--title TITLE</dt>
  <dd>
  Optional title for output chart.
  </dd>
</dl>

#### EXAMPLES
```
tealc set ~/path/to/set.txt
```

```
tealc set --length 25.5 --gauges 11 15 18 26 36 50 \
    --materials ps ps ps nps nps nps --pitches e4 b3 g3 d3 a2 e2
```

### tealc help
Print a man page style help manual to the terminal (a formatted version of this
**Usage** section).

