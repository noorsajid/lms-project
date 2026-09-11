# ================================================================
# OULAD FINAL MACHINE LEARNING PIPELINE
# ================================================================
#
# Algorithms:
# 1. Random Forest
# 2. XGBoost
# 3. Gradient Boosting
#
# Workflow:
# Data Loading
# -> Duplicate Removal
# -> Data Cleaning
# -> Target Encoding
# -> Stratified Train/Test Split
# -> Model Comparison
# -> Best Model Selection
# -> Hyperparameter Tuning
# -> Final Test Evaluation
# -> Confusion Matrix
# -> Feature Importance
# -> Save Final Model
#
# ================================================================

import os
import time
import warnings
import joblib
import numpy as np
import pandas as pd

from xgboost import XGBClassifier

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    GridSearchCV
)

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from sklearn.utils.class_weight import compute_sample_weight

warnings.filterwarnings("ignore")


# ================================================================
# 1. SETTINGS
# ================================================================

DATA_FILE = r"C:\Users\Noor-sajid\Downloads\archive\oulad_selected_features.csv"

OUTPUT_DIR = r"C:\Users\Noor-sajid\Downloads\archive\ml_results"

TARGET = "final_result"

RANDOM_STATE = 42

TEST_SIZE = 0.20

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

START_TIME = time.time()


# ================================================================
# HELPER FUNCTION
# ================================================================

def separator():
    print("\n" + "=" * 75)


# ================================================================
# 2. START
# ================================================================

separator()

print("OULAD FINAL MACHINE LEARNING PIPELINE")

separator()


# ================================================================
# 3. LOAD DATA
# ================================================================

print("\n[1/12] Loading dataset...")

df = pd.read_csv(DATA_FILE)

print("Original Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ================================================================
# 4. DATA QUALITY CHECK
# ================================================================

separator()

print("DATA QUALITY CHECK")

separator()

print("\nMissing Values:")

print(
    df.isnull().sum().sum()
)


print("\nDuplicate Rows:")

duplicate_count = df.duplicated().sum()

print(duplicate_count)


# ================================================================
# 5. REMOVE DUPLICATES
# ================================================================

print("\n[2/12] Removing duplicate rows...")

if duplicate_count > 0:

    df = (
        df
        .drop_duplicates()
        .reset_index(drop=True)
    )

    print(
        f"Removed {duplicate_count} duplicate rows."
    )

else:

    print("No duplicate rows found.")


print(
    "Dataset Shape After Duplicate Removal:",
    df.shape
)


# ================================================================
# 6. TARGET CHECK
# ================================================================

print("\n[3/12] Checking target variable...")

if TARGET not in df.columns:

    raise ValueError(
        f"Target column '{TARGET}' was not found."
    )


print("\nTarget Distribution:")

print(
    df[TARGET].value_counts()
)


print("\nTarget Percentage:")

print(
    df[TARGET]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


# ================================================================
# 7. SEPARATE FEATURES AND TARGET
# ================================================================

print("\n[4/12] Separating features and target...")

X = df.drop(
    columns=[TARGET]
).copy()

y = df[TARGET].copy()


print("\nX Shape:", X.shape)

print("y Shape:", y.shape)


# ================================================================
# 8. HANDLE CATEGORICAL FEATURES
# ================================================================

print("\n[5/12] Preparing feature matrix...")

categorical_columns = (
    X
    .select_dtypes(
        include=["object", "category"]
    )
    .columns
    .tolist()
)


if len(categorical_columns) > 0:

    print("\nCategorical features detected:")

    for col in categorical_columns:

        print(" -", col)


    X = pd.get_dummies(
        X,
        columns=categorical_columns,
        drop_first=False
    )

else:

    print("\nNo categorical features detected.")


# ================================================================
# 9. CLEAN FEATURES
# ================================================================

print("\nCleaning feature matrix...")


# Convert Boolean columns to integers

for column in X.columns:

    if X[column].dtype == "bool":

        X[column] = X[column].astype(int)


# Convert all features to numeric

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)


# Replace infinity values

X = X.replace(
    [np.inf, -np.inf],
    np.nan
)


# Fill missing values using median

X = X.fillna(
    X.median(numeric_only=True)
)


print(
    "\nFinal Feature Matrix:",
    X.shape
)


# ================================================================
# 10. TARGET ENCODING
# ================================================================

print("\n[6/12] Encoding target variable...")


target_mapping = {

    "Distinction": 0,

    "Fail": 1,

    "Pass": 2,

    "Withdrawn": 3
}


y_encoded = y.map(
    target_mapping
)


if y_encoded.isnull().any():

    unknown_classes = (
        y[y_encoded.isnull()]
        .unique()
    )

    raise ValueError(
        f"Unknown target classes: {unknown_classes}"
    )


y_encoded = y_encoded.astype(int)


print("\nTarget Encoding:")

for label, code in target_mapping.items():

    print(
        f" - {label} -> {code}"
    )


# ================================================================
# 11. TRAIN TEST SPLIT
# ================================================================

print(
    "\n[7/12] Creating stratified train/test split..."
)


X_train, X_test, y_train, y_test = train_test_split(

    X,

    y_encoded,

    test_size=TEST_SIZE,

    random_state=RANDOM_STATE,

    stratify=y_encoded
)


print("\nTraining Data:")

print(
    "X_train:",
    X_train.shape
)

print(
    "y_train:",
    y_train.shape
)


print("\nTesting Data:")

print(
    "X_test:",
    X_test.shape
)

print(
    "y_test:",
    y_test.shape
)


print("\nTraining Class Distribution:")

print(
    y_train
    .value_counts()
    .sort_index()
)


print("\nTesting Class Distribution:")

print(
    y_test
    .value_counts()
    .sort_index()
)


# ================================================================
# 12. CLASS WEIGHTS
# ================================================================

sample_weights = compute_sample_weight(

    class_weight="balanced",

    y=y_train
)


print(
    "\nBalanced sample weights calculated."
)


# ================================================================
# 13. DEFINE THREE MODELS
# ================================================================

separator()

print("MODEL PREPARATION")

separator()


models = {

    # ------------------------------------------------------------
    # RANDOM FOREST
    # ------------------------------------------------------------

    "Random Forest":

        RandomForestClassifier(

            n_estimators=300,

            max_depth=None,

            min_samples_split=2,

            min_samples_leaf=1,

            class_weight="balanced",

            random_state=RANDOM_STATE,

            n_jobs=-1
        ),


    # ------------------------------------------------------------
    # XGBOOST
    # ------------------------------------------------------------

    "XGBoost":

        XGBClassifier(

            n_estimators=300,

            max_depth=6,

            learning_rate=0.05,

            subsample=0.8,

            colsample_bytree=0.8,

            objective="multi:softmax",

            num_class=4,

            eval_metric="mlogloss",

            random_state=RANDOM_STATE,

            n_jobs=-1,

            tree_method="hist"
        ),


    # ------------------------------------------------------------
    # GRADIENT BOOSTING
    # ------------------------------------------------------------

    "Gradient Boosting":

        GradientBoostingClassifier(

            n_estimators=150,

            learning_rate=0.05,

            max_depth=3,

            min_samples_split=2,

            min_samples_leaf=1,

            random_state=RANDOM_STATE
        )
}


print("\nAlgorithms:")

for model_name in models:

    print(
        " -",
        model_name
    )


# ================================================================
# 14. TRAIN AND COMPARE MODELS
# ================================================================

separator()

print("BASELINE MODEL COMPARISON")

separator()


results = []

trained_models = {}

predictions = {}

classification_reports = {}

confusion_matrices = {}


class_names = [

    "Distinction",

    "Fail",

    "Pass",

    "Withdrawn"
]


for model_name, model in models.items():

    print("\n" + "-" * 75)

    print(
        f"TRAINING: {model_name}"
    )

    print("-" * 75)


    start = time.time()


    # ------------------------------------------------------------
    # TRAIN
    # ------------------------------------------------------------

    if model_name in [

        "XGBoost",

        "Gradient Boosting"

    ]:

        model.fit(

            X_train,

            y_train,

            sample_weight=sample_weights

        )

    else:

        model.fit(

            X_train,

            y_train

        )


    training_time = (
        time.time() - start
    )


    # ------------------------------------------------------------
    # PREDICTION
    # ------------------------------------------------------------

    y_pred = model.predict(
        X_test
    )


    # ------------------------------------------------------------
    # METRICS
    # ------------------------------------------------------------

    accuracy = accuracy_score(

        y_test,

        y_pred
    )


    balanced_accuracy = balanced_accuracy_score(

        y_test,

        y_pred
    )


    precision = precision_score(

        y_test,

        y_pred,

        average="weighted",

        zero_division=0
    )


    recall = recall_score(

        y_test,

        y_pred,

        average="weighted",

        zero_division=0
    )


    f1_weighted = f1_score(

        y_test,

        y_pred,

        average="weighted",

        zero_division=0
    )


    f1_macro = f1_score(

        y_test,

        y_pred,

        average="macro",

        zero_division=0
    )


    # ------------------------------------------------------------
    # PRINT RESULTS
    # ------------------------------------------------------------

    print(
        f"\nAccuracy:            {accuracy:.4f}"
    )

    print(
        f"Balanced Accuracy:   {balanced_accuracy:.4f}"
    )

    print(
        f"Precision:           {precision:.4f}"
    )

    print(
        f"Recall:              {recall:.4f}"
    )

    print(
        f"F1 Weighted:        {f1_weighted:.4f}"
    )

    print(
        f"F1 Macro:           {f1_macro:.4f}"
    )

    print(
        f"Training Time:      {training_time:.2f} sec"
    )


    # ------------------------------------------------------------
    # CLASSIFICATION REPORT
    # ------------------------------------------------------------

    report = classification_report(

        y_test,

        y_pred,

        labels=[0, 1, 2, 3],

        target_names=class_names,

        digits=4,

        zero_division=0
    )


    print("\nClassification Report:")

    print(report)


    # ------------------------------------------------------------
    # CONFUSION MATRIX
    # ------------------------------------------------------------

    cm = confusion_matrix(

        y_test,

        y_pred,

        labels=[0, 1, 2, 3]
    )


    print("Confusion Matrix:")

    print(cm)


    # ------------------------------------------------------------
    # SAVE RESULTS IN MEMORY
    # ------------------------------------------------------------

    results.append({

        "Model": model_name,

        "Accuracy": accuracy,

        "Balanced Accuracy": balanced_accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1 Weighted": f1_weighted,

        "F1 Macro": f1_macro,

        "Training Time (sec)": training_time
    })


    trained_models[model_name] = model

    predictions[model_name] = y_pred

    classification_reports[model_name] = report

    confusion_matrices[model_name] = cm


# ================================================================
# 15. MODEL COMPARISON TABLE
# ================================================================

separator()

print("MODEL COMPARISON")

separator()


results_df = pd.DataFrame(
    results
)


results_df = (

    results_df

    .sort_values(

        by="F1 Macro",

        ascending=False

    )

    .reset_index(drop=True)
)


results_df.insert(

    0,

    "Rank",

    range(

        1,

        len(results_df) + 1

    )
)


print(

    results_df.to_string(

        index=False,

        float_format=lambda x:

        f"{x:.4f}"
    )
)


# ================================================================
# 16. SAVE BASELINE RESULTS
# ================================================================

baseline_file = os.path.join(

    OUTPUT_DIR,

    "baseline_model_comparison.csv"
)


results_df.to_csv(

    baseline_file,

    index=False
)


print(
    "\nBaseline comparison saved:"
)

print(
    baseline_file
)


# ================================================================
# 17. SELECT BEST MODEL
# ================================================================

best_model_name = (

    results_df.iloc[0]["Model"]
)


print("\n" + "=" * 75)

print("BEST BASELINE MODEL")

print("=" * 75)


print(
    "\nBest Model:",
    best_model_name
)


print(

    "Macro F1:",

    round(

        results_df.iloc[0]["F1 Macro"],

        4
    )
)


print(

    "Accuracy:",

    round(

        results_df.iloc[0]["Accuracy"],

        4
    )
)


# ================================================================
# 18. HYPERPARAMETER TUNING
# ================================================================

print(
    "\n[8/12] Starting hyperparameter tuning..."
)


print(
    "\nSelected model:",
    best_model_name
)


cv = StratifiedKFold(

    n_splits=3,

    shuffle=True,

    random_state=RANDOM_STATE
)


# ================================================================
# PARAMETER GRID
# ================================================================

if best_model_name == "Random Forest":

    tuning_model = RandomForestClassifier(

        random_state=RANDOM_STATE,

        class_weight="balanced",

        n_jobs=-1
    )


    param_grid = {

        "n_estimators": [

            200,

            300
        ],

        "max_depth": [

            None,

            15,

            25
        ],

        "min_samples_split": [

            2,

            5
        ],

        "min_samples_leaf": [

            1,

            2
        ]
    }


elif best_model_name == "XGBoost":

    tuning_model = XGBClassifier(

        objective="multi:softmax",

        num_class=4,

        eval_metric="mlogloss",

        random_state=RANDOM_STATE,

        n_jobs=-1,

        tree_method="hist"
    )


    # Reduced grid to avoid excessive execution time

    param_grid = {

        "n_estimators": [

            200,

            300
        ],

        "max_depth": [

            3,

            5
        ],

        "learning_rate": [

            0.05,

            0.10
        ],

        "subsample": [

            0.8,

            1.0
        ],

        "colsample_bytree": [

            0.8,

            1.0
        ]
    }


else:

    tuning_model = GradientBoostingClassifier(

        random_state=RANDOM_STATE
    )


    param_grid = {

        "n_estimators": [

            100,

            150
        ],

        "learning_rate": [

            0.05,

            0.10
        ],

        "max_depth": [

            2,

            3
        ],

        "min_samples_split": [

            2,

            5
        ],

        "min_samples_leaf": [

            1,

            2
        ]
    }


# ================================================================
# GRID SEARCH
# ================================================================

print("\nRunning GridSearchCV...")

print(
    "Scoring: F1 Macro"
)

print(
    "Cross-validation: 3 folds"
)


tuning_start = time.time()


grid_search = GridSearchCV(

    estimator=tuning_model,

    param_grid=param_grid,

    scoring="f1_macro",

    cv=cv,

    n_jobs=-1,

    verbose=1,

    return_train_score=False
)


# ---------------------------------------------------------------
# FIT GRID SEARCH
# ---------------------------------------------------------------

if best_model_name in [

    "XGBoost",

    "Gradient Boosting"

]:

    grid_search.fit(

        X_train,

        y_train,

        sample_weight=sample_weights

    )

else:

    grid_search.fit(

        X_train,

        y_train

    )


tuning_time = (

    time.time() - tuning_start
)


# ================================================================
# 19. BEST HYPERPARAMETERS
# ================================================================

separator()

print("BEST HYPERPARAMETERS")

separator()


print("\nBest Parameters:")

for parameter, value in (

    grid_search.best_params_.items()

):

    print(

        f" - {parameter}: {value}"
    )


print(

    "\nBest CV Macro F1:",

    round(

        grid_search.best_score_,

        4
    )
)


print(

    "\nTuning Time:",

    round(

        tuning_time / 60,

        2
    ),

    "minutes"
)


# ================================================================
# 20. FINAL TUNED MODEL
# ================================================================

final_model = (

    grid_search.best_estimator_
)


# ================================================================
# 21. FINAL TEST PREDICTION
# ================================================================

print(
    "\n[9/12] Evaluating final tuned model..."
)


final_predictions = (

    final_model.predict(

        X_test
    )
)


# ================================================================
# 22. FINAL METRICS
# ================================================================

final_accuracy = accuracy_score(

    y_test,

    final_predictions
)


final_balanced_accuracy = balanced_accuracy_score(

    y_test,

    final_predictions
)


final_precision = precision_score(

    y_test,

    final_predictions,

    average="weighted",

    zero_division=0
)


final_recall = recall_score(

    y_test,

    final_predictions,

    average="weighted",

    zero_division=0
)


final_f1_weighted = f1_score(

    y_test,

    final_predictions,

    average="weighted",

    zero_division=0
)


final_f1_macro = f1_score(

    y_test,

    final_predictions,

    average="macro",

    zero_division=0
)


# ================================================================
# 23. FINAL RESULTS
# ================================================================

separator()

print("FINAL TUNED MODEL RESULTS")

separator()


print(
    f"\nModel:              {best_model_name}"
)

print(
    f"Accuracy:           {final_accuracy:.4f}"
)

print(
    f"Balanced Accuracy:  {final_balanced_accuracy:.4f}"
)

print(
    f"Precision:          {final_precision:.4f}"
)

print(
    f"Recall:             {final_recall:.4f}"
)

print(
    f"F1 Weighted:        {final_f1_weighted:.4f}"
)

print(
    f"F1 Macro:           {final_f1_macro:.4f}"
)


# ================================================================
# 24. FINAL CLASSIFICATION REPORT
# ================================================================

final_report = classification_report(

    y_test,

    final_predictions,

    labels=[0, 1, 2, 3],

    target_names=class_names,

    digits=4,

    zero_division=0
)


print("\nClassification Report:")

print(final_report)


# ================================================================
# 25. FINAL CONFUSION MATRIX
# ================================================================

final_cm = confusion_matrix(

    y_test,

    final_predictions,

    labels=[0, 1, 2, 3]
)


final_cm_df = pd.DataFrame(

    final_cm,

    index=class_names,

    columns=class_names
)


print("\nFinal Confusion Matrix:")

print(final_cm_df)


# ================================================================
# 26. SAVE FINAL RESULTS
# ================================================================

print(
    "\n[10/12] Saving final results..."
)


final_results_df = pd.DataFrame([{

    "Model": best_model_name,

    "Accuracy": final_accuracy,

    "Balanced Accuracy":
        final_balanced_accuracy,

    "Precision":
        final_precision,

    "Recall":
        final_recall,

    "F1 Weighted":
        final_f1_weighted,

    "F1 Macro":
        final_f1_macro,

    "CV F1 Macro":
        grid_search.best_score_,

    "Tuning Time (min)":
        tuning_time / 60

}])


final_results_file = os.path.join(

    OUTPUT_DIR,

    "final_model_results.csv"
)


final_results_df.to_csv(

    final_results_file,

    index=False
)


# ================================================================
# 27. SAVE CONFUSION MATRIX
# ================================================================

confusion_file = os.path.join(

    OUTPUT_DIR,

    "final_confusion_matrix.csv"
)


final_cm_df.to_csv(

    confusion_file
)


# ================================================================
# 28. SAVE CLASSIFICATION REPORT
# ================================================================

report_file = os.path.join(

    OUTPUT_DIR,

    "final_classification_report.txt"
)


with open(

    report_file,

    "w",

    encoding="utf-8"

) as file:

    file.write(

        "OULAD FINAL MODEL CLASSIFICATION REPORT\n"
    )

    file.write(

        "=" * 75 + "\n\n"
    )

    file.write(

        f"Model: {best_model_name}\n\n"
    )

    file.write(

        final_report
    )


# ================================================================
# 29. FEATURE IMPORTANCE
# ================================================================

print(
    "\n[11/12] Extracting feature importance..."
)


if hasattr(

    final_model,

    "feature_importances_"

):

    importance = (

        final_model.feature_importances_
    )


    feature_importance_df = pd.DataFrame({

        "Feature":
            X_train.columns,

        "Importance":
            importance
    })


    feature_importance_df = (

        feature_importance_df

        .sort_values(

            by="Importance",

            ascending=False
        )

        .reset_index(drop=True)
    )


    feature_importance_df.insert(

        0,

        "Rank",

        range(

            1,

            len(feature_importance_df) + 1
        )
    )


    print("\nTop 20 Features:")

    print(

        feature_importance_df

        .head(20)

        .to_string(index=False)
    )


    importance_file = os.path.join(

        OUTPUT_DIR,

        "final_feature_importance.csv"
    )


    feature_importance_df.to_csv(

        importance_file,

        index=False
    )


    print(
        "\nFeature importance saved:"
    )

    print(
        importance_file
    )


else:

    print(
        "\nFeature importance is not available."
    )


# ================================================================
# 30. SAVE FINAL MODEL
# ================================================================

print(
    "\n[12/12] Saving final model..."
)


final_model_file = os.path.join(

    OUTPUT_DIR,

    "final_oulad_model.pkl"
)


joblib.dump(

    final_model,

    final_model_file
)


print(
    "\nFinal model saved:"
)

print(
    final_model_file
)


# ================================================================
# 31. SAVE TARGET MAPPING
# ================================================================

mapping_file = os.path.join(

    OUTPUT_DIR,

    "target_mapping.pkl"
)


joblib.dump(

    target_mapping,

    mapping_file
)


# ================================================================
# 32. SAVE TEST PREDICTIONS
# ================================================================

prediction_df = pd.DataFrame({

    "Actual_Encoded":
        y_test.values,

    "Predicted_Encoded":
        final_predictions
})


reverse_mapping = {

    0: "Distinction",

    1: "Fail",

    2: "Pass",

    3: "Withdrawn"
}


prediction_df[

    "Actual_Result"

] = prediction_df[

    "Actual_Encoded"

].map(

    reverse_mapping
)


prediction_df[

    "Predicted_Result"

] = prediction_df[

    "Predicted_Encoded"

].map(

    reverse_mapping
)


prediction_file = os.path.join(

    OUTPUT_DIR,

    "final_model_predictions.csv"
)


prediction_df.to_csv(

    prediction_file,

    index=False
)


# ================================================================
# 33. SAVE GRID SEARCH RESULTS
# ================================================================

grid_file = os.path.join(

    OUTPUT_DIR,

    "hyperparameter_tuning_results.csv"
)


pd.DataFrame(

    grid_search.cv_results_

).to_csv(

    grid_file,

    index=False
)


# ================================================================
# 34. FINAL SUMMARY
# ================================================================

total_time = (

    time.time()

    -

    START_TIME
)


separator()

print("PIPELINE COMPLETED SUCCESSFULLY")

separator()


print(

    "\nOriginal Dataset:",

    df.shape
)


print(

    "Training Dataset:",

    X_train.shape
)


print(

    "Testing Dataset:",

    X_test.shape
)


print(

    "\nDuplicates Removed:",

    duplicate_count
)


print(

    "Models Compared:",

    len(models)
)


print(

    "\nBaseline Best Model:",

    best_model_name
)


print(

    "Final Accuracy:",

    round(

        final_accuracy,

        4
    )
)


print(

    "Final Balanced Accuracy:",

    round(

        final_balanced_accuracy,

        4
    )
)


print(

    "Final Macro F1:",

    round(

        final_f1_macro,

        4
    )
)


print(

    "Final Weighted F1:",

    round(

        final_f1_weighted,

        4
    )
)


print(

    "\nTotal Execution Time:",

    round(

        total_time / 60,

        2
    ),

    "minutes"
)


# ================================================================
# OUTPUT FILES
# ================================================================

separator()

print("OUTPUT FILES")

separator()


print(
    "\n1. Baseline Model Comparison:"
)

print(
    baseline_file
)


print(
    "\n2. Final Model Results:"
)

print(
    final_results_file
)


print(
    "\n3. Final Confusion Matrix:"
)

print(
    confusion_file
)


print(
    "\n4. Classification Report:"
)

print(
    report_file
)


print(
    "\n5. Feature Importance:"
)

print(

    os.path.join(

        OUTPUT_DIR,

        "final_feature_importance.csv"
    )
)


print(
    "\n6. Hyperparameter Tuning:"
)

print(
    grid_file
)


print(
    "\n7. Final Model:"
)

print(
    final_model_file
)


print(
    "\n8. Target Mapping:"
)

print(
    mapping_file
)


print(
    "\n9. Test Predictions:"
)

print(
    prediction_file
)


separator()

print("READY FOR THESIS MODEL ANALYSIS")

separator()

# ================================================================
# [FINAL] AFTER HYPERPARAMETER TUNING
# ================================================================

print("\n" + "=" * 75)
print("HYPERPARAMETER TUNING COMPLETED")
print("=" * 75)

print("\nBest Parameters:")
print(grid_search.best_params_)

print("\nBest Cross-Validation Macro F1:")
print(f"{grid_search.best_score_:.4f}")


# ================================================================
# 1. FINAL TUNED MODEL
# ================================================================

print("\n" + "=" * 75)
print("FINAL TUNED MODEL")
print("=" * 75)

final_model = grid_search.best_estimator_

print("\nFinal Model:")
print(final_model)


# ================================================================
# 2. FINAL TEST EVALUATION
# ================================================================

print("\n" + "=" * 75)
print("FINAL TEST EVALUATION")
print("=" * 75)

# Predict on completely unseen test data
final_predictions = final_model.predict(X_test)


# ================================================================
# PERFORMANCE METRICS
# ================================================================

final_accuracy = accuracy_score(
    y_test,
    final_predictions
)

final_balanced_accuracy = balanced_accuracy_score(
    y_test,
    final_predictions
)

final_precision = precision_score(
    y_test,
    final_predictions,
    average="weighted",
    zero_division=0
)

final_recall = recall_score(
    y_test,
    final_predictions,
    average="weighted",
    zero_division=0
)

final_f1_weighted = f1_score(
    y_test,
    final_predictions,
    average="weighted",
    zero_division=0
)

final_f1_macro = f1_score(
    y_test,
    final_predictions,
    average="macro",
    zero_division=0
)


print("\nFINAL MODEL PERFORMANCE")
print("-" * 75)

print(f"Accuracy:             {final_accuracy:.4f}")
print(f"Balanced Accuracy:    {final_balanced_accuracy:.4f}")
print(f"Precision:            {final_precision:.4f}")
print(f"Recall:               {final_recall:.4f}")
print(f"F1 Weighted:          {final_f1_weighted:.4f}")
print(f"F1 Macro:             {final_f1_macro:.4f}")


# ================================================================
# 3. CLASSIFICATION REPORT
# ================================================================

print("\n" + "=" * 75)
print("CLASSIFICATION REPORT")
print("=" * 75)

final_report = classification_report(
    y_test,
    final_predictions,
    labels=[0, 1, 2, 3],
    target_names=class_names,
    digits=4,
    zero_division=0
)

print(final_report)


# ================================================================
# 4. CONFUSION MATRIX
# ================================================================

print("\n" + "=" * 75)
print("CONFUSION MATRIX")
print("=" * 75)

final_cm = confusion_matrix(
    y_test,
    final_predictions,
    labels=[0, 1, 2, 3]
)

final_cm_df = pd.DataFrame(
    final_cm,
    index=class_names,
    columns=class_names
)

print("\n")
print(final_cm_df)


# Save confusion matrix
confusion_file = os.path.join(
    OUTPUT_DIR,
    "final_confusion_matrix.csv"
)

final_cm_df.to_csv(
    confusion_file
)

print("\nConfusion Matrix saved:")
print(confusion_file)


# ================================================================
# 5. FEATURE IMPORTANCE
# ================================================================

print("\n" + "=" * 75)
print("FEATURE IMPORTANCE")
print("=" * 75)

if hasattr(final_model, "feature_importances_"):

    feature_importance_df = pd.DataFrame({

        "Feature": X_train.columns,

        "Importance": final_model.feature_importances_

    })

    # Sort highest importance first
    feature_importance_df = (
        feature_importance_df
        .sort_values(
            by="Importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # Add ranking
    feature_importance_df.insert(
        0,
        "Rank",
        range(
            1,
            len(feature_importance_df) + 1
        )
    )

    print("\nFeature Importance:")
    print(
        feature_importance_df.to_string(
            index=False
        )
    )

    # Save feature importance
    importance_file = os.path.join(
        OUTPUT_DIR,
        "final_feature_importance.csv"
    )

    feature_importance_df.to_csv(
        importance_file,
        index=False
    )

    print("\nFeature Importance saved:")
    print(importance_file)

else:

    print(
        "\nFeature importance is not available "
        "for this model."
    )


# ================================================================
# 6. SAVE FINAL MODEL
# ================================================================

print("\n" + "=" * 75)
print("SAVING FINAL MODEL")
print("=" * 75)

model_file = os.path.join(
    OUTPUT_DIR,
    "final_oulad_model.pkl"
)

joblib.dump(
    final_model,
    model_file
)

print("\nFinal Model Saved:")
print(model_file)


# ================================================================
# 7. SAVE TARGET MAPPING
# ================================================================

mapping_file = os.path.join(
    OUTPUT_DIR,
    "target_mapping.pkl"
)

joblib.dump(
    target_mapping,
    mapping_file
)

print("\nTarget Mapping Saved:")
print(mapping_file)


# ================================================================
# 8. SAVE FEATURE NAMES
# ================================================================

feature_file = os.path.join(
    OUTPUT_DIR,
    "feature_names.pkl"
)

joblib.dump(
    list(X_train.columns),
    feature_file
)

print("\nFeature Names Saved:")
print(feature_file)


# ================================================================
# 9. SAVE TEST PREDICTIONS
# ================================================================

prediction_df = pd.DataFrame({

    "Actual_Encoded":
        y_test.values,

    "Predicted_Encoded":
        final_predictions

})

reverse_mapping = {
    0: "Distinction",
    1: "Fail",
    2: "Pass",
    3: "Withdrawn"
}

prediction_df["Actual_Result"] = (
    prediction_df["Actual_Encoded"]
    .map(reverse_mapping)
)

prediction_df["Predicted_Result"] = (
    prediction_df["Predicted_Encoded"]
    .map(reverse_mapping)
)

prediction_file = os.path.join(
    OUTPUT_DIR,
    "final_model_predictions.csv"
)

prediction_df.to_csv(
    prediction_file,
    index=False
)

print("\nTest Predictions Saved:")
print(prediction_file)


# ================================================================
# 10. SAVE FINAL MODEL RESULTS
# ================================================================

final_results_df = pd.DataFrame([{

    "Model":
        best_model_name,

    "Accuracy":
        final_accuracy,

    "Balanced Accuracy":
        final_balanced_accuracy,

    "Precision":
        final_precision,

    "Recall":
        final_recall,

    "F1 Weighted":
        final_f1_weighted,

    "F1 Macro":
        final_f1_macro,

    "CV F1 Macro":
        grid_search.best_score_

}])


results_file = os.path.join(
    OUTPUT_DIR,
    "final_model_results.csv"
)

final_results_df.to_csv(
    results_file,
    index=False
)

print("\nFinal Results Saved:")
print(results_file)


# ================================================================
# 11. SAVE CLASSIFICATION REPORT
# ================================================================

report_file = os.path.join(
    OUTPUT_DIR,
    "final_classification_report.txt"
)

with open(
    report_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "OULAD FINAL MODEL CLASSIFICATION REPORT\n"
    )

    file.write(
        "=" * 75 + "\n\n"
    )

    file.write(
        f"Model: {best_model_name}\n\n"
    )

    file.write(
        f"Accuracy: {final_accuracy:.4f}\n"
    )

    file.write(
        f"Balanced Accuracy: "
        f"{final_balanced_accuracy:.4f}\n"
    )

    file.write(
        f"Precision: {final_precision:.4f}\n"
    )

    file.write(
        f"Recall: {final_recall:.4f}\n"
    )

    file.write(
        f"F1 Weighted: {final_f1_weighted:.4f}\n"
    )

    file.write(
        f"F1 Macro: {final_f1_macro:.4f}\n\n"
    )

    file.write(
        "Classification Report:\n\n"
    )

    file.write(
        final_report
    )

print("\nClassification Report Saved:")
print(report_file)


# ================================================================
# 12. SAVE GRID SEARCH RESULTS
# ================================================================

grid_file = os.path.join(
    OUTPUT_DIR,
    "hyperparameter_tuning_results.csv"
)

pd.DataFrame(
    grid_search.cv_results_
).to_csv(
    grid_file,
    index=False
)

print("\nHyperparameter Tuning Results Saved:")
print(grid_file)


# ================================================================
# FINAL SUMMARY
# ================================================================

print("\n" + "=" * 75)
print("OULAD MACHINE LEARNING PIPELINE COMPLETED")
print("=" * 75)

print("\nFinal Model:")
print(best_model_name)

print("\nFinal Performance:")
print(f"Accuracy:          {final_accuracy:.4f}")
print(f"Balanced Accuracy: {final_balanced_accuracy:.4f}")
print(f"F1 Weighted:       {final_f1_weighted:.4f}")
print(f"F1 Macro:          {final_f1_macro:.4f}")

print("\n" + "-" * 75)
print("GENERATED FILES")
print("-" * 75)

print("\n1. Final Model:")
print(model_file)

print("\n2. Target Mapping:")
print(mapping_file)

print("\n3. Feature Names:")
print(feature_file)

print("\n4. Confusion Matrix:")
print(confusion_file)

print("\n5. Feature Importance:")
print(
    os.path.join(
        OUTPUT_DIR,
        "final_feature_importance.csv"
    )
)

print("\n6. Final Results:")
print(results_file)

print("\n7. Classification Report:")
print(report_file)

print("\n8. Test Predictions:")
print(prediction_file)

print("\n9. Hyperparameter Tuning Results:")
print(grid_file)

print("\n" + "=" * 75)
print("READY FOR FLASK API")
print("=" * 75)