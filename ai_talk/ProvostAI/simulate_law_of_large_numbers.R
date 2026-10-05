# Load necessary libraries
library(tidyverse)

# Define constants
N_TRIALS <- 1000
N_SIMULATIONS <- 5

# Function to simulate the law of large numbers
simulate_lln <- function(seed) {
  set.seed(seed)
  tibble(
    trial = 1:N_TRIALS,
    mean = map_dbl(1:N_TRIALS, ~ mean(rnorm(.x)))
  )
}

# Simulate the law of large numbers multiple times
simulations <- map(1:N_SIMULATIONS, simulate_lln) %>%
  bind_rows(.id = "simulation_id")

# Plot the simulations
simulations %>%
  ggplot(aes(x = trial, y = mean, color = simulation_id)) +
  geom_line() +
  geom_hline(yintercept = 0, color = "red") +
  labs(
    title = "Law of Large Numbers Simulations",
    subtitle = "Mean of random normals vs. number of trials",
    x = "Number of Trials",
    y = "Mean"
  )

ggsave("lln_simulations.png", width = 7, height = 7)