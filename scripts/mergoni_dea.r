library(tidyverse)
library(janitor)
library(rcDEA)
library(readxl)
library(writexl)

args <- commandArgs(trailingOnly = TRUE)
dea_file = args[1]
input = args[2]
output = args[3]
conditioneel = args[4]
col_name = args[5]

df <- read_xlsx(dea_file)

dea_df <- df %>%
  select(-unit_code_so, -jaar_afgestudeerd_so, -schoolbestuur, -net, -leerlingengroepen)

dea_input <- dea_df %>%
  select(all_of(input))

dea_output <- dea_df %>%
  select(all_of(output))

dea_exo <- dea_df %>%
  select(all_of(conditioneel))

c_DEA <- conditional_DEA(input = dea_input, output = dea_output,
                         exogenous = dea_exo,
m = 402, B = 50,
alpha = TRUE,
RTS = "crs", ORIENTATION = "in")

results <- df %>%
  select(unit_code_so) %>%
  mutate(!!col_name := c_DEA$eff)

df_updated <- df %>%
  left_join(results, by = "unit_code_so")

write_xlsx(df_updated, dea_file)
