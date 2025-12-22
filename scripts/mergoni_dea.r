library(tidyverse)
library(janitor)
library(rcDEA)
library(readxl)
library(writexl)

df <- read_xlsx("output\\18_dea_master.xlsx")

reference_df <- df %>%
  filter(jaar_afgestudeerd_so == "2022-2023") %>%
  filter(leerlingen_laatste_jaar_aso > 0) %>%
  mutate(aso = `uren-leraar_laatste_jaar_aso` / leerlingen_laatste_jaar_aso) %>%
  filter(leerlingen_laatste_jaar_aso>0)

dea_df <- reference_df %>%
  select(-unit_code_so, -jaar_afgestudeerd_so, -schoolbestuur, -net, -leerlingengroepen)

dea_input <- dea_df %>%
  select(aso)

dea_output <- dea_df %>%
  select(studierendement) %>%
  mutate(studierendement = coalesce(studierendement, 0))

dea_exo <- dea_df %>%
  select(gemiddelde_oki)

c_DEA <- conditional_DEA(input = dea_input, output = dea_output,
                         exogenous = dea_exo,
m = 402, B = 50,
alpha = TRUE,
RTS = "crs", ORIENTATION = "in")

results <- reference_df %>%
  select(unit_code_so, `uren-leraar_laatste_jaar_aso`, leerlingen_laatste_jaar_aso, aso, studierendement) %>%
  mutate(dea = c_DEA$eff)

write_xlsx(results, "output\\r_mergoni_results.xlsx")
