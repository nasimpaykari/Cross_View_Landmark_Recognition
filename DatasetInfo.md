# CLR Dataset - Complete Ground Truth

This document contains the complete query-reference mappings for the CLR Dataset used in our paper.

## Ground Truth Format

The ground truth is stored in `data/CLR_dataset/ground_truth_new.npy` as a numpy array where each entry is:
```
[query_index, [reference_indices]]
```

## Query-Reference Assignment Method

For each location, we **randomly selected one image as the query** and designated **all remaining images as references**. This split is reproducible and recorded in the ground truth file.

**Note:** A self-match (image serving as both query and reference) is intentionally included to validate the experimental pipeline, inflating precision by approximately 0.45%; a negligible effect.

---

## Complete Query-Reference Mappings

Each query (0-219) maps to one or more reference images:

### Single Reference Queries (143 queries, 65%)

| Query Range | Reference(s) | Count |
|-------------|--------------|-------|
| 0-3 | [0], [1], [2], [3] | 4 |
| 6-15 | [8], [9], [10], [11], [12], [13], [14], [15], [16], [17] | 10 |
| 17 | [20] | 1 |
| 19-23 | [23], [24], [25], [26], [27] | 5 |
| 26 | [33] | 1 |
| 28-33 | [37], [38], [39], [40], [41], [42] | 6 |
| 36-44 | [53], [54], [55], [56], [57], [58], [59], [60], [61] | 9 |
| 48-49 | [70], [71] | 2 |
| 52-53 | [78], [79] | 2 |
| 55-56 | [82], [83] | 2 |
| 58-59 | [87], [88] | 2 |
| 61-63 | [91], [92], [93] | 3 |
| 65-69 | [96], [97], [98], [99], [100] | 5 |
| 71 | [103] | 1 |
| 73 | [105] | 1 |
| 75-76 | [111], [112] | 2 |
| 78-79 | [122], [123] | 2 |
| 81 | [133] | 1 |
| 85-86 | [141], [142] | 2 |
| 88-89 | [145], [146] | 2 |
| 91 | [150] | 1 |
| 94 | [155] | 1 |
| 98-100 | [162], [163], [164] | 3 |
| 102-103 | [169], [170] | 2 |
| 105 | [172] | 1 |
| 108-110 | [176], [177], [178] | 3 |
| 112 | [181] | 1 |
| 114-116 | [185], [186], [187] | 3 |
| 118-119 | [194], [195] | 2 |
| 121-123 | [199], [200], [201] | 3 |
| 125-126 | [208], [209] | 2 |
| 129 | [215] | 1 |
| 131-134 | [219], [220], [221], [222] | 4 |
| 136 | [225] | 1 |
| 138-141 | [227], [228], [229], [230] | 4 |
| 143-149 | [232], [233], [234], [235], [236], [237], [238] | 7 |
| 151-156 | [241], [242], [243], [244], [245], [246] | 6 |
| 158-162 | [249], [250], [251], [252], [253] | 5 |
| 164-165 | [256], [257] | 2 |
| 167-168 | [260], [261] | 2 |
| 170-172 | [265], [266], [267] | 3 |
| 174-178 | [270], [271], [272], [273], [274] | 5 |
| 180-181 | [277], [278] | 2 |
| 184-190 | [285], [286], [287], [288], [289], [290], [291] | 7 |
| 193-199 | [296], [297], [298], [299], [300], [301], [302] | 7 |
| 202-204 | [308], [309], [310] | 3 |
| 206-219 | [314], [315], [316], [317], [318], [319], [320], [321], [322], [323], [324], [325], [326], [327] | 14 |

### Multi-Reference Queries (77 queries, 35%)

| Query | References | Count | Paper Reference |
|-------|------------|-------|-----------------|
| 4 | [4, 5] | 2 | |
| 5 | [6, 7] | 2 | |
| 16 | [18, 19] | 2 | |
| 18 | [21, 22] | 2 | |
| 24 | [28, 29] | 2 | |
| 25 | [30, 31, 32] | 3 | |
| 27 | [34, 35] | 2 | |
| 34 | [42, 43] | 2 | |
| **35** | [44, 45, 46, 47, 48, 49, 50, 51, 52] | 9 | Query 80 in paper |
| 45 | [62, 63] | 2 | |
| 46 | [64, 65] | 2 | |
| 47 | [66, 67, 68, 69] | 4 | |
| 50 | [72, 73, 74] | 3 | |
| **51** | [75, 76, 77] | 3 | Query 35 in paper |
| 54 | [80, 81] | 2 | |
| **57** | [84, 85, 86] | 3 | **Analyzed in paper** |
| 60 | [89, 90] | 2 | |
| 64 | [94, 95] | 2 | |
| 70 | [101, 102] | 2 | |
| **74** | [106, 107, 108, 109, 110] | 5 | **Analyzed in paper** |
| **77** | [113, 114, 115, 116, 117, 118, 119, 120, 121] | 9 | |
| **80** | [124, 125, 126, 127, 128, 129, 130, 131, 132] | 9 | **Failure case in paper** |
| 82 | [134, 135] | 2 | |
| 83 | [136, 137, 138] | 3 | |
| 84 | [139, 140] | 2 | |
| 87 | [143, 144] | 2 | |
| 90 | [147, 148, 149] | 3 | |
| 92 | [151, 152] | 2 | |
| 93 | [153, 154] | 2 | |
| 95 | [156, 157] | 2 | |
| 96 | [158, 159] | 2 | |
| 97 | [160, 161] | 2 | |
| 101 | [165, 166, 167, 168] | 4 | |
| 106 | [173, 174] | 2 | |
| 111 | [179, 180] | 2 | |
| 113 | [182, 183, 184] | 3 | |
| **117** | [188, 189, 190, 191, 192, 193] | 6 | **Analyzed in paper** |
| 120 | [196, 197, 198] | 3 | |
| 124 | [202, 203, 204, 205, 206, 207] | 6 | |
| 127 | [210, 211] | 2 | |
| 128 | [212, 213, 214] | 3 | |
| 130 | [216, 217, 218] | 3 | |
| 135 | [223, 224] | 2 | |
| **137** | [226] | 1 | **Sanity check (identical view)** |
| 150 | [239, 240] | 2 | |
| 157 | [247, 248] | 2 | |
| 163 | [254, 255] | 2 | |
| 166 | [258, 259] | 2 | |
| 169 | [262, 263, 264] | 3 | |
| 173 | [268, 269] | 2 | |
| 179 | [275, 276] | 2 | |
| 182 | [279, 280, 281, 282] | 4 | |
| 183 | [283, 284] | 2 | |
| **191** | [292, 293] | 2 | **Analyzed in paper** |
| 192 | [294, 295] | 2 | |
| **201** | [304, 305, 306, 307] | 4 | |
| 205 | [311, 312, 313] | 3 | |

---

## Reference Type Labels (as used in paper)

For the queries analyzed in detail in the paper:

| Query | Reference | Type | Notes |
|-------|-----------|------|-------|
| **57** | 84 | VPR-like | Front-facing, easy |
| | 85 | CLR-like | Highly oblique, challenging |
| | 86 | CLR-like | Moderate difficulty |
| **74** | 109, 110 | VPR-like | Similar viewpoint |
| | 106, 107, 108 | CLR-like | Oblique/CLR viewpoints |
| **117** | 188 | VPR-like | Distance view |
| | 192 | CLR-like | Distinctive, easy |
| | 189, 190, 191, 193 | CLR-like | Various angles, challenging |
| **137** | 226 | Identical | Sanity check (all methods pass) |
| **191** | 292 | VPR-like | Similar viewpoint |
| | 293 | CLR-like | Different perspective |
| **201** | 304 | Similar | Similar viewpoint |
| | 305, 306, 307 | Separate | Different views |
| **142** | 231 | Separate | Separate items together |

---

## Dataset Statistics Summary

```
┌─────────────────────────────────────┬──────────┐
│ Metric                              │ Value    │
├─────────────────────────────────────┼──────────┤
│ Total queries                       │ 220      │
│ Total references                    │ 328      │
│ Total images                        │ 548      │
│ Single-ref queries                  │ 143 (65%)│
│ Multi-ref queries                   │ 77 (35%) │
│ Max references per query            │ 9        │
│ Min references per query            │ 1        │
│ Average references per query        │ 1.49     │
│ Locations with VPR+CLR pairs        │ 17       │
└─────────────────────────────────────┴──────────┘
```
