import osimport argparse
import pandas as pd
import numpy as np

_TRAFFIC = "processed_data/uk_traffic.csv"
_AREAS = "processed_data/areas.csv"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="processed_data/")
    args = parser.parse_args()


    traffic = pd.read_csv(_TRAFFIC, index_col=0)
    areas = pd.read_csv(_AREAS, index_col=0)


    assert (np.diag(traffic) > 0).all()
    assert (traffic.sum(axis=1) > 0).all()

    populations = areas["population"]

    # %%
    np.fill_diagonal(traffic.values, 0)  # remove all diagonal terms, setting to zero

    # row normalized version
    traffic_prop = traffic.divide(populations, axis="index")

    np.fill_diagonal(
        traffic_prop.values,
        traffic_prop.sum(axis=1).values.max() - traffic_prop.sum(axis=1).values,
    )

    traffic_prop /= traffic_prop.sum(axis=1).max()

    assert np.isclose(traffic_prop.sum(axis=1).values, 1).all()

    traffic_prop.to_csv(os.path.join(args.output_dir, "traffic_flux_row-normed.csv"))

    # row normalized transpose version
    traffic_T_prop = traffic.divide(populations, axis="index")

    np.fill_diagonal(
        traffic_T_prop.values,
        traffic_T_prop.sum(axis=0).values.max() - traffic_T_prop.sum(axis=0).values,
    )

    traffic_T_prop /= traffic_T_prop.sum(axis=0).max()

    assert np.isclose(traffic_T_prop.sum(axis=0).values, 1).all()

    traffic_T_prop = traffic_T_prop.T
    traffic_T_prop.to_csv(os.path.join(args.output_dir, "traffic_flux_transpose_row-normed.csv"))
    # %%
    # Unnormalized version

