# %%
import os
import re
import csv
import argparse
import pandas as pd
import numpy as np
from geopy import distance


from types import SimpleNamespace

_UK_CASES = "processed_data/uk_cases.csv"
_METADATA = "processed_data/metadata.csv"

# %%

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="processed_data/")
    args = parser.parse_args()

    uk_cases = pd.read_csv(_UK_CASES)
    uk_cases = uk_cases[
        ~uk_cases["Area name"].isin(["Outside Wales", "Unknown", "...17", "...18"])
    ].reset_index()
    N = len(uk_cases)
    areas = uk_cases["Area name"]
    quoted_areas = '"' + uk_cases["Area name"] + '"'

    metadata = pd.read_csv(_METADATA)
    metadata = metadata[metadata["AREA"].isin(areas)].reset_index(drop=True)

    geoloc = np.zeros((N, 2))
    geodist = np.zeros((N, N))
    population = np.zeros((N))

    meta_areas = metadata["AREA"]
    longitudes = metadata["LONG"]
    latitudes = metadata["LAT"]

    nhs_regions = metadata["NHS_Region"]
    nhs_regions_unique = nhs_regions.unique()
    nhs_regions_to_areas = np.zeros((N, 9))

    for i in range(N):
        area = areas[i]
        j = [
            ind for ind, s in enumerate(meta_areas) if re.compile(f"^{area}$").match(s)
        ]
        l = len(j) - 1
        if l >= 0:
            if l > 0:
                print(f"Area: {area}")
                print(f"Matched meta_areas {', '.join(meta_areas[j].to_list())}")
                print(f"Using {meta_areas[j[l]]}, {metadata.CODE[j[l]]}")

            geoloc[i, 0] = longitudes[j[l]]
            geoloc[i, 1] = latitudes[j[l]]
            population[i] = metadata.POPULATION[j[l]]

            nhs_row = nhs_regions_unique == nhs_regions[j[l]]
            nhs_regions_to_areas[i] = nhs_row
        else:
            print(f"Cannot find area {area}")
            for r in range(len(meta_areas)):
                if len([ind for ind, s in enumerate(meta_areas) if s in area]) > 0:
                    geoloc[i, 0] = longitudes[r]
                    geoloc[i, 1] = latitudes[r]
                    population[i] = metadata.POPULATION[r]
                    print(f"... found area {meta_area[r]}")

    pd.DataFrame(
        {
            "area": areas,
            "longitude": geoloc[:, 0],
            "latitude": geoloc[:, 1],
            "population": population.astype(int),
        }
    ).join(
        pd.DataFrame(
            nhs_regions_to_areas.astype(int),
            columns=[f"nhs_region.{i}" for i in range(nhs_regions_to_areas.shape[1])],
        )
    ).to_csv(
        os.path.join(args.output_dir, "areas.csv"),
        index=False,
        quoting=csv.QUOTE_NONNUMERIC,
    )

    pd.DataFrame({"nhs_region": nhs_regions_unique}).to_csv(
        os.path.join(args.output_dir, "nhs_regions.csv"),
        index=False,
        quoting=csv.QUOTE_NONE,
        escapechar="",
    )

    for i in range(N):
        for j in range(i, N):
            geodist[i, j] = distance.distance(geoloc[i], geoloc[j]).km / 100
            geodist[j, i] = geodist[i, j]

    geoDist = pd.DataFrame(geodist, index=areas.to_list(), columns=areas.to_list())
    geoDist.to_csv(
        os.path.join(args.output_dir, "distances.csv"),
        quoting=csv.QUOTE_NONNUMERIC,
    )
