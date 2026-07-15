################################################################################
#                                  PRELIMINARIES                               #
# Load the packages you need at the top of the screen                          #
# The raw_variables vector is here to make your life easier later              #
################################################################################
raw_variables <- c("id",
                   "program.type", "age", "ethnicity.r", "faculty", "stats", "stats.history", 
                   "self.efficacy", "asi", "asi.social", "asi.cog", "asi.phys","perf.cog", 
                   "stat.anx.ah","stat.anx.tc","stat.anx.fst","math.anx", "stat.anx.ws")

rename_variables <- function (dataset) {
    cleaned_name_dataset <- dataset |>
        rename(
            anxiety_global = asi,
            anxiety_social = asi_social,
            anxiety_cognitive = asi_cog,
            anxiety_physical = asi_phys,

            cognitive_perfectionism = perf_cog,

            stat_anxiety_help = stat_anx_ah,
            stat_anxiety_test = stat_anx_tc,
            stat_anxiety_teacher_fear = stat_anx_fst,

            math_anxiety = math_anx,

            statistics_worthiness = stat_anx_ws
        )
    
    return(cleaned_name_dataset)
}

################################################################################
#                                  PREPARE DATA                                #
################################################################################



