# Load all support package
library('tibble')
library('readxl')
library('tidyr')
library('dplyr')
library('ggplot2')

#======================================================================
#---------------------------plotting-----------------------------------
# Carbon emission plot
#Carbon emission data
data <- read_excel("data.xls",sheet = 1, skip = 0)
data <- mutate(data,Carbon_emission = as.numeric(data$Carbon_emission))
carbon_plot <- ggplot(data = as_tibble(data),aes(x=year, y=Carbon_emission, fill = scenario)) +
  geom_bar(stat = 'identity', width=0.5, position=position_dodge(0.6)) + 
  ylim(min(as.numeric(data$Carbon_emission),0)*1.1,max(as.numeric(data$Carbon_emission))*1.1) +
  labs(title = "Carbon_emission(mil CO2)", y = "") +
  theme(plot.title = element_text(hjust = 0.5)) 

fig_name <- paste("Carbon_emission.png",sep="")
ggsave(fig_name, dpi=800, plot = carbon_plot,width = 9.0, height = 6.55)

# Industry energy use plot
# Industry energy use data
data_indenguse <- read_excel("data.xls",sheet = 2, skip = 0)
data_indenguse <- mutate(data_indenguse, energy_use = as.numeric(data_indenguse$energy_use))

# Type 1
indenguse_plot <- ggplot(data = as_tibble(data_indenguse),aes(x=year, y= energy_use, fill = sector)) +
  geom_bar(stat = 'identity',color = 'white') + 
  facet_wrap(~scenario,nrow=1) +
  ylim(0,80) +
  labs(title = "Industry Energy use (EJ)", y = "") +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(axis.text.x=element_text(angle = 90))

fig_name <- paste("Industry energy use.png",sep="")
ggsave(fig_name, dpi=800, plot = indenguse_plot, width = 16.0, height = 6.55)

# Type 2
indenguse_plot_2 <- ggplot(data = as_tibble(data_indenguse),aes(x=scenario, y= energy_use, fill = sector)) +
  geom_bar(stat = 'identity',color = 'white') + 
  facet_wrap(~year,nrow=1) +
  ylim(0,80) +
  labs(title = "Industry Energy use (EJ)", y = "") +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(axis.text.x=element_text(angle = 90))

fig_name <- paste("Industry energy use_2.png",sep="")
ggsave(fig_name, dpi=800, plot = indenguse_plot_2, width = 16.0, height = 6.55)
