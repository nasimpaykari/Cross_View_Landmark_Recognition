<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cross-View Landmark Recognition (CLR) Dataset</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            max-width: 900px;
        }
        h1, h2, h3 {
            color: #1e3a8a;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f1f5f9;
        }
        ul {
            line-height: 1.8;
        }
        pre {
            background-color: #f8fafc;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
        }
    </style>
</head>
<body>

    <h1>Cross-View Landmark Recognition (CLR) Foundation Dataset</h1>

    <p><strong>The Cross-View Landmark Recognition (CLR) Foundation Dataset</strong> is a curated collection of landmark images designed for evaluating cross-view recognition under wide-baseline conditions. Derived from Google Landmarks v2, this dataset prioritizes landmarks that remain identifiable across extreme viewpoint changes.</p>

    <h2>Dataset Statistics</h2>
    <table>
        <tr>
            <th>Metric</th>
            <th>Value</th>
        </tr>
        <tr><td>Total images</td><td>557</td></tr>
        <tr><td>Unique landmarks</td><td>229</td></tr>
        <tr><td>Avg images/landmark</td><td>2.43</td></tr>
        <tr><td>Min images/landmark</td><td>1</td></tr>
        <tr><td>Max images/landmark</td><td>10</td></tr>
        <tr><td>Countries</td><td>9</td></tr>
        <tr><td>Continents</td><td>North America, Oceania, Asia, Other</td></tr>
    </table>

    <h3>Image Format Distribution</h3>
    <ul>
        <li><code>.jpg</code>: 556 images</li>
        <li><code>.jpeg</code>: 1 image</li>
    </ul>

    <h3>Image Size Statistics</h3>
    <table>
        <tr>
            <th>Dimension</th>
            <th>Min</th>
            <th>Max</th>
            <th>Average</th>
        </tr>
        <tr><td>Width (pixels)</td><td>639</td><td>640</td><td>639.99</td></tr>
        <tr><td>Height (pixels)</td><td>172</td><td>1205</td><td>572.79</td></tr>
        <tr><td>File size (MB)</td><td>0.03</td><td>0.27</td><td>0.10</td></tr>
    </table>

    <h3>Geographic Coverage</h3>
    <ul>
        <li><strong>Asia</strong>: Azerbaijan, Iran, Israel, Oman, Thailand, Turkey, UAE</li>
        <li><strong>North America</strong>: United States</li>
        <li><strong>Oceania</strong>: Australia</li>
        <li><strong>Other</strong>: (additional regions as applicable)</li>
    </ul>

    <h2>Copyright &amp; Attribution</h2>
    <p>This dataset is derived from the <strong>Google Landmarks v2 dataset</strong>. All images are subject to their original copyrights and licenses as provided by Google. This repository provides only curated subsets and metadata; the original images remain the property of their respective copyright holders.</p>

    <h3>Terms of Use</h3>
    <ul>
        <li>This dataset is intended for <strong>research purposes only</strong></li>
        <li>Images may not be used for commercial applications without permission from the original copyright holders</li>
        <li>Users must comply with Google's Terms of Service for the original dataset</li>
        <li>When publishing results using this dataset, you must cite both the original Google Landmarks v2 paper and this work</li>
    </ul>

    <h3>Required Citations</h3>
    <pre><code>@article{weyand2020google,
  title={Google Landmarks Dataset v2},
  author={Weyand, Tobias and others},
  journal={arXiv preprint arXiv:2004.01804},
  year={2020}
}

@inproceedings{clr2025,
  title={Cross-View Landmark Recognition for Cooperative Visual Navigation},
  author={Paykari, Nasim and Vural, Ilayda and Desta, Natnael and Zain, Ademi and Clark, Taylor and Rahouti, Mohamed and Lyons, Damian},
}
</code></pre>

</body>
</html>
