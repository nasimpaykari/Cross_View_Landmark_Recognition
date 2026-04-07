Cross View Landmark Recognition 

The Cross-View Landmark Recognition (CLR) Foundation Dataset is a curated collection of landmark images designed for evaluating cross-view recognition under wide-baseline conditions. Derived from Google Landmarks v2, this dataset prioritizes landmarks that remain identifiable across extreme viewpoint changes.

Dataset Statistics
- Total images: 557
- Unique landmarks: 229
- Average images per landmark: 2.43
- Min images per landmark: 1
- Max images per landmark: 10
- Geographic coverage: 9 countries across Asia, North America, Oceania

Image Format Distribution
- `.jpg`: 556 images
- `.jpeg`: 1 image

#Image Size Statistics
| Dimension       | Min  | Max  | Average |
|-----------------|------|------|---------|
| Width (pixels)  | 639  | 640  | 639.99  |
| Height (pixels) | 172  | 1205 | 572.79  |
| File size (MB)  | 0.03 | 0.27 | 0.10    |

Geographic Coverage
- Asia: Azerbaijan, Iran, Israel, Oman, Thailand, Turkey, UAE
- North America: United States
- Oceania: Australia

Copyright & Attribution

This dataset is derived from the Google Landmarks v2 dataset~\cite{weyand2020google}. All images are subject to their original copyrights and licenses as provided by Google. This repository provides only curated subsets and metadata; the original images remain the property of their respective copyright holders.

Terms of Use:
- This dataset is intended for research purposes only
- Images may not be used for commercial applications without permission from the original copyright holders
- Users must comply with Google's Terms of Service for the original dataset
- When publishing results using this dataset, you must cite both the original Google Landmarks v2 paper and this work

Required Citations:
```bibtex
@article{weyand2020google,
  title={Google Landmarks Dataset v2},
  author={Weyand, Tobias and others},
  journal={arXiv preprint arXiv:2004.01804},
  year={2020}
}

@inproceedings{...,
  title={Cross-View Landmark Recognition for Cooperative Visual Navigation},
  author={Paykari, Nasim and Vural, Ilayda and Desta, Natnael and Zain, Ademi and Clark, Taylor and Rahouti, Mohamed and Lyons, Damian},
}
