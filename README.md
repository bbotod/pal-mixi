# PAL MIXI — Web Trainer (Flask)

A web-based simulator and task builder for the PAL MIXI logic circuit trainer.
Made by **Barna Botond**.

---

## Setup

### 1. Install Python (3.9 or newer)
Download from https://python.org if not already installed.

### 2. Install dependencies
Open a terminal/command prompt in this folder and run:

```
pip install -r requirements.txt
```

### 3. Run the server

```
python app.py
```

### 4. Open in browser
Go to: **http://localhost:5000**

---

## Features

### Simulator tab
- Select any task from the left panel
- Flip the input switches (A–F) to test combinations
- The LED lights up when output = 1
- Truth table on the right highlights the current row
- Download the current task's .mxf file
- Upload your own .mxf files (saved to the server)
- Delete tasks from the server

### Build Task tab
- Choose variables and their polarity (positive/complement)
- Add minterms (output = 1) and don't-cares (output = X)
- Live .mxf preview
- Save to server, download as .mxf, or test directly in the simulator

---

## .mxf Format

```
outputSignal|minterms|dontcares|x
```

- Fields separated by `|`
- Uppercase letter = variable is 1 (e.g. `A`)
- Lowercase letter = variable is 0 / complemented (e.g. `a` = Ā)
- Multiple terms separated by `+`
- Last field is always `x` or `X`

**Example:** `e|abcD+abCd+aBcd||x`
- Output signal: E
- 3 minterms: (ĀB̄C̄D), (ĀB̄CD̄), (ĀBC̄D̄)
- No don't-cares

---

## File structure

```
mixi_app/
├── app.py              ← Flask server
├── requirements.txt    ← Python dependencies
├── templates/
│   └── index.html      ← Web interface
└── tasks/
    ├── 1.mxf           ← Task files
    ├── ...
    └── Megoldasok/     ← Solution files
        ├── felad1.mxf
        └── ...
```
