# Predictive Modeling Experiments

## Evaluation setup

- Stratified 80/20 split with random_state=42.
- Training: 8,000 customers; reserved test: 2,000 customers.
- No customers overlap between the two portions.
- Models compared using the same five stratified validation folds.
- Imputation, scaling, and encoding fitted inside each fold.
- Customer ID excluded from model inputs.
- Prior exploration used the full dataset, so the reserved test
  portion is not completely independent of exploratory choices.

## Mean cross-validation results

| Model | Accuracy | Precision | Recall | F1 | ROC AUC | Average precision |
|---|---:|---:|---:|---:|---:|---:|
| Dummy | 0.7962 | 0.0000 | 0.0000 | 0.0000 | 0.5000 | 0.2037 |
| Logistic regression | 0.7409 | 0.4222 | 0.7362 | 0.5366 | 0.8184 | 0.5815 |
| Random forest | 0.7712 | 0.4610 | 0.7245 | 0.5634 | 0.8415 | 0.6489 |

Dummy precision is undefined because it predicts no churners;
the evaluation code records it as zero.

## Initial interpretation

The random forest has higher mean precision, F1, ROC AUC,
and average precision than logistic regression.
Logistic regression has slightly higher recall.

Both trained models use balanced class weights and the default
classification threshold. Their scores have not been calibrated
as real-world churn probabilities.

## Tuning objective

Used F1 as the primary tuning metric for this educational project,
while continuing to report precision, recall, ROC AUC, and average
precision. Business costs and contact capacity have not been supplied,
so this is not a claim that F1 is the optimal business objective.

Keep the reserved test data out of tuning and model selection.

## Random forest tuning

Eight configurations were compared using five-fold stratified
cross-validation on the training data. Selection used mean F1.

Selected settings:
- n_estimators: 300
- max_depth: 8
- max_features: 0.7
- min_samples_leaf: 5
- class_weight: balanced
- random_state: 42

Selected configuration's mean CV results:
- Accuracy: 0.7892
- Precision: 0.4880
- Recall: 0.6945
- F1: 0.5730
- ROC AUC: 0.8416
- Average precision: 0.6532

F1 improved modestly from 0.5634 to 0.5730, with higher precision
and lower recall. Ranking performance changed little.

These validation folds also guided selection, so the selected
score may be optimistic. This is not independent confirmation
that tuning improved performance.

## Final evaluation decision

Selected the tuned random forest using the settings above.
Keep the default classification threshold of 0.5.

Preprocessing and the classifier were fitted on all 8,000 training rows,
then evaluated on the 2,000 reserved test rows.
Do not use test results to revise settings or the threshold.
Earlier full-dataset exploration remains an evaluation limitation.

## Final test results

| Metric | Test result |
|---|---:|
| Accuracy | 0.8130 |
| Precision | 0.5286 |
| Recall | 0.7494 |
| F1 | 0.6199 |
| ROC AUC | 0.8622 |
| Average precision | 0.6967 |

Of 407 churners in the test split, 305 were identified and 102 missed.
There were 272 false alarms and 1,321 correctly classified retained customers.
In total, 577 of 2,000 customers were flagged. At this threshold, about
47.14% of alerts were false positives. No customer-retention intervention
or financial uplift was measured.

The test metrics are higher than the selected CV averages, but they come
from a single split. This is not evidence of general improvement over
cross-validation. Model settings and the threshold were not revised using
these results. Earlier full-dataset EDA remains an evaluation limitation.

The model is saved as a complete preprocessing/classifier pipeline. CSV
scoring is available through `scripts/predict.py`. Tableau is deferred.
