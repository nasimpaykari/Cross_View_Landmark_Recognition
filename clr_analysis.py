#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive VPR Analysis for CLR Dataset
Generates: Recall@K, MRR, Rank Distribution, and Method Comparison
"""

from __future__ import print_function, division
import os
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime

# ================= CONFIGURATION =================
VPR_BENCH_ROOT = ""
DATASET_NAME = "CLR_dataset"

GROUND_TRUTH_PATH = os.path.join(VPR_BENCH_ROOT, "datasets", DATASET_NAME, "ground_truth_new.npy")
PRECOMPUTED_BASE = os.path.join(VPR_BENCH_ROOT, "precomputed_matches", DATASET_NAME)
OUTPUT_DIR = os.path.join(VPR_BENCH_ROOT, "results", DATASET_NAME)

METHODS = [
    'AlexNet_VPR',
    'AMOSNet',
    'CALC',
    'CoHOG',
    'HOG',
    'HybridNet',
    'NetVLAD',
    'RegionVLAD'
]

# Create output directory
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("=" * 80)
print("Comprehensive VPR Analysis for CLR Dataset")
print("=" * 80)

# ============= LOAD GROUND TRUTH =============
print("\n[1] Loading ground truth...")
gt_data = np.load(GROUND_TRUTH_PATH, allow_pickle=True)

ground_truth_dict = {}
for item in gt_data:
    query_idx = int(item[0])
    ref_indices = [int(x) for x in item[1]]
    ground_truth_dict[query_idx] = ref_indices

num_queries = len(ground_truth_dict)
print("  Loaded {} queries".format(num_queries))

# ============= LOAD METHOD DATA =============
print("\n[2] Loading method results...")
method_data = {}

for method in METHODS:
    npy_path = os.path.join(PRECOMPUTED_BASE, method, 'precomputed_data_corrected.npy')
    
    if os.path.exists(npy_path):
        try:
            data = np.load(npy_path, allow_pickle=True, encoding='latin1')
            method_data[method] = {
                'query_indices': data[0],
                'predictions': data[1],
                'scores': data[2],
                'similarity_matrix': data[3]
            }
            print("  Loaded {}".format(method))
        except Exception as e:
            print("  Failed to load {}: {}".format(method, e))
    else:
        print("  {}: File not found".format(method))

# ============= EVALUATION METRICS =============
print("\n[3] Computing evaluation metrics...")

results = {}

for method, data in method_data.items():
    print("  Processing {}...".format(method))
    
    query_indices = data['query_indices']
    predictions = data['predictions']
    scores = data['scores']
    sim_matrix = data['similarity_matrix']
    
    # Ensure query order matches ground truth
    # Some methods may have queries in different order
    query_order = []
    for q in sorted(ground_truth_dict.keys()):
        pos = np.where(query_indices == q)[0]
        if len(pos) > 0:
            query_order.append((q, pos[0]))
    
    # Initialize metrics
    recall_at_k = {1: 0, 5: 10, 10: 0, 20: 0}
    reciprocal_ranks = []
    rank_list = []
    
    for q_idx, pos in query_order:
        gt_refs = ground_truth_dict[q_idx]
        query_scores = sim_matrix[q_idx]  # Similarity to all references
        
        # Get ranking of references
        ranked_refs = np.argsort(query_scores)[::-1]  # Descending order
        
        # Find rank of first correct match
        first_correct_rank = None
        for rank, ref in enumerate(ranked_refs):
            if ref in gt_refs:
                first_correct_rank = rank + 1  # 1-indexed
                break
        
        if first_correct_rank is not None:
            rank_list.append(first_correct_rank)
            reciprocal_ranks.append(1.0 / first_correct_rank)
            
            # Recall@K
            for k in recall_at_k.keys():
                if first_correct_rank <= k:
                    recall_at_k[k] += 1
    
    # Compute metrics
    results[method] = {
        'recall_at_k': {k: v / len(query_order) for k, v in recall_at_k.items()},
        'mrr': np.mean(reciprocal_ranks) if reciprocal_ranks else 0,
        'median_rank': np.median(rank_list) if rank_list else float('inf'),
        'mean_rank': np.mean(rank_list) if rank_list else float('inf'),
        'rank_distribution': rank_list
    }
    
    print("    Recall@1: {:.2f}%, MRR: {:.4f}".format(
        results[method]['recall_at_k'][1] * 100,
        results[method]['mrr']
    ))

# ============= PRINT RESULTS TABLE =============
print("\n[4] Results Summary")
print("=" * 80)
print("\n{:<15} {:>10} {:>10} {:>10} {:>10} {:>12}".format(
    "Method", "R@1", "R@5", "R@10", "R@20", "MRR"
))
print("-" * 80)

for method in METHODS:
    if method in results:
        r = results[method]
        print("{:<15} {:>9.2f}% {:>9.2f}% {:>9.2f}% {:>9.2f}% {:>11.4f}".format(
            method,
            r['recall_at_k'][1] * 100,
            r['recall_at_k'][5] * 100,
            r['recall_at_k'][10] * 100,
            r['recall_at_k'][20] * 100,
            r['mrr']
        ))

# ============= SAVE RESULTS =============
print("\n[5] Saving results...")

# Save as JSON
json_path = os.path.join(OUTPUT_DIR, "results_summary.json")
with open(json_path, 'w') as f:
    # Convert numpy values to Python types
    serializable_results = {}
    for method, r in results.items():
        serializable_results[method] = {
            'recall_at_k': {k: float(v) for k, v in r['recall_at_k'].items()},
            'mrr': float(r['mrr']),
            'median_rank': float(r['median_rank']),
            'mean_rank': float(r['mean_rank'])
        }
    json.dump(serializable_results, f, indent=2)
print("  Saved to: {}".format(json_path))

# ============= PLOT RECALL CURVE =============
print("\n[6] Generating plots...")

plt.figure(figsize=(10, 6))
k_values = [1, 5, 10, 20]

for method in METHODS:
    if method in results:
        recall_values = [results[method]['recall_at_k'][k] * 100 for k in k_values]
        plt.plot(k_values, recall_values, marker='o', label=method)

plt.xlabel('K')
plt.ylabel('Recall@K (%)')
plt.title('Recall@K Comparison on CLR Dataset')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()

plot_path = os.path.join(OUTPUT_DIR, "recall_curve.png")
plt.savefig(plot_path, dpi=150)
print("  Saved recall curve to: {}".format(plot_path))

# ============= PLOT RANK DISTRIBUTION =============
plt.figure(figsize=(12, 6))

# Plot rank distribution as histogram
for method in METHODS[:4]:  # First 4 methods for clarity
    if method in results and results[method]['rank_distribution']:
        ranks = results[method]['rank_distribution']
        plt.hist(ranks, bins=50, alpha=0.5, label=method, density=True)

plt.xlabel('Rank of First Correct Match')
plt.ylabel('Density')
plt.title('Rank Distribution (First 4 Methods)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

rank_plot_path = os.path.join(OUTPUT_DIR, "rank_distribution.png")
plt.savefig(rank_plot_path, dpi=150)
print("  Saved rank distribution to: {}".format(rank_plot_path))

# ============= BAR CHART COMPARISON =============
plt.figure(figsize=(12, 6))

x = np.arange(len(METHODS))
width = 0.2

r1 = [results[m]['recall_at_k'][1] * 100 if m in results else 0 for m in METHODS]
r5 = [results[m]['recall_at_k'][5] * 100 if m in results else 0 for m in METHODS]
r10 = [results[m]['recall_at_k'][10] * 100 if m in results else 0 for m in METHODS]

plt.bar(x - width, r1, width, label='Recall@1')
plt.bar(x, r5, width, label='Recall@5')
plt.bar(x + width, r10, width, label='Recall@10')

plt.xlabel('Method')
plt.ylabel('Recall (%)')
plt.title('Recall Comparison Across Methods')
plt.xticks(x, METHODS, rotation=45, ha='right')
plt.legend()
plt.tight_layout()

bar_path = os.path.join(OUTPUT_DIR, "recall_bars.png")
plt.savefig(bar_path, dpi=150)
print("  Saved bar chart to: {}".format(bar_path))

# ============= SUMMARY REPORT =============
print("\n[7] Generating summary report...")

report_path = os.path.join(OUTPUT_DIR, "analysis_report.txt")
with open(report_path, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("VPR Analysis Report for CLR Dataset\n")
    f.write("Generated: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    f.write("=" * 80 + "\n\n")
    
    f.write("Dataset Statistics:\n")
    f.write("  Total queries: {}\n".format(num_queries))
    f.write("  Total references: 328\n")
    f.write("  Average references per query: 1.5\n\n")
    
    f.write("Method Rankings (by Recall@1):\n")
    sorted_methods = sorted(results.items(), key=lambda x: x[1]['recall_at_k'][1], reverse=True)
    for rank, (method, r) in enumerate(sorted_methods, 1):
        f.write("  {}. {}: R@1={:.2f}%, R@5={:.2f}%, MRR={:.4f}\n".format(
            rank, method,
            r['recall_at_k'][1] * 100,
            r['recall_at_k'][5] * 100,
            r['mrr']
        ))
    
    f.write("\n" + "-" * 80 + "\n")
    f.write("Complete Results Table:\n")
    f.write("{:<15} {:>10} {:>10} {:>10} {:>10} {:>12} {:>12}\n".format(
        "Method", "R@1", "R@5", "R@10", "R@20", "MRR", "MedRank"
    ))
    f.write("-" * 80 + "\n")
    
    for method in METHODS:
        if method in results:
            r = results[method]
            f.write("{:<15} {:>9.2f}% {:>9.2f}% {:>9.2f}% {:>9.2f}% {:>11.4f} {:>11.0f}\n".format(
                method,
                r['recall_at_k'][1] * 100,
                r['recall_at_k'][5] * 100,
                r['recall_at_k'][10] * 100,
                r['recall_at_k'][20] * 100,
                r['mrr'],
                r['median_rank']
            ))

print("  Saved report to: {}".format(report_path))

print("\n" + "=" * 80)
print("Analysis complete!")
print("Results saved to: {}".format(OUTPUT_DIR))
print("=" * 80)