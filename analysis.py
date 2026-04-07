# -*- coding: utf-8 -*-
"""
Consolidated plots:
- One figure for all methods: Rank CDF comparison
- One figure for all methods: Recall@K comparison
- Both plots compare corridor vs CLR_dataset

Python 3 compatible
"""

from __future__ import print_function
import os
import numpy as np
import matplotlib.pyplot as plt

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['lines.linewidth'] = 2.2

# ================= CONFIG =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "results")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Dataset paths
DATASETS = {
    "corridor": {
        "path": os.path.join(BASE_DIR, "precomputed_matches", "corridor"),
        "gt": os.path.join(BASE_DIR, "datasets", "corridor", "ground_truth_new.npy")
    },
    "CLR_dataset": {
        "path": os.path.join(BASE_DIR, "precomputed_matches", "CLR_dataset"),
        "gt": os.path.join(BASE_DIR, "datasets", "CLR_dataset", "ground_truth_new.npy")
    }
}

METHODS = [
    "AlexNet_VPR",
    "AMOSNet",
    "CALC",
    "CoHOG",
    "HOG",
    "HybridNet",
    "NetVLAD",
    "RegionVLAD"
]

K_VALUES = [1, 5, 10, 20]

# Professional color palette for methods
COLORS = {
    "AlexNet_VPR": "#1E88E5",   # vibrant blue
    "AMOSNet": "#FF6D00",       # vibrant orange
    "CALC": "#43A047",          # vibrant green
    "CoHOG": "#E53935",         # vibrant red
    "HOG": "#8E24AA",           # vibrant purple
    "HybridNet": "#6D4C41",     # warm brown
    "NetVLAD": "#D81B60",       # vibrant pink
    "RegionVLAD": "#546E7A"     # slate gray
}

# Dataset styling
DATASET_COLORS = {
    "corridor": "#1565C0",      # deep blue
    "CLR_dataset": "#C62828"    # deep red
}

LINESTYLES = {
    "corridor": "-",
    "CLR_dataset": "--"
}


# ================= LOAD GT =================
def load_gt(gt_path):
    data = np.load(gt_path, allow_pickle=True)
    gt_dict = {}
    for item in data:
        q_idx = int(item[0])
        refs = [int(r) for r in item[1]]
        gt_dict[q_idx] = refs
    return gt_dict


# ================= LOAD METHOD =================
def load_method(dataset_path, method):
    path = os.path.join(dataset_path, method, "precomputed_data_corrected.npy")
    if not os.path.exists(path):
        return None, None
    data = np.load(path, allow_pickle=True, encoding='latin1')
    return data[0], data[3]  # queries, similarity_matrix


# ================= RANKS =================
def compute_ranks(gt_dict, queries, sim_matrix):
    ranks = []

    for i in range(len(queries)):
        q_idx = int(queries[i])

        if q_idx not in gt_dict:
            continue

        sim_row = sim_matrix[i]
        sorted_indices = np.argsort(sim_row)[::-1]

        gt_refs = gt_dict[q_idx]

        rank = None
        for r, idx in enumerate(sorted_indices):
            if idx in gt_refs:
                rank = r + 1
                break

        if rank is not None:
            ranks.append(rank)

    return np.array(ranks)


# ================= RECALL@K =================
def compute_recall_at_k(gt_dict, queries, sim_matrix, K):
    correct = 0
    total = 0

    for i in range(len(queries)):
        q_idx = int(queries[i])

        if q_idx not in gt_dict:
            continue

        total += 1

        sim_row = sim_matrix[i]
        top_k = np.argsort(sim_row)[::-1][:K]

        gt_refs = gt_dict[q_idx]

        found = False
        for idx in top_k:
            if idx in gt_refs:
                found = True
                break

        if found:
            correct += 1

    return float(correct) / total if total > 0 else 0


# ================= LOAD ALL DATA =================
print("=" * 70)
print("Loading data for all methods...")
print("=" * 70)

# Store results: results[dataset][method] = {'ranks': array, 'recall': list}
results = {dataset: {} for dataset in DATASETS.keys()}

for method in METHODS:
    print("\nProcessing {}...".format(method))
    
    for dataset_name in DATASETS:
        gt_path = DATASETS[dataset_name]["gt"]
        dataset_path = DATASETS[dataset_name]["path"]
        
        if not os.path.exists(gt_path):
            print("  Warning: GT not found for {} at {}".format(dataset_name, gt_path))
            continue
            
        method_path = os.path.join(dataset_path, method)
        if not os.path.exists(method_path):
            print("  Warning: Method {} not found for {}".format(method, dataset_name))
            continue
        
        print("  Loading {}...".format(dataset_name))
        gt_dict = load_gt(gt_path)
        queries, sim_matrix = load_method(dataset_path, method)
        
        if queries is None:
            print("    Failed to load method data")
            continue
        
        ranks = compute_ranks(gt_dict, queries, sim_matrix)
        
        recall_curve = []
        for K in K_VALUES:
            r = compute_recall_at_k(gt_dict, queries, sim_matrix, K)
            recall_curve.append(r)
        
        results[dataset_name][method] = {
            "ranks": ranks,
            "recall": recall_curve
        }
        
        print("    Queries: {}, Valid ranks: {}".format(len(queries), len(ranks)))
        print("    Recall@1: {:.2f}%, Recall@5: {:.2f}%".format(
            recall_curve[0] * 100, recall_curve[1] * 100
        ))

# ================= PLOT 1: RANK CDF (ALL METHODS) =================
print("\n" + "=" * 70)
print("Generating consolidated Rank CDF plot...")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')

# Left subplot: corridor
ax1 = axes[0]
ax1.set_title("Corridor Dataset", fontsize=15, fontweight='bold', pad=12)
ax1.set_xlabel("Rank", fontsize=13)
ax1.set_ylabel("Cumulative Probability", fontsize=13)
ax1.grid(True, alpha=0.25, linestyle='--', linewidth=0.8)
ax1.set_xlim(0, 200)
ax1.set_ylim(0, 1.02)
ax1.set_facecolor('#FAFAFA')

# Right subplot: CLR Dataset
ax2 = axes[1]
ax2.set_title("CLR Dataset", fontsize=15, fontweight='bold', pad=12)
ax2.set_xlabel("Rank", fontsize=13)
ax2.set_ylabel("Cumulative Probability", fontsize=13)
ax2.grid(True, alpha=0.25, linestyle='--', linewidth=0.8)
ax2.set_xlim(0, 200)
ax2.set_ylim(0, 1.02)
ax2.set_facecolor('#FAFAFA')

# Plot each method on both subplots
for method in METHODS:
    # corridor
    if method in results["corridor"]:
        ranks = results["corridor"][method]["ranks"]
        if len(ranks) > 0:
            sorted_ranks = np.sort(ranks)
            cdf = np.arange(1, len(sorted_ranks) + 1) / float(len(sorted_ranks))
            
            # Cap at rank 200 for visualization
            capped_ranks = sorted_ranks[sorted_ranks <= 200]
            capped_cdf = cdf[sorted_ranks <= 200]
            
            ax1.plot(capped_ranks, capped_cdf, 
                     label=method, 
                     color=COLORS.get(method, '#333333'),
                     linewidth=2.2,
                     alpha=0.85)
    
    # CLR Dataset
    if method in results["CLR_dataset"]:
        ranks = results["CLR_dataset"][method]["ranks"]
        if len(ranks) > 0:
            sorted_ranks = np.sort(ranks)
            cdf = np.arange(1, len(sorted_ranks) + 1) / float(len(sorted_ranks))
            
            # Cap at rank 200 for visualization
            capped_ranks = sorted_ranks[sorted_ranks <= 200]
            capped_cdf = cdf[sorted_ranks <= 200]
            
            ax2.plot(capped_ranks, capped_cdf, 
                     label=method, 
                     color=COLORS.get(method, '#333333'),
                     linewidth=2.2,
                     alpha=0.85)

# Add legends
ax1.legend(loc='lower right', fontsize=9, framealpha=0.9, edgecolor='#CCCCCC')
ax2.legend(loc='lower right', fontsize=9, framealpha=0.9, edgecolor='#CCCCCC')

plt.tight_layout()

# Save
cdf_png = os.path.join(OUTPUT_DIR, "rank_cdf_all_methods.png")
cdf_pdf = os.path.join(OUTPUT_DIR, "rank_cdf_all_methods.pdf")
plt.savefig(cdf_png, dpi=200, bbox_inches='tight', facecolor='white')
plt.savefig(cdf_pdf, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: rank_cdf_all_methods.png/pdf")

# ================= PLOT 2: RECALL@K (ALL METHODS) =================
print("\n" + "=" * 70)
print("Generating consolidated Recall@K plot...")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')

# Left subplot: corridor
ax1 = axes[0]
ax1.set_title("Corridor Dataset", fontsize=15, fontweight='bold', pad=12)
ax1.set_xlabel("K (Number of Top Matches)", fontsize=13)
ax1.set_ylabel("Recall@K (%)", fontsize=13)
ax1.grid(True, alpha=0.25, linestyle='--', linewidth=0.8)
ax1.set_xticks(K_VALUES)
ax1.set_ylim(0, 105)
ax1.set_facecolor('#FAFAFA')

# Right subplot: CLR Dataset
ax2 = axes[1]
ax2.set_title("CLR Dataset", fontsize=15, fontweight='bold', pad=12)
ax2.set_xlabel("K (Number of Top Matches)", fontsize=13)
ax2.set_ylabel("Recall@K (%)", fontsize=13)
ax2.grid(True, alpha=0.25, linestyle='--', linewidth=0.8)
ax2.set_xticks(K_VALUES)
ax2.set_ylim(0, 105)
ax2.set_facecolor('#FAFAFA')

# Plot each method on both subplots
for method in METHODS:
    # corridor
    if method in results["corridor"]:
        recall_vals = [r * 100 for r in results["corridor"][method]["recall"]]
        ax1.plot(K_VALUES, recall_vals, 
                 marker='o', 
                 label=method, 
                 color=COLORS.get(method, '#333333'),
                 linewidth=2.2,
                 markersize=8,
                 markerfacecolor='white',
                 markeredgewidth=2,
                 alpha=0.9)
    
    # CLR Dataset
    if method in results["CLR_dataset"]:
        recall_vals = [r * 100 for r in results["CLR_dataset"][method]["recall"]]
        ax2.plot(K_VALUES, recall_vals, 
                 marker='s', 
                 label=method, 
                 color=COLORS.get(method, '#333333'),
                 linewidth=2.2,
                 markersize=7,
                 markerfacecolor='white',
                 markeredgewidth=2,
                 alpha=0.9)

# Add legends
ax1.legend(loc='lower right', fontsize=9, framealpha=0.9, edgecolor='#CCCCCC')
ax2.legend(loc='lower right', fontsize=9, framealpha=0.9, edgecolor='#CCCCCC')

plt.tight_layout()

# Save
recall_png = os.path.join(OUTPUT_DIR, "recall_all_methods.png")
recall_pdf = os.path.join(OUTPUT_DIR, "recall_all_methods.pdf")
plt.savefig(recall_png, dpi=200, bbox_inches='tight', facecolor='white')
plt.savefig(recall_pdf, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: recall_all_methods.png/pdf")

# ================= SUMMARY TABLE =================
print("\n" + "=" * 70)
print("SUMMARY: Recall@1 Comparison")
print("=" * 70)
print("\n{:<15} {:>18} {:>18} {:>18}".format(
    "Method", "corridor R@1", "CLR R@1", "Performance Drop"
))
print("-" * 70)

for method in METHODS:
    corr_r1 = results["corridor"][method]["recall"][0] * 100 if method in results["corridor"] else 0
    clr_r1 = results["CLR_dataset"][method]["recall"][0] * 100 if method in results["CLR_dataset"] else 0
    drop = corr_r1 - clr_r1
    
    # Color formatting for drop
    if drop > 50:
        drop_str = "{:>17.1f}%".format(drop)
    elif drop > 20:
        drop_str = "{:>17.1f}%".format(drop)
    elif drop > 0:
        drop_str = "{:>17.1f}%".format(drop)
    else:
        drop_str = "{:>17.1f}% (Improvement)".format(abs(drop))
    
    print("{:<15} {:>17.2f}% {:>17.2f}% {:>18}".format(
        method, corr_r1, clr_r1, drop_str
    ))

print("\n" + "=" * 70)
print("All plots saved in: {}".format(OUTPUT_DIR))
print("=" * 70)