"""Entry point for the Student Performance Analytics System."""

from pathlib import Path
import argparse

from functions import (
    calculate_student_metrics,
    get_department_analysis,
    get_subject_analysis,
    load_student_data,
    print_report,
)

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "data" / "students.csv"
DEFAULT_REPORTS = ROOT / "reports"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse student marks and attendance from a CSV dataset."
    )
    parser.add_argument(
        "--data", default=str(DEFAULT_DATA),
        help="Path to a student CSV file (default: data/students.csv)"
    )
    parser.add_argument(
        "--output-dir", default=str(DEFAULT_REPORTS),
        help="Directory where analysis CSV reports will be saved."
    )
    args = parser.parse_args()

    try:
        df = load_student_data(args.data)
        metrics = calculate_student_metrics(df)
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        metrics.to_csv(output_dir / "student_results.csv", index=False)
        get_subject_analysis(df).to_csv(output_dir / "subject_analysis.csv", index=False)
        get_department_analysis(metrics).to_csv(output_dir / "department_analysis.csv", index=False)

        print_report(df, metrics)
        print(f"\nReports saved to: {output_dir.resolve()}")
        print("Generated: student_results.csv, subject_analysis.csv, department_analysis.csv")
    except (OSError, ValueError, KeyError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
