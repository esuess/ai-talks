library(a11yviz)
library(dplyr)
library(purrr)

# 1. Point this to the exact directory path where your rendered HTML syllabi live
syllabus_folder <- "~/Documents/University_Courses/Syllabi_HTML/"

# 2. Gather every compiled HTML file inside that target folder
html_files <- list.files(
  path = syllabus_folder, 
  pattern = "\\.html$", 
  full.names = TRUE, 
  recursive = FALSE # Set to TRUE if you have nested sub-folders
)

# 3. Create a safe verification wrapper function
audit_single_syllabus <- function(file_path) {
  message("Auditing: ", basename(file_path))
  
  tryCatch({
    # Run the core a11yviz document-level parser
    audit_results <- a11y_audit_doc(file_path)
    
    # Standardize the data frame output and map it to the file name
    if (nrow(audit_results) > 0) {
      audit_results %>%
        mutate(
          file_name = basename(file_path),
          full_path = file_path
        ) %>%
        select(file_name, status, criterion, description, everything())
    } else {
      # Return a clean row if the document passes perfectly
      data.frame(
        file_name = basename(file_path),
        status = "PASS",
        criterion = "All Clear",
        description = "No structural WCAG compliance violations detected.",
        stringsAsFactors = FALSE
      )
    }
  }, error = function(e) {
    # Fail-safe catch for empty or corrupted HTML files
    data.frame(
      file_name = basename(file_path),
      status = "ERROR",
      criterion = "File Read Fail",
      description = paste("Could not successfully parse HTML file:", e$message),
      stringsAsFactors = FALSE
    )
  })
}

# 4. Map the audit function across all files and bind into a single dataset
master_compliance_report <- map_df(html_files, audit_single_syllabus)

# 5. Filter for actionable compliance failures (skips perfect passes)
actionable_violations <- master_compliance_report %>%
  filter(status %in% c("FAIL", "WARNING", "ERROR"))

# 6. Save the results as a CSV spreadsheet for remediation tracking
write.csv(
  actionable_violations, 
  file = file.path(syllabus_folder, "ada_compliance_remediation_log.csv"), 
  row.names = FALSE
)

# 7. Print a quick diagnostic console summary
cat("\n--- BATCH AUDIT COMPLETE ---\n")
cat("Total Files Audited : ", length(html_files), "\n")
cat("Total Actionable Hits: ", nrow(actionable_violations), "\n")
cat("Log exported to: ada_compliance_remediation_log.csv\n")
