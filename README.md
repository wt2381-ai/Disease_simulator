# Epidemic Grid Simulator (`simulator.py`)

---

## Overview

This repository contains a Python-based cellular automaton simulation designed to model infectious disease spread across a 2D spatial grid. The program simulates disease dynamics—such as infection transmission, probability-based mortality, and recovery—and renders a live visualization of spatial disease progression over discrete time steps using `Matplotlib`.

---

## Key Features & Disease Dynamics

1. **Cell State Transitions**
   * **Susceptible (`S`):** Uninfected cells, represented in green.
   * **Infected (`I`):** Actively infected cells capable of spreading the virus to orthogonal neighbors after 1 time step, represented in red.
   * **Resistant / Deceased (`R`):** Cells that die based on a normal distribution mortality probability, represented in grey.
   * **Recovery:** Infected cells automatically recover back to a susceptible state after reaching the designated recovery time threshold.

2. **Probabilistic Mortality Model**
   * Calculates time-dependent death rates using numerical integration over a Gaussian (normal) probability density function (`normpdf`).

3. **Spatial Grid & Map Rendering**
   * Imports spatial coordinate data from CSV files (`nyc_map.csv`) to initialize a 150 x 150 grid map.
   * Generates real-time RGB matrix visualizations of epidemic spread across the grid.

---

## Required Dependencies

* `numpy`
* `matplotlib`

---

## How to Run

1. Ensure the input map file (`nyc_map.csv`) is present in the working directory.
2. Execute the simulator from your terminal:

```bash
python simulator.py
