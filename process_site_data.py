import os
import sys
import argparse
import pandas as pd

UK_CASES_PATH = "processed_data/uk_cases.csv"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="processed_data/")
    args = parser.parse_args()

    uk_cases = pd.read_csv(UK_CASES_PATH)
    # RtCproj = pd.read_csv(RtCproj_PATH)

    df = (
        uk_cases.set_index(["Country", "Area name"])
        .stack()
        .to_frame()
        .reset_index()
        .rename(columns={"Area name": "area", "level_2": "Date", 0: "cases_new"})
    )
    df["cases_new_smoothed"] = df["cases_new"].rolling(7, center=True).mean()
    df["Date"] = pd.to_datetime(df["Date"])

    # Remove the last 5 days of actual cases which are exluded in the modelling due to being unreliable
    max_date = df["Date"].max()
    df = df[df["Date"] <= max_date - pd.offsets.Day(0)]

    df.to_csv(os.path.join(args.output_dir, "uk_cases.csv"), index=False)
    print("Wrote", os.path.join(args.output_dir, "uk_cases.csv"))
