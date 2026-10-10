# Conversation History: Setting Up an `/autoresearch` Loop with R Tidymodels in OpenCode

## 1. Initial Architecture & Framework Setup

### Question
How to set up an `/autoresearch` loop to run R Tidymodels to fit models for the Titanic data in OpenCode.

### Strategy Overview
To run an `/autoresearch` loop using **R Tidymodels** to fit models on the **Titanic dataset** inside **OpenCode**, you leverage the popular "Karpathy Loop" port designed for terminal-based coding agents. The core mechanic relies on a three-file structure: a static dataset, a strict validation script (`eval.sh`), and a single R script that OpenCode will autonomously modify, benchmark, and keep or revert based on model accuracy.

### Baseline Implementation Steps

#### Step 1: Install the Autoresearch Skill in OpenCode
Ensure you have the universal `autoresearch` skill added to your global or local OpenCode configuration. Run the following in your terminal:
```bash
git clone https://github.com/uditgoenka/autoresearch.git
cd autoresearch
./scripts/install.sh --opencode --global
```

#### Step 2: Structure Your Project Directory
Create a clean directory and initialize a git repository (autoresearch requires git to handle automatic rollbacks of failing configurations):
```bash
mkdir titanic-autoresearch && cd titanic-autoresearch
git init
mkdir -p data eval
```
Place your `train.csv` and `test.csv` Titanic data inside the `data/` folder.

#### Step 3: Create the Mutable Target Script (`train.R`)
This is the **only file** OpenCode will be allowed to modify. Write a baseline script using `tidymodels` that trains a model, saves it, and writes the accuracy to a text file.
```R
# train.R
library(tidymodels)
library(readr)

# 1. Load Data
titanic_data <- read_csv("data/train.csv") %>%
  mutate(Survived = factor(Survived, levels = c(0, 1), labels = c("No", "Yes")))

# 2. Split Data
set.seed(123)
data_split <- initial_split(titanic_data, prop = 0.80, strata = Survived)
train_data <- training(data_split)
test_data  <- testing(data_split)

# 3. Recipes & Preprocessing (OpenCode will try to iterate on this)
titanic_recipe <- recipe(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare, data = train_data) %>%
  step_impute_mean(all_numeric_predictors()) %>%
  step_impute_mode(all_nominal_predictors()) %>%
  step_dummy(all_nominal_predictors())

# 4. Model Specification (OpenCode can change specs, engines, or tuning parameters)
model_spec <- logistic_reg() %>%
  set_engine("glm") %>%
  set_mode("classification")

# 5. Workflow & Fit
titanic_wflow <- workflow() %>%
  add_recipe(titanic_recipe) %>%
  add_model(model_spec)

fitted_model <- fit(titanic_wflow, data = train_data)

# 6. Evaluate and Save Scalar Metric
predictions <- predict(fitted_model, new_data = test_data) %>%
  bind_cols(test_data)

accuracy_metric <- accuracy(predictions, truth = Survived, estimate = .pred_class)
final_accuracy <- accuracy_metric$.estimate

# Write accuracy out for the bash test runner
writeLines(as.character(final_accuracy), "eval/accuracy.txt")
```
Commit this initial version to git so OpenCode has a baseline: `git add . && git commit -m "baseline setup"`

#### Step 4: Create the Scoring Harness (`eval/eval.sh`)
The autoresearch loop needs an executable script that returns a single numeric value representing performance. Create `eval/eval.sh`:
```bash
#!/bin/bash
# Run the mutable R script
Rscript train.R

# Extract and output the accuracy score
cat eval/accuracy.txt
```
Make it executable: `chmod +x eval/eval.sh`

#### Step 5: Configure the Autoresearch Program Instructions
Create a `.autoresearch/program.md` file to tell OpenCode what its constraints are, what libraries to use, and how to maximize the metric:
```markdown
# Program Instructions: Titanic Model Optimization

## Objective
Maximize the classification accuracy score outputted by `eval/eval.sh`.

## Rules & Scope
1. You may only modify `train.R`. Do not edit anything in the `data/` or `eval/` directories.
2. Use the R `tidymodels` framework.
3. You can explore:
   - Feature engineering steps in `titanic_recipe` (e.g., interaction terms, step_ns, step_YeoJohnson).
   - Swapping out `logistic_reg()` for alternative `parsnip` models like `rand_forest()`, `boost_tree()`, or `decision_tree()`.
   - Modifying hyperparameter configurations.
4. Do not remove the `set.seed(123)` boundary ensuring evaluation consistency.
5. Do not stop or ask questions. Keep running iterations autonomously until maximum runtime or iterations are exhausted.
```

#### Step 6: Launch the Loop in OpenCode
Now, start your OpenCode session inside this directory and trigger the command directly from the interface:
```bash
opencode
```
Once inside OpenCode, pass your target goal using the `/autoresearch` slash command:
```text
/autoresearch maximize the validation accuracy in train.R using Tidymodels recipes and alternative parsnip engines
```

---

## 2. Integrating V-Fold Cross-Validation

### Follow-Up Request
Add cross-validation.

### Updated Strategy
To prevent OpenCode from overfitting to your holdout set during its autonomous iterations, you can implement **V-fold cross-validation** directly within `train.R`. Instead of evaluating on a single test split, the script will pass the average cross-validated accuracy to OpenCode's evaluation harness.

### Updated `train.R` with Cross-Validation
```R
# train.R
library(tidymodels)
library(readr)

# 1. Load Data
titanic_data <- read_csv("data/train.csv") %>%
  mutate(Survived = factor(Survived, levels = c(0, 1), labels = c("No", "Yes")))

# 2. Set Seed and Create Resamples (Keep resamples constant so OpenCode evaluations are stable)
set.seed(123)
titanic_folds <- vfold_cv(titanic_data, v = 5, strata = Survived)

# 3. Recipes & Preprocessing (OpenCode will try to iterate on this)
titanic_recipe <- recipe(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare, data = titanic_data) %>%
  step_impute_mean(all_numeric_predictors()) %>%
  step_impute_mode(all_nominal_predictors()) %>%
  step_dummy(all_nominal_predictors())

# 4. Model Specification (OpenCode can change specs, engines, or tuning parameters)
model_spec <- logistic_reg() %>%
  set_engine("glm") %>%
  set_mode("classification")

# 5. Workflow Configuration
titanic_wflow <- workflow() %>%
  add_recipe(titanic_recipe) %>%
  add_model(model_spec)

# 6. Fit Resamples (Cross-Validation Loop)
cv_results <- fit_resamples(
  titanic_wflow,
  resamples = titanic_folds,
  metrics = metric_set(accuracy),
  control = control_resamples(save_pred = FALSE)
)

# 7. Collect and Save Average CV Metric
cv_metrics <- collect_metrics(cv_results)
mean_accuracy <- cv_metrics %>%
  filter(.metric == "accuracy") %>%
  pull(mean)

# Write out the mean score for the bash test runner
writeLines(as.character(mean_accuracy), "eval/accuracy.txt")
```

---

## 3. Hyperparameter Grid Tuning & Final Evaluation Holdout

### Follow-Up Request
Add hyperparameter tuning and a final evaluation step on a separate `test.csv`.

### Updated Strategy
To implement both features seamlessly, we restructure `train.R` so that OpenCode can autonomously find optimal hyperparameter values via grid tuning while calculating the final score using a strict train/test split. By tracking **cross-validated performance** to select the best hyperparameter configuration and then scoring it on a **hidden holdout test set**, you completely protect your loop from data leakage.

### Directory Configuration
```bash
data/train.csv  # Used for Cross-Validation and Hyperparameter Tuning
data/test.csv   # Used ONLY for the Final Evaluation Step
```

### Unified Hyperparameter Tuning and Final Evaluation `train.R`
```R
# train.R
library(tidymodels)
library(readr)

# 1. Load Data
train_raw <- read_csv("data/train.csv") %>%
  mutate(Survived = factor(Survived, levels = c(0, 1), labels = c("No", "Yes")))

test_raw <- read_csv("data/test.csv") %>%
  mutate(Survived = factor(Survived, levels = c(0, 1), labels = c("No", "Yes")))

# 2. Set Seed and Setup CV Folds for Hyperparameter Search
set.seed(123)
titanic_folds <- vfold_cv(train_raw, v = 5, strata = Survived)

# 3. Recipes & Preprocessing (OpenCode can iterate on these steps)
titanic_recipe <- recipe(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare, data = train_raw) %>%
  step_impute_mean(all_numeric_predictors()) %>%
  step_impute_mode(all_nominal_predictors()) %>%
  step_dummy(all_nominal_predictors())

# 4. Model Specification with Tuneable Hyperparameters
model_spec <- rand_forest(
  mtry = tune(),
  trees = tune(),
  min_n = tune()
) %>%
  set_engine("ranger") %>%
  set_mode("classification")

# 5. Workflow Configuration
titanic_wflow <- workflow() %>%
  add_recipe(titanic_recipe) %>%
  add_model(model_spec)

# 6. Tune Hyperparameters across the CV Folds
set.seed(123)
tune_results <- tune_grid(
  titanic_wflow,
  resamples = titanic_folds,
  grid = 5,
  metrics = metric_set(accuracy)
)

# 7. Select Best Model Based on CV Performance
best_params <- select_best(tune_results, metric = "accuracy")
final_wflow <- finalize_workflow(titanic_wflow, best_params)

# 8. Final Evaluation Step (Train on entire train.csv, evaluate on test.csv)
final_fit <- fit(final_wflow, data = train_raw)

test_predictions <- predict(final_fit, new_data = test_raw) %>%
  bind_cols(test_raw)

# Calculate final unseen accuracy
final_metrics <- accuracy(test_predictions, truth = Survived, estimate = .pred_class)
final_accuracy <- final_metrics$.estimate

# Write out the strict final test evaluation score for the bash runner
writeLines(as.character(final_accuracy), "eval/accuracy.txt")
```

---

## 4. Supported Modeling Engines Specification

### Follow-Up Request
Incorporate different supported classification engines into the search space configuration.

### Strategy Details
To give OpenCode clear boundaries on which modeling engines to explore, update the `.autoresearch/program.md` file to tell the agent exactly which packages are installed and how to specify alternative model backends in Tidymodels.

### Engine Inventory Reference
* **`ranger` (Random Forest):** Fast, handles missing numeric values natively if configured, and excels at tabular data.
* **`xgboost` (Boosted Trees):** Highly accurate, but requires all predictors to be numeric (`step_dummy`).
* **`rpart` (Decision Tree):** A simple baseline tree for rapid iterations.
* **`glm` (Logistic Regression):** The standard linear baseline.
* **`glmnet` (LASSO / Ridge / Elastic Net):** Penalizes irrelevant variables or high interaction layers.
* **`kknn` (K-Nearest Neighbors):** Distance-based relationships after numeric scaling.

---

## 5. Integrating Ensemble Stacking

### Follow-Up Request
Use a stacked model ensemble.

### Strategy Overview
To have OpenCode autonomously build and optimize a **Stacked Ensemble** (combining predictions from multiple model types like Random Forests, XGBoost, and Logistic Regression), integrate the `stacks` package into your `train.R` file. This approach automates the process of training diverse candidate models, saving their out-of-fold predictions, and blending them using a regularized meta-model.

### Stacking Environment Initialization
```R
install.packages(c("stacks", "ranger", "xgboost", "glmnet"))
```

### Full Ensemble Stacking `train.R` Script
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

# 3. Base Recipe
titanic_recipe <- recipe(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare, data = train_raw) %>%
  step_impute_mean(all_numeric_predictors()) %>%
  step_impute_mode(all_nominal_predictors()) %>%
  step_dummy(all_nominal_predictors()) %>%
  step_zv(all_predictors())

# ==================== CANDIDATE MODELS ====================
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

### Stacked Optimization `.autoresearch/program.md` Configuration
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

## 6. Execution & Monitoring of the Loop

### Follow-Up Request
Fire off the optimization loop execution.

### Deployment Instructions

#### Step 1: Open OpenCode in Your Terminal
Ensure you are inside your working directory (`titanic-autoresearch`) and load the environment:
```bash
opencode
```

#### Step 2: Initialize Your Baseline Score
Run your test runner script manually once to verify everything compiles error-free and establish your starting score:
```bash
./eval/eval.sh
```

#### Step 3: Launch the Autoresearch Command
Execute the slash command inside the OpenCode console interface:
```text
/autoresearch Maximize the validation accuracy in train.R. Optimize the preprocessing recipe, tune grid densities, or refine the candidate specs within the tidymodels stacks framework. Ensure no syntax errors are introduced.
```

### Monitoring the Process
* **`autoresearch-results.tsv`:** OpenCode generates this tabular record in your workspace root directory. Follow this file to trace metrics over time, along with corresponding script alterations.
* **Git Log Tracing:** Open `git log --oneline` in a parallel shell to monitor automated commits triggered every time the agent unlocks a higher ensemble score.
* **Error Log Reversion:** If an experimental branch throws an error or fails execution, the runner logs the runtime error trace and fires an automated `git reset --hard` to rollback the script to its most recent working state.