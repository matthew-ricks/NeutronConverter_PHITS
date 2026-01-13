# PHITS Neutron Converter Simulation

This directory contains a PHITS (Particle and Heavy Ion Transport code System) simulation converted from the original Geant4 NeutronConverter simulation. The simulation models neutron production from a deuteron beam impinging on a 9Be target.

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Physics Description](#physics-description)
4. [Geometry Configuration](#geometry-configuration)
5. [Source Definition](#source-definition)
6. [Input Files](#input-files)
7. [Output Files and Tallies](#output-files-and-tallies)
8. [Running the Simulation](#running-the-simulation)
9. [Configuration Options](#configuration-options)
10. [Comparison with Geant4](#comparison-with-geant4)

---

## Overview

This simulation studies neutron production via the 9Be(d,n) reaction. A deuteron beam with a measured energy spectrum strikes a beryllium target, producing neutrons that can be tracked and scored using various tallies.

### Key Features:
- Deuteron beam with experimentally measured energy spectrum (0.46 - 8.0 MeV)
- Gaussian angular distribution (FWHM = 11.7°)
- 9Be target disk (1 inch diameter, 1 mm thick)
- Optional center hole in target
- Optional aluminum degrader
- Optional stainless steel shielding cylinder
- Comprehensive neutron scoring tallies

---

## Directory Structure

```
phits/
├── neutron_converter.inp          # Main input file (solid Be disk)
├── neutron_converter_hole.inp     # Be disk with center hole
├── neutron_converter_full.inp     # Full geometry (Be + Al + Steel)
├── neutron_converter_mono.inp     # Monoenergetic source for testing
├── convert_spectrum.py            # Spectrum conversion utility
├── README.md                      # This file
├── source/
│   ├── deuteron_spectrum.dat      # Mean spectrum (PHITS format)
│   ├── deuteron_spectrum_lower.dat # Lower bound spectrum (mean - 1σ)
│   └── deuteron_spectrum_upper.dat # Upper bound spectrum (mean + 1σ)
└── output/
    └── [simulation outputs]       # Generated during runs
```

---

## Physics Description

### Reaction of Interest
The primary physics process is the 9Be(d,n)10B reaction:
- **d + 9Be → 10B + n**

This reaction has a Q-value of approximately +4.36 MeV, making it effective for neutron production even at low deuteron energies.

### PHITS Physics Models
PHITS uses several physics models for this simulation:

| Physics Process | PHITS Model |
|----------------|-------------|
| Nuclear reactions | INCL/JQMD + evaporation |
| Neutron transport | Data-driven (JENDL, ENDF) |
| Ionization | ATIMA/SPAR |
| Electron/photon | EGS5 (negs=1) |

### Data Libraries
The simulation uses nuclear data libraries specified by `nucdata=1`:
- JENDL-4.0 for neutron cross-sections
- Nuclear reaction data for d+Be

---

## Geometry Configuration

### Coordinate System
- **Origin**: (0, 0, 0) - location of deuteron source
- **Beam direction**: +Z axis
- **Be target center**: z = 3.95 cm (39.5 mm from source)

### Components

#### 1. Beryllium Target
| Parameter | Value |
|-----------|-------|
| Material | 9Be (100% isotopic) |
| Density | 1.848 g/cm³ |
| Outer diameter | 25.4 mm (1 inch) |
| Thickness | 1.0 mm |
| Center hole (optional) | 1.5875 mm dia (1/16 inch) |
| Position | z = 39.0 - 40.0 mm |

#### 2. Aluminum Slab (optional)
| Parameter | Value |
|-----------|-------|
| Material | Aluminum |
| Density | 2.699 g/cm³ |
| Diameter | 25.4 mm (matches Be) |
| Thickness | 3.0 mm |
| Center hole | 1.5875 mm (matches Be) |
| Position | z = 36.0 - 39.0 mm |

#### 3. Stainless Steel Cylinder (optional)
| Parameter | Value |
|-----------|-------|
| Material | SS304 (Fe/Cr/Ni/Mn) |
| Density | 8.0 g/cm³ |
| Inner radius | 631.825 mm |
| Outer radius | 638.175 mm |
| Length | 368.3 mm |
| Orientation | Axis along X (rotated 90°) |
| Center | Coincident with Be target |

---

## Source Definition

### Particle Type
- **Projectile**: Deuteron (d)
- **Charge**: +1
- **Mass**: 2.014 amu

### Energy Distribution
Three spectrum options are provided:

| Spectrum | File | Description |
|----------|------|-------------|
| Mean | `deuteron_spectrum.dat` | Central value |
| Lower | `deuteron_spectrum_lower.dat` | Mean - 1σ |
| Upper | `deuteron_spectrum_upper.dat` | Mean + 1σ |

**Energy range**: 0.46 - 8.0 MeV

### Angular Distribution
- **Type**: Gaussian cone around +Z axis
- **FWHM**: 11.7 degrees
- **σ (sigma)**: 4.97 degrees
- **PHITS parameters**: `dir=cos(11.7)`, `dom=-4.97`

### Position
- **Type**: Point source
- **Location**: (0, 0, 0)

---

## Input Files

### Main Input Files

| File | Geometry | Description |
|------|----------|-------------|
| `neutron_converter.inp` | Solid Be disk | Default configuration |
| `neutron_converter_hole.inp` | Be disk with hole | 1/16" center hole |
| `neutron_converter_full.inp` | Complete | Be + Al slab + Steel cylinder |
| `neutron_converter_mono.inp` | Solid Be | Monoenergetic source (1 MeV default) |

### Input File Sections

Each input file contains these PHITS sections:

```
[Title]      - Simulation title
[Parameters] - Run control and physics options
[Source]     - Deuteron beam definition
[Material]   - Material compositions
[Surface]    - Geometry surface definitions
[Cell]       - Cell (region) definitions
[T-Track]    - Track length (flux) tallies
[T-Cross]    - Surface crossing tallies
[T-Product]  - Particle production tallies
[T-Deposit]  - Energy deposition tallies
[T-Yield]    - Particle yield tallies
[T-Time]     - Time distribution tallies
[End]        - End of input
```

---

## Output Files and Tallies

### Tally Descriptions

| Tally | Purpose | Output File |
|-------|---------|-------------|
| T-Track (xy) | Neutron flux in X-Y plane | `neutron_track_xy.out` |
| T-Track (xz) | Neutron flux in X-Z plane | `neutron_track_xz.out` |
| T-Cross | Escaping neutron spectrum | `neutron_escape_spectrum.out` |
| T-Cross (angle) | Angular distribution | `neutron_angular_dist.out` |
| T-Product | Production spectrum | `neutron_production_spectrum.out` |
| T-Time | Time distribution | `neutron_time_dist.out` |
| T-Deposit | Energy deposition | `energy_deposit_Be.out` |
| T-Yield | Particle yields | `particle_yields.out` |

### Output Formats

- `.out` files: ASCII data tables
- `.eps` files: PostScript plots (when `epsout=1`)
- `phits.out`: Main output summary
- `phits.log`: Detailed run log

---

## Running the Simulation

### Prerequisites

1. **PHITS Installation**: PHITS must be installed on your system
   - Obtain PHITS from JAEA: https://phits.jaea.go.jp/
   - PHITS requires a license (free for academic use)
   
2. **Environment Setup**: Configure your shell environment
   ```bash
   # Add to your ~/.bashrc or ~/.bash_profile
   export PHITSPATH=/path/to/phits
   export PATH=$PHITSPATH/bin:$PATH
   
   # Verify installation
   which phits
   phits --version
   ```

3. **Nuclear Data Libraries**: Ensure data paths are set
   ```bash
   # PHITS typically sets these automatically, but verify:
   export DATAPATH=$PHITSPATH/data
   ```

### Step-by-Step Instructions

#### 1. Navigate to the simulation directory
```bash
cd /home/mttricks/NeutronConverter_PHITS/phits
```

#### 2. Choose your input file

| Input File | Configuration |
|------------|---------------|
| `neutron_converter.inp` | Solid Be disk (default) |
| `neutron_converter_hole.inp` | Be disk with 1/16" center hole |
| `neutron_converter_hole_cyl.inp` | Be disk with hole + steel cylinder |
| `neutron_converter_full.inp` | Full geometry (Be + Al + steel) |
| `neutron_converter_mono.inp` | Monoenergetic source (testing) |

#### 3. Run the simulation

**Basic execution:**
```bash
phits < neutron_converter.inp
```

**With explicit output redirection:**
```bash
phits < neutron_converter.inp > run.log 2>&1
```

**Run in background:**
```bash
nohup phits < neutron_converter.inp > run.log 2>&1 &
```

#### 4. Monitor progress

While running, PHITS displays progress. You can also check:
```bash
# View the log file
tail -f output/phits.log

# Check if still running
ps aux | grep phits
```

#### 5. View results

After completion, outputs are in the `output/` directory:
```bash
ls -la output/

# View a tally result
cat output/neutron_production_spectrum.out

# View geometry plots (if you have an EPS viewer)
evince output/geometry_xz.out.eps
# or convert to PNG
convert output/geometry_xz.out.eps output/geometry_xz.png
```

### Parallel Execution (MPI)

For faster execution with multiple CPU cores:

```bash
# Run with 4 MPI processes
mpirun -np 4 phits < neutron_converter.inp

# Run with all available cores
mpirun -np $(nproc) phits < neutron_converter.inp

# On a cluster with SLURM
srun -n 16 phits < neutron_converter.inp
```

**Note:** MPI requires PHITS to be compiled with MPI support.

### Adjusting Simulation Parameters

#### Number of Histories (Statistics)

Edit the `[Parameters]` section:
```
maxcas = 1000000   $ Number of histories per batch
maxbch = 10        $ Number of batches
```
Total particles = maxcas × maxbch = 10,000,000

**Recommendations:**
- Quick test: `maxcas=10000, maxbch=1` (~10 seconds)
- Standard run: `maxcas=100000, maxbch=10` (~minutes)
- Production: `maxcas=1000000, maxbch=100` (~hours)

#### Geometry Check Only (No Transport)

To verify geometry without running particles:
```
icntl = 8    $ Geometry check mode
```

This generates geometry plots quickly without particle transport.

### Example: Complete Run Workflow

```bash
# 1. Go to simulation directory
cd /home/mttricks/NeutronConverter_PHITS/phits

# 2. Clean previous outputs (optional)
rm -f output/*.out output/*.eps output/*.log

# 3. Run simulation
phits < neutron_converter_hole_cyl.inp

# 4. Check for errors
grep -i "error\|warning" output/phits.log

# 5. View results
cat output/neutron_production_spectrum_hole_cyl.out

# 6. Convert plots to viewable format
for f in output/*.eps; do
    convert "$f" "${f%.eps}.png"
done

# 7. Open geometry plot
xdg-open output/geometry_xz_hole_cyl.png
```

### Expected Runtime

| Configuration | Histories | Estimated Time |
|---------------|-----------|----------------|
| 1,000 | 1,000 | ~1 second |
| 100,000 | 100,000 | ~30 seconds |
| 1,000,000 | 1,000,000 | ~5 minutes |
| 10,000,000 | 10,000,000 | ~30-60 minutes |
| 100,000,000 | 100,000,000 | ~5-10 hours |

*Times are approximate and depend on hardware and geometry complexity.*

Total histories = maxcas × maxbch

---

## Configuration Options

### Changing the Energy Spectrum

To use a different spectrum, edit the `[Source]` section:

```
$ Mean spectrum (default)
file = source/deuteron_spectrum.dat

$ Lower bound spectrum
file = source/deuteron_spectrum_lower.dat

$ Upper bound spectrum
file = source/deuteron_spectrum_upper.dat
```

### Monoenergetic Source

For a monoenergetic beam, use `neutron_converter_mono.inp` and edit:

```
e-type = 1          $ Monoenergetic
e0     = 2.0        $ Energy in MeV (change this value)
```

### Modifying Geometry

#### Enable/Disable Components

In the `[Cell]` section, comment/uncomment cells:

```
$ Enable Al slab (uncomment this line)
    3   3  -2.699   30 -31 32 -33

$ Enable steel cylinder (uncomment this line)
    4   4  -8.0     40 -41 42 -43
```

#### Solid Disk vs Disk with Hole

For solid disk, use surfaces 10-12:
```
2   2  -1.848   10 -11 -12       $ Solid Be disk
```

For disk with hole, use surfaces 20-23:
```
2   2  -1.848   20 -21 22 -23    $ Be annulus with hole
```

### Changing Beam Angular Spread

Edit the `[Source]` section:
```
dir = cos(11.7)    $ Reference angle (degrees)
dom = -4.97        $ Negative = Gaussian sigma in degrees
                   $ For FWHM, sigma = FWHM / 2.355
```

For a pencil beam:
```
dir = 1.0          $ Along +z
dom = 1            $ All in forward hemisphere
```

---

## Comparison with Geant4

### Key Differences

| Aspect | Geant4 | PHITS |
|--------|--------|-------|
| Physics | QGSP_BIC_AllHP | INCL/evaporation + data |
| Data | G4NDL, ParticleHP | JENDL, ENDF |
| Geometry | C++ classes | Text input (surfaces/cells) |
| Source | C++ sampling | Built-in distributions |
| Tallies | SteppingAction | Built-in tally sections |
| Units | mm, MeV | cm, MeV |

### Unit Conversions

**Important**: PHITS uses centimeters, while Geant4 used millimeters.

| Parameter | Geant4 (mm) | PHITS (cm) |
|-----------|-------------|------------|
| Be target z | 39.5 | 3.95 |
| Be thickness | 1.0 | 0.10 |
| Be radius | 12.7 | 1.27 |
| Hole radius | 0.79375 | 0.079375 |
| Al thickness | 3.0 | 0.30 |

### Physics Equivalence

The Geant4 simulation used:
- `G4HadronPhysicsQGSP_BIC_AllHP` for hadronic physics
- `G4ParticleHP` for high-precision neutron/proton transport
- Binary Cascade (BIC) for nucleon-nucleus reactions

PHITS equivalently uses:
- INCL (Liège Intranuclear Cascade) model
- Generalized Evaporation Model
- Evaluated nuclear data libraries

Results may differ slightly due to different nuclear models and data libraries.

---

## Troubleshooting

### Common Issues

1. **"Cannot find data file"**
   - Ensure spectrum files are in the `source/` directory
   - Check file paths in `[Source]` section

2. **"Cell overlap error"**
   - Verify cell definitions don't overlap
   - Use `icntl=8` for geometry check only

3. **"Unknown particle"**
   - Verify `proj = deuteron` is spelled correctly
   - Check PHITS version supports deuterons

4. **Low statistics**
   - Increase `maxcas` and/or `maxbch`
   - Use parallel execution

### Geometry Visualization

To generate a geometry plot without running transport:
```
icntl = 8    $ Geometry check only
```

This creates geometry check outputs without particle transport.

---

## References

1. PHITS User Manual: https://phits.jaea.go.jp/
2. JENDL Nuclear Data Library: https://wwwndc.jaea.go.jp/jendl/
3. 9Be(d,n) cross-section data: EXFOR database
4. Original Geant4 code: `/home/mttricks/NeutronConverter_PHITS/` (archived)

---

## Contact

For questions about this simulation conversion, please contact the project maintainer.

---

*Last updated: January 2026*
*Converted from Geant4 to PHITS*
