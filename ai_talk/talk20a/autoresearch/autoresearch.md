# OpenCode /autoresearch Loop Configuration Guide (R Tidymodels Stack)

This document outlines the complete setup for running an autonomous model optimization loop using **R Tidymodels** and the **`stacks` package** for the Titanic dataset inside **OpenCode**.

---

## 📋 Directory Structure

Ensure your project folder is organized as follows before launching the loop:

```text
titanic-autoresearch/
├── .autoresearch/
│   └── program.md
├── data/
│   ├── train.csv
│   └── test.csv
├── eval/
│   └── eval.sh
└── train.R
```

---

## 🛠️ Code Implementations

### 1. The Mutable Target Script (`train.R`)
This is the file OpenCode will autonomously modify, benchmark, and optimize.

```R
# train.R
library(tidymodels)
library(stacks)
library(readr)

# 1. Load Data
train_raw <- read_csv("data/train.csv") %>%
  mutate(Survived = factor(Survived, levels = c(0, 1), labels = c("No", "Yes")))

test_raw <- read_csv("data/test.csv") %>%
  mutate(Survived = factor(Survived, levels = c(0, 1), labels = c("No", "Yes")))

# 2. Setup Resamples (CRITICAL: Must save predictions and workflow for stacking)
set.seed(123)
titanic_folds <- vfold_cv(train_raw, v = 5, strata = Survived)

ctrl_stack <- control_stack_grid()

# 3. Base Recipe (OpenCode can modify or add feature engineering here)
titanic_recipe <- recipe(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare, data = train_raw) %>%
  step_impute_mean(all_numeric_predictors()) %>%
  step_impute_mode(all_nominal_predictors()) %>%
  step_dummy(all_nominal_predictors()) %>%
  step_zv(all_predictors())

# ==================== CANDIDATE MODELS ====================
# OpenCode can add, modify, or swap out these candidates and grids

# Candidate A: Random Forest
rf_spec <- rand_forest(mtry = tune(), min_n = tune(), trees = 500) %>%
  set_engine("ranger") %>% set_mode("classification")

rf_wf <- workflow() %>% add_recipe(titanic_recipe) %>% add_model(rf_spec)
rf_res <- tune_grid(rf_wf, resamples = titanic_folds, grid = 4, control = ctrl_stack)

# Candidate B: XGBoost
xgb_spec <- boost_tree(mtry = tune(), trees = tune(), learn_rate = tune()) %>%
  set_engine("xgboost") %>% set_mode("classification")

xgb_wf <- workflow() %>% add_recipe(titanic_recipe) %>% add_model(xgb_spec)
xgb_res <- tune_grid(xgb_wf, resamples = titanic_folds, grid = 4, control = ctrl_stack)

# Candidate C: Regularized Logistic Regression (GLMNET)
lr_spec <- logistic_reg(penalty = tune(), mixture = tune()) %>%
  set_engine("glmnet") %>% set_mode("classification")

lr_wf <- workflow() %>% add_recipe(titanic_recipe) %>% add_model(lr_spec)
lr_res <- tune_grid(lr_wf, resamples = titanic_folds, grid = 4, control = ctrl_stack)
# ==========================================================

# 4. Initialize and Blend the Model Stack
model_stack <- 
  stacks() %>%
  add_candidates(rf_res) %>%
  add_candidates(xgb_res) %>%
  add_candidates(lr_res) %>%
  blend_predictions(penalty = 10^seq(-3, -0.5, length = 20))

# 5. Fit the Finalized Stack on the entire training data
final_stack <- fit_members(model_stack)

# 6. Final Evaluation Step (Predict on the holdout test set)
test_predictions <- predict(final_stack, new_data = test_raw) %>%
  bind_cols(test_raw)

# Calculate final unseen accuracy
final_metrics <- accuracy(test_predictions, truth = Survived, estimate = .pred_class)
final_accuracy <- final_metrics$.estimate

# Write out the strict stacked evaluation score for the bash runner
writeLines(as.character(final_accuracy), "eval/accuracy.txt")
```

### 2. The Scoring Harness (`eval/eval.sh`)
```bash
#!/bin/bash
# Run the mutable R script
Rscript train.R

# Extract and output the accuracy score
cat eval/accuracy.txt
```

### 3. Loop Instructions (`.autoresearch/program.md`)
```markdown
# Program Instructions: Titanic Model Optimization via Stacking

## Objective
Maximize the strict evaluation accuracy score outputted by `eval/eval.sh`.

## Scope for OpenCode Modification
1. You may modify the preprocessing steps in `titanic_recipe` (ensure `step_dummy` and `step_zv` remain, as XGBoost and Glmnet require numeric inputs without zero variance).
2. You can tweak the model definitions (`rf_spec`, `xgb_spec`, `lr_spec`), their parameters, or change the tuning grid sizing (e.g., increasing `grid = 4` to a higher number to try more model variants).
3. You can introduce a 4th candidate workflow model if you wish (such as a Support Vector Machine or K-Nearest Neighbor).

## Rules
- Do not alter the configuration of `ctrl_stack`. Stacking *requires* `control_stack_grid()`.
- Do not alter the final scoring pipeline that generates `eval/accuracy.txt`.
```

---

## 🚀 Execution Steps

1. **Install Dependencies:**
   ```R
   install.packages(c("stacks", "ranger", "xgboost", "glmnet", "tidymodels", "readr"))
   ```
2. **Commit Baseline:**
   ```bash
   git add . && git commit -m "initial ensemble stack baseline"
   ```
3. **Fire Off Loop:** Open `opencode` and execute:
   ```text
   /autoresearch Maximize the validation accuracy in train.R. Optimize the preprocessing recipe, tune grid densities, or refine the candidate specs within the tidymodels stacks framework. Ensure no syntax errors are introduced.
   ```