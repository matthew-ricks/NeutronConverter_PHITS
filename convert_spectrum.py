#!/usr/bin/env python3
"""
Convert deuteron energy spectrum from CSV to PHITS e-type=22 format.
This script creates a histogram file for use with PHITS source definition.
"""

import csv
import os

def convert_spectrum_to_phits(input_csv, output_file):
    """
    Convert spectrum CSV to PHITS e-type=22 histogram format.
    
    PHITS e-type=22 format:
    - First line: number of energy bins
    - Following lines: energy_low  energy_high  probability
    
    The probability values are automatically normalized by PHITS.
    """
    energies = []
    fluxes = []
    
    with open(input_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                try:
                    energy = float(row[0])
                    flux = float(row[1])
                    energies.append(energy)
                    fluxes.append(flux)
                except ValueError:
                    continue
    
    if len(energies) < 2:
        raise ValueError("Need at least 2 data points")
    
    # Create histogram bins
    # Use midpoints between consecutive energy values as bin edges
    bins = []
    for i in range(len(energies) - 1):
        e_low = energies[i]
        e_high = energies[i + 1]
        # Average flux in this bin
        flux_avg = (fluxes[i] + fluxes[i + 1]) / 2.0
        bins.append((e_low, e_high, flux_avg))
    
    # Normalize probabilities (PHITS will renormalize anyway)
    total = sum(b[2] * (b[1] - b[0]) for b in bins)
    
    with open(output_file, 'w') as f:
        # Write PHITS e-type=22 format
        f.write(f"$ Deuteron energy spectrum for PHITS source\n")
        f.write(f"$ Converted from: {os.path.basename(input_csv)}\n")
        f.write(f"$ Energy range: {energies[0]:.4f} - {energies[-1]:.4f} MeV\n")
        f.write(f"$ Number of bins: {len(bins)}\n")
        f.write(f"$\n")
        f.write(f"$ Format: e-type=22 (user-defined histogram)\n")
        f.write(f"$ ne = number of bins\n")
        f.write(f"$ followed by: E_low  E_high  relative_intensity\n")
        f.write(f"$\n")
        f.write(f"    ne = {len(bins)}\n")
        
        for e_low, e_high, prob in bins:
            # Normalize to get relative probability
            norm_prob = prob / total if total > 0 else 1.0 / len(bins)
            f.write(f"    {e_low:.6e}  {e_high:.6e}  {norm_prob:.6e}\n")
    
    print(f"Converted {len(bins)} energy bins to {output_file}")
    print(f"Energy range: {energies[0]:.4f} - {energies[-1]:.4f} MeV")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    
    spectra = [
        ('spectrum_mean.csv', 'deuteron_spectrum.dat'),
        ('spectrum_lower.csv', 'deuteron_spectrum_lower.dat'),
        ('spectrum_upper.csv', 'deuteron_spectrum_upper.dat'),
    ]
    
    for input_name, output_name in spectra:
        input_path = os.path.join(base_dir, 'setup', input_name)
        output_path = os.path.join(script_dir, 'source', output_name)
        
        if os.path.exists(input_path):
            print(f"\nProcessing {input_name}...")
            convert_spectrum_to_phits(input_path, output_path)
        else:
            print(f"Warning: {input_path} not found, skipping")

if __name__ == '__main__':
    main()
