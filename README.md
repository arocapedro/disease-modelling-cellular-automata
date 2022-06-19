# virus-sim

## 🚀 Usage

Install pre-requirements for the project

```sh
pip install -r requirements.txt
```

Run this command to see all the avalible option for this seir implementation

```sh
python seir_cli/seir_model.py --help
```

Run this command to run experiment

```sh
python seir_cli/seir_model.py --init_E 1 --init_I 1 --init_R 0 --init_pop_size 10000 --infection_rate 3.8 --incubation_rate 0.19 --recovery_rate 0.34 --days 100 --is_lockdown True --start_day 25 --duration_of_lockdown 14
```
