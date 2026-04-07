
# Cross-View Landmark Recognition (CLR) for Cooperative Visual Navigation

This repository contains the official dataset, evaluation code, and benchmark results for the paper:

> **Cross-View Landmark Recognition for Cooperative Visual Navigation**  
> *Nasim Paykari, Ilayda Vural, Natnael Desta, Ademi Zain, Taylor Clark, Mohamed Rahouti, Damian Lyons*  
> Department of Computer and Information Science, Fordham University, NY, USA  
> ...

---

## Purpose of This Work

**Cross-View Landmark Recognition (CLR)** addresses a fundamental challenge in multi-robot navigation: enabling robots to recognize the same landmark when viewed from dramatically different perspectives, distances, and viewing angles.

Unlike traditional **Visual Place Recognition (VPR)** which asks *"Are we in the same place?"* (assuming spatial proximity), CLR asks *"Can you see what I see?"* — focusing on identifying shared perceptual anchors rather than co-located positions.

### Key Applications
- **Search and rescue missions** in GNSS-denied environments
- **Urban canyons and forests** where GPS signals are unreliable
- **Warehouse automation** with multiple robots sharing visual references
- **Multi-robot exploration** without overlapping fields of view

### What This Repository Provides
1. **CLR Dataset**: 220 query images and 328 reference images from Google Landmarks v2
2. **Benchmark Results**: Performance evaluation of 8 VPR methods
3. **Precomputed Matches**: Similarity matrices for all methods (VPR-Bench format)
4. **Interactive Analysis Tools**: Query any landmark and compare all methods

---

## Repository Structure

```
Cross_View_Landmark_Recognition/
│
├── data/
│   ├── CLR_dataset/
│   │   ├── query/           # 220 query images
│   │   ├── reference/       # 328 reference images
│   │   └── ground_truth_new.npy   # Query-reference mappings
│   │
│   └── corridor/
│       └── ground_truth_new.npy    # Corridor dataset ground truth
│
├── precomputed_matches/
│   ├── CLR_dataset/
│   │   ├── AlexNet_VPR/
│   │   │   └── precomputed_data_corrected.npy
│   │   ├── AMOSNet/
│   │   │   └── precomputed_data_corrected.npy
│   │   ├── CALC/
│   │   │   └── precomputed_data_corrected.npy
│   │   ├── CoHOG/
│   │   │   └── precomputed_data_corrected.npy
│   │   ├── HOG/
│   │   │   └── precomputed_data_corrected.npy
│   │   ├── HybridNet/
│   │   │   └── precomputed_data_corrected.npy
│   │   ├── NetVLAD/
│   │   │   └── precomputed_data_corrected.npy
│   │   └── RegionVLAD/
│   │       └── precomputed_data_corrected.npy
│   │
│   └── corridor/
│       ├── AlexNet_VPR/
│       │   └── precomputed_data_corrected.npy
│       └── ... (same structure for all methods)
│
├── results/                  # Paper results (tables, figures)
│   ├── clr_performance.csv
│   ├── discrimination_metrics.csv
│   ├── efficiency.csv
│   ├── recall_all_methods.pdf
│   └── rank_cdf_all_methods.pdf
│
├── scripts/
│   ├── interactive_clr_analyzer.py   # Main interactive tool
│   ├── clr_analysis.py               # CLR dataset analysis
│   ├── corridor_analysis.py          # Corridor dataset analysis
│   └── generate_figures.py           # Reproduce paper figures
│
├── README.md
├── LICENSE
└── requirements.txt
```

---

## Ground Truth Format

### CLR Dataset (`data/CLR_dataset/ground_truth_new.npy`)

The ground truth is stored as a numpy array where each entry is:
```
[query_index, [reference_indices]]
```

**Example:**
```python
[57, [84, 85, 86]]  # Query 57 matches references 84, 85, 86
[74, [106, 107, 108, 109, 110]]  # Query 74 matches 5 references
[137, [226]]  # Single reference (sanity check)
```

### Query-Reference Assignment (Randomized)

For each location, we **randomly selected one image as the query** and designated **all remaining images as references**. This split is reproducible and recorded in the ground truth file.

**Note:** A self-match (image serving as both query and reference) is intentionally included to validate the experimental pipeline, inflating precision by approximately 0.45% — a negligible effect.

---

## 📊 Dataset Statistics

| Metric | Value |
|--------|-------|
| Total queries | 220 |
| Total references | 328 |
| Total images | 548 |
| Single-ref queries | 143 (65%) |
| Multi-ref queries | 77 (35%) |
| Max references per query | 9 |
| Average references per query | 1.49 |

---

## Quick Start

### 1. Clone the repository

```bash
git clone -b clr-benchmark https://github.com/nasimpaykari/Cross_View_Landmark_Recognition.git
cd Cross_View_Landmark_Recognition
```

### 2. Run the interactive query analyzer

```bash
python interactive_clr_analyzer.py
```

Then enter a query index (0-219) to see:
- Ground truth references
- Top-1 predictions for all 8 methods
- Per-reference rank and score analysis
- Color-coded comparison summary

### 3. Run CLR dataset analysis

```bash
python clr_analysis.py
```

### 4. Run CLR/Corridor dataset analysis (baseline)

```bash
python analysis.py
```

Outputs saved to `results/` directory.

---

## 📈 Key Results Summary

| Method | CLR R@1 | Corridor R@1 | Drop | AUC ROC |
|--------|---------|--------------|------|---------|
| **NetVLAD** | **56.82%** | 67.57% | -10.7% | **93.01%** |
| RegionVLAD | 28.64% | 43.24% | -14.6% | 82.05% |
| HybridNet | 26.36% | 90.09% | -63.7% | 77.76% |
| CoHOG | 25.00% | 3.60% | **+21.4%** | 68.07% |
| AMOSNet | 22.73% | 84.68% | -62.0% | 76.22% |
| AlexNet_VPR | 9.55% | 69.37% | -59.8% | 67.67% |
| CALC | 5.00% | 4.50% | +0.5% | 65.19% |
| HOG | 1.82% | 47.75% | -45.9% | 56.65% |

---

## Precomputed Data Format

Each method folder contains `precomputed_data_corrected.npy` with the following structure:

```python
data[0] = query_indices    # Array of query indices
data[1] = predictions      # Top-1 predictions for each query
data[2] = scores           # Similarity scores for top-1 predictions
data[3] = similarity_matrix # Full similarity matrix (queries × references)
```

---

## Citation

If you use this dataset or code in your research, please cite:

```bibtex
@inproceedings{...,
  title={Cross-View Landmark Recognition for Cooperative Visual Navigation},
  author={Paykari, Nasim and Vural, Ilayda and Desta, Natnael and Zain, Ademi and Clark, Taylor and Rahouti, Mohamed and Lyons, Damian},
  ...
}
```

---

## Contact

- **Nasim Paykari**: npaykari@fordham.edu
- **Damian Lyons**: dlyons@fordham.edu
- **Mohamed Rahouti**: mrahouti@fordham.edu

Or open a [GitHub Issue](https://github.com/nasimpaykari/Cross_View_Landmark_Recognition/issues).

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Google Landmarks v2** for source images
- **VPR-Bench** authors for the evaluation framework
- **SPIE** for publication

---

## Star This Repository

If you find this work useful, please consider starring this repository and citing our paper.


---
