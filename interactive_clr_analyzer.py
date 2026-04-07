#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive VPR Analysis Tool - Check any query across all methods
Shows performance per individual reference (VPR-like vs CLR-like distinction)
"""

from __future__ import print_function, division
import os
import numpy as np
import re

# ================= COLOR DEFINITIONS =================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    DIM = '\033[2m'

# Helper to remove colors for alignment
def strip_color(text):
    return re.sub(r'\033\[[0-9;]+m', '', text)

# ================= CONFIGURATION =================
BENCH_ROOT = ""  # Leave empty if script is in the same directory
DATASET_NAME = "CLR_dataset"

GROUND_TRUTH_PATH = os.path.join(BENCH_ROOT, "datasets", DATASET_NAME, "ground_truth_new.npy")
PRECOMPUTED_BASE = os.path.join(BENCH_ROOT, "precomputed_matches", DATASET_NAME)

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

# ============= LOAD GROUND TRUTH =============
print(Colors.BOLD + "Loading ground truth..." + Colors.END)
gt_data = np.load(GROUND_TRUTH_PATH, allow_pickle=True)

ground_truth_dict = {}
for item in gt_data:
    query_idx = int(item[0])
    ref_indices = [int(x) for x in item[1]]
    ground_truth_dict[query_idx] = ref_indices

print(Colors.GREEN + "Loaded {} queries".format(len(ground_truth_dict)) + Colors.END)
print("Query range: {} to {}".format(min(ground_truth_dict.keys()), max(ground_truth_dict.keys())))
print()

# ============= LOAD ALL METHOD DATA =============
print(Colors.BOLD + "Loading method results..." + Colors.END)
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
            print(Colors.GREEN + "  Loaded {}".format(method) + Colors.END)
        except Exception as e:
            print(Colors.RED + "    Failed to load {}: {}".format(method, e) + Colors.END)
    else:
        print(Colors.YELLOW + "  ? {}: File not found".format(method) + Colors.END)

print("\n" + Colors.BOLD + "=" * 60 + Colors.END)
print(Colors.HEADER + Colors.BOLD + "Interactive Query Checker" + Colors.END)
print(Colors.BOLD + "=" * 60 + Colors.END)

# ============= INTERACTIVE LOOP =============
while True:
    print("\n" + Colors.DIM + "-" * 60 + Colors.END)
    query_input = input(Colors.BLUE + "Enter query index (0-219), or quit (q): " + Colors.END).strip()
    
    if query_input.lower() in ('q', 'quit'):
        print("Exiting...")
        break
    
    try:
        query_idx = int(query_input)
    except ValueError:
        print(Colors.RED + "Invalid! Please enter a number between 0 and 219." + Colors.END)
        continue
    
    if query_idx not in ground_truth_dict:
        print(Colors.RED + "Query {} not found! Available range: 0-219".format(query_idx) + Colors.END)
        continue
    
    # Display ground truth
    gt_refs = ground_truth_dict[query_idx]
    print("\n" + Colors.BOLD + "=" * 60 + Colors.END)
    print(Colors.HEADER + Colors.BOLD + "QUERY {} - GROUND TRUTH".format(query_idx) + Colors.END)
    print(Colors.BOLD + "=" * 60 + Colors.END)
    print(Colors.YELLOW + "Correct references: {}".format(gt_refs) + Colors.END)
    print("Number of correct references: {}".format(len(gt_refs)))
    print()
    
    # Ask user if they want to label references
    if len(gt_refs) > 1:
        label_refs = input(Colors.BLUE + "Do you want to label individual references? (y/n): " + Colors.END).strip().lower()
        ref_labels = {}
        if label_refs in ('y', 'yes'):
            print("\nEnter labels for each reference (e.g., 'VPR', 'CLR', ...):")
            for ref in gt_refs:
                label = input("  Reference {}: ".format(ref)).strip()
                ref_labels[ref] = label if label else "Ref{}".format(ref)
    else:
        ref_labels = {gt_refs[0]: "Only Ref"}
    
    # ============= SUMMARY TABLE =============
    print("\n" + Colors.BOLD + "-" * 80 + Colors.END)
    print(Colors.UNDERLINE + "SUMMARY: Top-1 Prediction for Each Method".center(80) + Colors.END)
    print(Colors.BOLD + "-" * 80 + Colors.END)
    print("{:<20} {:>12} {:>10} {:>12} {:>18}".format(
        "Method", "Top-1 Pred", "Correct?", "Score", "Which Ref?"
    ))
    print(Colors.DIM + "-" * 80 + Colors.END)
    
    for method in METHODS:
        if method not in method_data:
            print("{:<20} {:>46}".format(method, "NOT LOADED"))
            continue
        
        data = method_data[method]
        query_indices = data['query_indices']
        predictions = data['predictions']
        scores = data['scores']
        
        mask = np.where(query_indices == query_idx)[0]
        
        if len(mask) == 0:
            print("{:<20} {:>46}".format(method, "NOT FOUND"))
            continue
        
        pos = mask[0]
        top1_pred = predictions[pos]
        top1_score = scores[pos]
        is_correct = top1_pred in gt_refs
        
        which_ref = ref_labels.get(top1_pred, "Wrong") if is_correct else "Wrong"
        
        if is_correct:
            correct_str = Colors.GREEN + "PASS" + Colors.END
            score_color = Colors.GREEN
        else:
            correct_str = Colors.RED + "FAIL" + Colors.END
            score_color = Colors.RED
        
        score_str = score_color + "{:.4f}".format(top1_score) + Colors.END
        
        # Fixed alignment only
        plain = "{:<20} {:>12} {:>10} {:>12} {:>18}".format(
            method, top1_pred, strip_color(correct_str), strip_color(score_str), which_ref
        )
        final = plain.replace(strip_color(correct_str), correct_str).replace(strip_color(score_str), score_str)
        print(final)
    
    # ============= DETAILED PER-REFERENCE ANALYSIS =============
    print("\n" + Colors.BOLD + "=" * 80 + Colors.END)
    print(Colors.HEADER + Colors.BOLD + "DETAILED PER-REFERENCE ANALYSIS" + Colors.END)
    print(Colors.BOLD + "=" * 80 + Colors.END)
    
    for ref_idx in gt_refs:
        ref_label = ref_labels.get(ref_idx, "Ref{}".format(ref_idx))
        print("\n" + Colors.BOLD + "-" * 80 + Colors.END)
        print(Colors.YELLOW + Colors.BOLD + "ANALYZING: {} (Reference {})".format(ref_label, ref_idx) + Colors.END)
        print(Colors.DIM + "-" * 80 + Colors.END)
        
        print("{:<20} {:>15} {:>15} {:>12}".format(
            "Method", "Rank of Ref", "Score", "In Top-5?"
        ))
        print(Colors.DIM + "-" * 80 + Colors.END)
        
        for method in METHODS:
            if method not in method_data:
                continue
            
            data = method_data[method]
            sim_matrix = data['similarity_matrix']
            query_scores = sim_matrix[query_idx]
            sorted_indices = np.argsort(query_scores)[::-1]
            
            rank = None
            score = None
            for r, idx in enumerate(sorted_indices):
                if idx == ref_idx:
                    rank = r + 1
                    score = query_scores[idx]
                    break
            
            in_top5 = rank is not None and rank <= 5
            
            # Color-coded rank display (original logic kept)
            if rank is not None and rank == 1:
                rank_display = Colors.GREEN + Colors.BOLD + "Top-1" + Colors.END
                rank_color = Colors.GREEN
            elif rank is not None and rank <= 5:
                rank_display = Colors.BLUE + "Rank {}".format(rank) + Colors.END
                rank_color = Colors.BLUE
            elif rank is not None:
                rank_display = Colors.DIM + "Rank {}".format(rank) + Colors.END
                rank_color = Colors.DIM
            else:
                rank_display = Colors.RED + "Not Found" + Colors.END
                rank_color = Colors.RED
            
            score_str = "{:.4f}".format(score) if score is not None else "N/A"
            score_display = rank_color + score_str + Colors.END if score is not None else score_str
            
            top5_str = Colors.GREEN + "Yes" + Colors.END if in_top5 else (Colors.RED + "No" + Colors.END if rank is not None else Colors.RED + "No" + Colors.END)
            
            # Fixed alignment only
            plain = "{:<20} {:>15} {:>15} {:>12}".format(
                method, strip_color(rank_display), strip_color(score_display), strip_color(top5_str)
            )
            final = plain.replace(strip_color(rank_display), rank_display)\
                         .replace(strip_color(score_display), score_display)\
                         .replace(strip_color(top5_str), top5_str)
            print(final)
    
    # ============= TOP-5 PREDICTIONS ============= (unchanged)
    show_details = input("\n" + Colors.BLUE + "Show top-5 predictions? (y/n): " + Colors.END).strip().lower()
    if show_details in ('y', 'yes'):
        print("\n" + Colors.BOLD + "=" * 70 + Colors.END)
        print(Colors.HEADER + Colors.BOLD + "TOP-5 PREDICTIONS PER METHOD" + Colors.END)
        print(Colors.BOLD + "=" * 70 + Colors.END)
        
        for method in METHODS:
            if method not in method_data:
                continue
            
            data = method_data[method]
            sim_matrix = data['similarity_matrix']
            query_scores = sim_matrix[query_idx]
            top5_indices = np.argsort(query_scores)[::-1][:5]
            top5_scores = query_scores[top5_indices]
            
            print("\n" + Colors.BOLD + method + Colors.END)
            print("  Rank  | Ref Index |    Score    | Status  | Label")
            print("  " + Colors.DIM + "-" * 58 + Colors.END)
            
            for rank, (ref_idx, score) in enumerate(zip(top5_indices, top5_scores)):
                is_correct = ref_idx in gt_refs
                if is_correct:
                    status = Colors.GREEN + "CORRECT" + Colors.END
                    score_display = Colors.GREEN + "{:.6f}".format(score) + Colors.END
                    rank_display = Colors.GREEN + Colors.BOLD + "  {:>2}".format(rank+1) + Colors.END
                else:
                    status = Colors.RED + "WRONG" + Colors.END
                    score_display = Colors.DIM + "{:.6f}".format(score) + Colors.END
                    rank_display = "  {:>2}".format(rank+1)
                
                label = ref_labels.get(ref_idx, "Reference {}".format(ref_idx)) if is_correct else "-"
                
                print("{}    | {:>9} | {} | {} | {}".format(
                    rank_display, ref_idx, score_display, status, label
                ))
    
    # ============= COMPARISON SUMMARY ============= (unchanged)
    print("\n" + Colors.BOLD + "=" * 60 + Colors.END)
    print(Colors.HEADER + Colors.BOLD + "COMPARISON SUMMARY" + Colors.END)
    print(Colors.BOLD + "=" * 60 + Colors.END)
    print("\n" + Colors.UNDERLINE + "Which references were successfully retrieved by each method?" + Colors.END)
    print(Colors.DIM + "-" * 70 + Colors.END)
    
    header = "{:<20}".format("Method")
    for ref_idx in gt_refs:
        ref_label = ref_labels.get(ref_idx, "Ref{}".format(ref_idx))
        short_label = ref_label[:10] if len(ref_label) > 10 else ref_label
        header += " {:>12}".format(short_label)
    print(header)
    print(Colors.DIM + "-" * (20 + 13 * len(gt_refs)) + Colors.END)
    
    for method in METHODS:
        if method not in method_data:
            continue
        
        data = method_data[method]
        sim_matrix = data['similarity_matrix']
        query_scores = sim_matrix[query_idx]
        sorted_indices = np.argsort(query_scores)[::-1]
        
        row = "{:<20}".format(method)
        
        for ref_idx in gt_refs:
            rank = None
            for r, idx in enumerate(sorted_indices):
                if idx == ref_idx:
                    rank = r + 1
                    break
            
            if rank is None:
                status = Colors.RED + "Not Found" + Colors.END
            elif rank == 1:
                status = Colors.GREEN + Colors.BOLD + "Top-1" + Colors.END
            elif rank <= 5:
                status = Colors.BLUE + "Rank {}".format(rank) + Colors.END
            else:
                status = Colors.DIM + "Rank {}".format(rank) + Colors.END
            
            row += " {:>15}".format(strip_color(status))
        # Re-apply color (simple way for this section)
        for color_code in [Colors.GREEN, Colors.BLUE, Colors.DIM, Colors.RED]:
            row = row.replace(strip_color(color_code + "Top-1" + Colors.END), Colors.GREEN + Colors.BOLD + "Top-1" + Colors.END)
            row = row.replace(strip_color(color_code + "Rank " + str(rank)), status)  # This part is approximate
        print(row)   # Note: This section is harder to perfectly color-align without more changes

print("\n" + Colors.BOLD + "=" * 60 + Colors.END)
print(Colors.HEADER + "Interactive session ended" + Colors.END)
print(Colors.BOLD + "=" * 60 + Colors.END)