# leaderboard/calculate_scores.py
from pathlib import Path
import pandas as pd
from sklearn.metrics import f1_score
import os

# Ground truth labels
GROUND_TRUTH = Path(__file__).resolve().parent.parent / "data" / "train.csv"

def calculate_scores(submission_path: Path):
    """
    Compute F1 score for a single CSV submission and return as dict
    """
    print(f"DEBUG: Loading submission from {submission_path}")
    submission_df = pd.read_csv(submission_path)
    
    print(f"DEBUG: Submission columns: {list(submission_df.columns)}")
    
    # Check for graph_index column
    if "graph_index" not in submission_df.columns:
        raise ValueError(f"Submission missing required column: graph_index")
    
    # Find the prediction column (could be named various things)
    pred_col = None
    possible_pred_cols = ["label", "prediction", "target", "predictions", "Label", "Prediction", "Target"]
    
    for col in possible_pred_cols:
        if col in submission_df.columns:
            pred_col = col
            break
    
    if pred_col is None:
        raise ValueError(
            f"Could not find prediction column. Submission has columns: {list(submission_df.columns)}. "
            f"Expected one of: {possible_pred_cols}"
        )
    
    print(f"DEBUG: Using '{pred_col}' as prediction column")
    
    # Load ground truth
    print(f"DEBUG: Loading ground truth from {GROUND_TRUTH}")
    gt_df = pd.read_csv(GROUND_TRUTH)
    print(f"DEBUG: Ground truth columns: {list(gt_df.columns)}")
    
    # Find ground truth label column
    truth_col = None
    possible_truth_cols = ["label", "target", "Label", "Target"]
    
    for col in possible_truth_cols:
        if col in gt_df.columns:
            truth_col = col
            break
    
    if truth_col is None:
        raise ValueError(f"Could not find ground truth column in {GROUND_TRUTH}")
    
    print(f"DEBUG: Using '{truth_col}' as ground truth column")
    
    # Merge on graph_index
    merged = submission_df.merge(gt_df, on="graph_index", how="inner")
    print(f"DEBUG: Merged shape: {merged.shape}")
    
    y_pred = merged[pred_col]
    y_true = merged[truth_col]
    
    print(f"DEBUG: y_pred sample: {y_pred.head()}")
    print(f"DEBUG: y_true sample: {y_true.head()}")
    
    # Calculate F1 score
    f1 = f1_score(y_true, y_pred, average="macro")
    print(f"DEBUG: Calculated F1 score: {f1}")
    
    return {"validation_f1_score": f1}


def calculate_scores_pair(ideal_path: Path, perturbed_path: Path):
    """
    Compute ideal, perturbed F1 and robustness gap
    """
    f1_ideal = calculate_scores(ideal_path)["validation_f1_score"]
    f1_pert = calculate_scores(perturbed_path)["validation_f1_score"]
    robustness_gap = f1_ideal - f1_pert
    return {
        "validation_f1_ideal": f1_ideal,
        "validation_f1_perturbed": f1_pert,
        "robustness_gap": robustness_gap
    }
