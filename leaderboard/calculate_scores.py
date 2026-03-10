from sklearn.metrics import f1_score
import pandas as pd


def compute_scores(ideal_pred, perturbed_pred, truth):

    merged_ideal = ideal_pred.merge(truth, on="graph_index")
    merged_perturbed = perturbed_pred.merge(truth, on="graph_index")

    y_true = merged_ideal["target"]

    f1_ideal = f1_score(y_true, merged_ideal["prediction"])
    f1_perturbed = f1_score(y_true, merged_perturbed["prediction"])

    robustness_gap = abs(f1_ideal - f1_perturbed)

    return {
        "f1_ideal": f1_ideal,
        "f1_perturbed": f1_perturbed,
        "robustness_gap": robustness_gap
    }
