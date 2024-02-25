import math
import optuna

n_variables = 10


def objective(trial: optuna.Trial) -> float:
    x_list = []
    for i in range(n_variables):
        x_list.append(trial.suggest_float("x" + str(i), -5, 5))

    banana = 0
    for i in range(len(x_list) - 1):
        banana += 100 * (x_list[i + 1] - x_list[i] ** 2) ** 2 + (1 - x_list[i]) ** 2
    return banana


if __name__ == "__main__":
    studies = []
    seed = 10
    n_trails = 128

    storage = optuna.storages.JournalStorage(
        optuna.storages.JournalFileStorage("./journal.log"),
    )
    # storage = optuna.storages.InMemoryStorage()

    sampler = optuna.samplers.TPESampler(
        seed=seed, n_startup_trials=math.floor(n_trails / 2)
    )
    study = optuna.create_study(storage=storage, study_name="TPE", sampler=sampler)
    study.optimize(objective, n_trials=n_trails)
    studies.append(study)

    sampler = optuna.samplers.RandomSampler(seed=seed)
    study = optuna.create_study(storage=storage, study_name="Random", sampler=sampler)
    study.optimize(objective, n_trials=n_trails)
    studies.append(study)

    sampler = optuna.samplers.CmaEsSampler(seed=seed)
    study = optuna.create_study(storage=storage, study_name="CMA-ES", sampler=sampler)
    study.optimize(objective, n_trials=n_trails)
    studies.append(study)

    sampler = optuna.samplers.NSGAIISampler(seed=seed, population_size=25)
    study = optuna.create_study(storage=storage, study_name="NSGA-II", sampler=sampler)
    study.optimize(objective, n_trials=n_trails)
    studies.append(study)

    sampler = optuna.integration.BoTorchSampler(
        seed=seed, n_startup_trials=math.floor(n_trails / 2)
    )
    study = optuna.create_study(storage=storage, study_name="GP", sampler=sampler)
    study.optimize(objective, n_trials=n_trails)
    studies.append(study)

    sampler = optuna.samplers.QMCSampler(seed=seed, qmc_type="halton")
    study = optuna.create_study(storage=storage, study_name="QMC", sampler=sampler)
    study.optimize(objective, n_trials=n_trails)
    studies.append(study)

    fig = optuna.visualization.plot_optimization_history(studies)
    fig.update_layout(yaxis=dict(type="log"))
    fig.show()
    fig.write_html("10_variables_128_trials.html")
