# epimap-data

Data preprocessing code to pull together data about the UK to use in epimap models for local Rt estimation

### Set up

First update the path to your conda installation in line 2 of the [Makefile](Makefile) and run:

```{bash}
make install
```

### Preprocess data

```{bash}
make preprocess-data
```

The generated data files will be saved in the `processed_data` directory.
