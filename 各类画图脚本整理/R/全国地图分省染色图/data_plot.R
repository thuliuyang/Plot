# Load all support package
library('tibble')
library('readxl')
library('tidyr')
library('dplyr')
library('tidyverse')
library('maptools')
library('mapdata')
library('ggplot2')
library('mapproj')
library("ggthemes")
library("rgdal")
options(stringsAsFactors=FALSE,warn=FALSE,encoding="UTF-8")
# ============================================================================
# read shapefile
china_map = readOGR('C:/Users/liuyang/Desktop/画图/shapefile/gadm36_CHN_1.shp')
china_map1 <-china_map@data
china_map1 <- data.frame(china_map1,id=seq(0:30)-1) 
china_map2 <- fortify(china_map)

#======================================================================
#---------------------------plotting-----------------------------------

## plot map
# read data
data_ironpro <- as_tibble(read_excel("data.xls",sheet = 1, skip = 1))

# Merge data and shapefile
china_map1 %>%
  left_join(data_ironpro,by = c('NAME_1' = 'NAME')) ->
  data_ironpro_map

newmapdata<-merge(china_map2[,c(-4,-5)],data_ironpro_map[,c("id","NAME_1","sum")],by="id")

map_plot <- ggplot()+
  geom_polygon(data=newmapdata,aes(x=long,y=lat,group=group,fill=sum),col="grey95")+
  scale_fill_gradient(low="white",high="steelblue") +
  coord_map("polyconic") +
  theme_map()

fig_name <- paste("iron and steel by province_map_2050.png",sep="")
ggsave(fig_name, dpi=400, plot = map_plot,width = 10.0, height = 8.55)
