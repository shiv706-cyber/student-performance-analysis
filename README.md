# Student Performance Analytics System

A beginner-friendly Python data-analysis project that evaluates student marks and attendance using **Python, NumPy and Pandas**. It generates a clear terminal report and CSV files that can be opened in Excel or Google Sheets.

> **Dataset note:** `data/students.csv` contains fictional sample records created for demonstration. It is not real student data.

## Features

- Loads and validates student records from CSV using Pandas.
- Calculates total marks and average marks for each student.
- Assigns grades using a clearly defined grading scale.
- Determines Pass/Fail using subject marks and attendance.
- Calculates class average, highest/lowest average, pass count and pass percentage.
- Performs subject-wise analysis using NumPy.
- Compares departments and identifies top-performing students.
- Exports detailed results and analysis tables as CSV files.
- Includes reusable functions, input validation and automated tests.

## Technology used

- Python 3.10 or newer recommended
- Pandas
- NumPy
- `unittest` for tests (included with Python)

## Project structure

```text
student-performance-analytics/
├── data/
│   └── students.csv
├── reports/
│   └── .gitkeep
├── tests/
│   └── test_functions.py
├── Project_Documentation.md
├── README.md
├── functions.py
├── main.py
└── requirements.txt
```

## Run the project

### 1. Install Python
Install Python 3.10+ from [python.org](https://www.python.org/downloads/). During installation on Windows, select **Add Python to PATH**.

### 2. Open a terminal in the project folder

```bash
python -m venv .venv
```

Activate the environment:

**Windows Command Prompt**
```bat
.venv\Scripts\activate
```

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the analysis

```bash
python main.py
```

To use a different CSV file:

```bash
python main.py --data path/to/your_students.csv --output-dir reports
```

## Output files

After a successful run, the `reports/` directory contains:

| File | Contents |
|---|---|
| `student_results.csv` | Original records plus total, average, grade, result and rank |
| `subject_analysis.csv` | Average, highest, lowest and standard deviation per subject |
| `department_analysis.csv` | Student count, average and pass percentage by department |

The files are generated when the program runs and are intentionally not committed as fixed output snapshots.

## Rules used

### Grade scale

| Average marks | Grade |
|---:|:---|
| 90–100 | A+ |
| 80–89.99 | A |
| 70–79.99 | B |
| 60–69.99 | C |
| 50–59.99 | D |
| Below 50 | F |

### Pass/Fail rule

A student passes only when **all four subjects are at least 40 marks** and attendance is at least **75%**. Otherwise, the student is marked Fail. These are example project rules; an institution may use a different policy.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## GitHub submission

1. Create a new GitHub repository named `student-performance-analytics`.
2. Keep the repository public if that is what your trainer requires.
3. Upload the complete project folder, including the dataset, source code, tests and documentation.
4. Do **not** upload the `.venv/` folder or personal/real student information.
5. Check that `README.md` renders correctly and that the code runs from a clean setup.
6. Copy the repository URL and submit it through the Google Form supplied by your trainer.

Example Git commands (run from the project folder after creating an empty GitHub repository):

```bash
git init
git add .
git commit -m "Build student performance analytics system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/student-performance-analytics.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. The repository is not published until you complete these steps.

## Academic integrity

Use this project as a working reference, run it yourself, understand the grading and analysis rules, and be ready to explain each function during evaluation. Personalize the documentation and make sure your final submission reflects your own understanding.
