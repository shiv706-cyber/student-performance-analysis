"""Reusable calculations and analysis for Student Performance Analytics."""

from __future__ import annotations

import numpy as np
import pandas as pd

SUBJECTS = ["Python", "Mathematics", "Statistics", "Communication"]
PASS_MARK = 40
MIN_ATTENDANCE = 75


def load_student_data(file_path: str) -> pd.DataFrame:
    """Load and validate student records from a CSV file."""
    df = pd.read_csv(file_path)
    required = {"Student_ID", "Name", "Department", *SUBJECTS, "Attendance"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    if df.empty:
        raise ValueError("The dataset contains no student records.")
    if df["Student_ID"].duplicated().any():
        duplicates = df.loc[df["Student_ID"].duplicated(), "Student_ID"].tolist()
        raise ValueError(f"Duplicate Student_ID values found: {duplicates}")
    for column in SUBJECTS + ["Attendance"]:
        df[column] = pd.to_numeric(df[column], errors="raise")
        if not df[column].between(0, 100).all():
            raise ValueError(f"{column} values must be between 0 and 100.")
    if df[["Student_ID", "Name", "Department"]].isna().any().any():
        raise ValueError("Student_ID, Name and Department cannot contain blank values.")
    return df


def calculate_student_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy enriched with total, average, grade and pass/fail columns."""
    result = df.copy()
    result["Total_Marks"] = result[SUBJECTS].sum(axis=1)
    result["Average_Marks"] = result[SUBJECTS].mean(axis=1).round(2)
    result["Grade"] = result["Average_Marks"].apply(assign_grade)
    subject_pass = result[SUBJECTS].ge(PASS_MARK).all(axis=1)
    attendance_pass = result["Attendance"].ge(MIN_ATTENDANCE)
    result["Result"] = np.where(subject_pass & attendance_pass, "Pass", "Fail")
    result["Rank"] = result["Average_Marks"].rank(method="min", ascending=False).astype(int)
    return result


def assign_grade(average: float) -> str:
    """Assign a grade based on average marks out of 100."""
    if average >= 90:
        return "A+"
    if average >= 80:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= 50:
        return "D"
    return "F"


def get_class_summary(metrics: pd.DataFrame) -> dict:
    """Calculate headline class statistics."""
    return {
        "student_count": int(len(metrics)),
        "class_average": round(float(metrics["Average_Marks"].mean()), 2),
        "highest_average": round(float(metrics["Average_Marks"].max()), 2),
        "lowest_average": round(float(metrics["Average_Marks"].min()), 2),
        "pass_count": int((metrics["Result"] == "Pass").sum()),
        "fail_count": int((metrics["Result"] == "Fail").sum()),
        "pass_percentage": round(float((metrics["Result"] == "Pass").mean() * 100), 2),
        "average_attendance": round(float(metrics["Attendance"].mean()), 2),
    }


def get_subject_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize average, highest, lowest and standard deviation by subject using NumPy."""
    rows = []
    for subject in SUBJECTS:
        values = df[subject].to_numpy(dtype=float)
        rows.append({
            "Subject": subject,
            "Average": round(float(np.mean(values)), 2),
            "Highest": round(float(np.max(values)), 2),
            "Lowest": round(float(np.min(values)), 2),
            "Std_Deviation": round(float(np.std(values)), 2),
        })
    return pd.DataFrame(rows)


def get_department_analysis(metrics: pd.DataFrame) -> pd.DataFrame:
    """Compare departments by student count, average and pass percentage."""
    grouped = metrics.groupby("Department", sort=True)
    return grouped.agg(
        Students=("Student_ID", "count"),
        Average_Marks=("Average_Marks", "mean"),
        Pass_Count=("Result", lambda values: (values == "Pass").sum()),
    ).assign(
        Pass_Percentage=lambda table: (
            table["Pass_Count"] / table["Students"] * 100
        ).round(2)
    ).assign(Average_Marks=lambda table: table["Average_Marks"].round(2)).reset_index()


def get_top_performers(metrics: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    """Return the top students by average marks, with rank as a tie-breaker."""
    return metrics.sort_values(
        ["Average_Marks", "Name"], ascending=[False, True]
    ).head(limit).reset_index(drop=True)


def print_report(df: pd.DataFrame, metrics: pd.DataFrame) -> None:
    """Print a readable summary and key analysis tables to the terminal."""
    summary = get_class_summary(metrics)
    print("\n" + "=" * 64)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 64)
    print(f"Students analysed       : {summary['student_count']}")
    print(f"Overall class average  : {summary['class_average']:.2f}/100")
    print(f"Highest student average: {summary['highest_average']:.2f}/100")
    print(f"Lowest student average : {summary['lowest_average']:.2f}/100")
    print(f"Pass / Fail             : {summary['pass_count']} / {summary['fail_count']}")
    print(f"Pass percentage         : {summary['pass_percentage']:.2f}%")
    print(f"Average attendance      : {summary['average_attendance']:.2f}%")

    print("\nSUBJECT-WISE ANALYSIS")
    print(get_subject_analysis(df).to_string(index=False))
    print("\nDEPARTMENT-WISE ANALYSIS")
    print(get_department_analysis(metrics).to_string(index=False))
    print("\nTOP 5 PERFORMERS")
    cols = ["Rank", "Student_ID", "Name", "Department", "Average_Marks", "Grade"]
    print(get_top_performers(metrics)[cols].to_string(index=False))
    print("\nSTUDENT RESULT SUMMARY")
    cols = ["Student_ID", "Name", "Total_Marks", "Average_Marks", "Grade", "Attendance", "Result"]
    print(metrics.sort_values("Rank")[cols].to_string(index=False))
