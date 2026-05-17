# DustTrak Data Cleaner

A Windows desktop tool that converts raw **TSI DustTrak DRX** log files (models 8533 and 8534) into clean, analysis-ready CSVs and PM concentration figures.

TSI DustTrak instruments export CSV files with a proprietary metadata header and concentrations in mg/m³. This tool strips the metadata, converts units to µg/m³, reconstructs absolute datetimes from elapsed time, and generates a time-series plot — all in one step.

For each input file the tool produces:
- **`<name>_processed.csv`** — columns: `Datetime, pm1, pm2.5, pm4, pm10, pmt` (µg/m³)
- **`<name>_processed_plot.png`** — PM₁, PM₂.₅, and PM₁₀ concentration time-series chart

Python script was used to make the algorithm while the github repo and production was done in conjunction with Claude.
---

## Download (Windows)

Pre-built executables are available on the [Releases](../../releases) page — no Python required.

---

## Running from source

**Requirements:** Python 3.9+

```bash
pip install -r requirements.txt
python dusttrak_data_cleaner.py
```

---

## Usage

1. Launch the application (double-click the `.exe`, or run `python dusttrak_data_cleaner.py`).
2. Select one or more TSI DustTrak CSV files using the file picker (multi-select supported).
3. Output files are saved in the same folder as each input file.

---

## Building the executable

Requires [PyInstaller](https://pyinstaller.org):

```bash
pip install pyinstaller
pyinstaller dusttrak_data_cleaner.spec
```

The output `.exe` is written to `dist/`.

---

## Sample data

Three example DustTrak CSV files are provided in [`sample_data/`](sample_data/) for testing.

---

## Input file format

The tool expects standard TSI DustTrak DRX CSV exports containing:
- `Start Date` and `Start Time` metadata rows near the top
- A data section beginning with an `Elapsed Time [s]` header
- Concentration columns in mg/m³ (`PM1`, `PM2.5`, `PM4`, `PM10`, `TOTAL`)

---

## License

MIT — see [LICENSE](LICENSE).
