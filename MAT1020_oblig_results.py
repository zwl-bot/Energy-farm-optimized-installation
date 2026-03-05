import MAT1020_oblig_functions as mof
import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt


## Opprette tabeller 
wind_file = "kapasitetsfaktorer_vind_onshore_daily_2014-20.csv"
wind_table, wind_location_list = mof.createTableCSV(wind_file)

############################# OPPGAVE 1 ###################################


## 1 a)
#mof.plotLocations(wind_table, wind_location_list, "Vind", [0,200])
mof.plotEachLocation(wind_table, wind_location_list, "Vind")



## 1 b) - gjennomsnitt kapasitetsfaktor for hver lokasjon
wind_table_list = mof.makeTableList(wind_table)
wind_avg_list = mof.findAverage(wind_table_list) # forventet kapasitetsfaktor liste

print("Gjennomsnittlig kapasitetsfaktor for hver lokasjon"); print()
print(f"{'LOKASJON':<25}", " | ", "GJENNOMSNITT KAPASITETSFAKTOR")
for location, wind_avg in zip(wind_location_list, wind_avg_list):
    print(f"{location:<25}", " | ", wind_avg)
print("\n\n")




## 1 c) - Varians og standardavvik for kapasitetsfaktorene i hver lokasjon'
wind_var_list, wind_sd_list = mof.findVarianceStandardDeviation(wind_table_list, wind_avg_list)

print("Varians og standardavvik for hver lokasjon"); print()
print(f"{'LOKASJON':<25}", " | ", f"{'VARIANS':<20}", " | ", f"{'STANDARDAVVIK':<20}")
for location, wind_var, wind_sd in zip(wind_location_list, wind_var_list, wind_sd_list):
    print(f"{location:<25}", " | ", f"{wind_var:<20}", " | ", wind_sd)
print("\n\n")




## 1 d) - Kovariansen til kapasitetsfaktorene
wind_cov = mof.createCovarianceMatrix(wind_table_list, wind_avg_list, wind_var_list) # kovariansmatrisen
wind_cor = mof.createCorrelationMatrix(wind_cov, wind_sd_list) # korrelasjonsmatrise

# printer kovarians og korrelasjon mellom alle 2 ulike lokasjoner
d = len(wind_table_list)
print(f"{'LOKASJON 1':<20}", "|", f"{'LOKASJON 2':<20}", "|", f"{'KOVARIANS':<22}", 
      "|", f"{'KORRELASJON':<10}")
for row in range(d-1):
    for col in range(row+1, d):
        print(f"{wind_location_list[row]:<20}", "|", f"{wind_location_list[col]:<20}", 
              "|", f"{wind_cov[row, col]:<22}", "|", f"{wind_cor[row, col]:<10}")
print("\n\n")


############################# OPPGAVE 2 ###################################

## 2 a) Gjennomsnittlig timesforbruk av strom i Norge
nettoforbruk_file = "norge_nettoforbruk_2000_2023.csv"
nettoforbruk_table = mof.createTableCSV_Norway(nettoforbruk_file)
avg_forbruk_hour = mof.findAverageEnergyUsage(nettoforbruk_table) # Forventet ettersporsel

print(f"Gjennomsnittlig timesforbruk av strom (GWh) i Norge, periode {nettoforbruk_table[0][0]} - {nettoforbruk_table[-1][0]}") 
print("Gjennomsnittlig timesforbruk:", avg_forbruk_hour, "GWh"); print("\n\n")



## 2 b) Installert kapasitet i hver av de 4 lokasjonene
mu_E = 0.05 * avg_forbruk_hour # 5% av Norges forventet ettersporsel (GWh)

#w_ = mof.findOptimalInstalledCapacity(mu_E, wind_cov, wind_avg_list); print(w_)

# w_star: den optimalserte installert kapasitet for hver lokasjon
w_star = mof.findOptimalInstalledCapacityFinal(mu_E, wind_cov, wind_avg_list, wind_location_list)

print(f"Installert kapasitet for alle lokasjoner, med forventet ettersporsel over 1 h (MWh): {mu_E*1000}\n")
print(f"{'LOKASJON':<20}", "|", f"{'INSTALLERT KAPASITET (MWh)':<26}")
for i in range(len(wind_location_list)):
    print(f"{wind_location_list[i]:<20}", "|", f"{w_star[i]*1000:<26}")
print("\n\n")



## 2 c) d) Finn forventet produksjon og standardavvik for alle lokasjoner for 1 h 
wind_prod = w_star @ wind_avg_list.T # totalproduksjon for alle lokasjoner
wind_prod_var = w_star @ wind_cov @ w_star.T # variansen til totalproduksjonen
wind_prod_sd = np.sqrt(wind_prod_var) # standardavviket til totalproduksjonen

print("Forventet totalproduksjon over 1 h for alle lokasjoner (MWh):", 
      round(wind_prod*1000, 3))
print("Standardavvik til totalproduksjon over 1 h for alle lokasjoner (MWh):", 
      round(wind_prod_sd*1000, 3)); print("\n\n")





############################# OPPGAVE 3 ###################################

capacity_each_location_lst, capacity_diff_lst, smallest_location_index = mof.minimizeDemand(mu_E, wind_sd_list, wind_avg_list)


# forventet totalproduksjon for hver lokasjon
exp_prod_lst = capacity_each_location_lst * wind_avg_list 

# standardavvik (produksjon) for hver lokasjon
sd_prod_lst = capacity_each_location_lst * wind_sd_list

print("Installert kapasitet, forventet produksjon og standardavvik for hver lokasjon separat")
print(f"{'LOKASJON':<20}", "|", f"{'INSTALLERT KAPASITET (MWh)':<26}", "|", 
      f"{'FORVENTET PRODUKSJON (MWh)':<26}", "|", f"{'STANDARDAVVIK (MWh)'}")
for i in range(len(capacity_each_location_lst)):
    print(f"{wind_location_list[i]:<20}", "|", f"{capacity_each_location_lst[i]*1000:<26}", 
          "|", f"{exp_prod_lst[i]*1000:<26}", "|", f"{sd_prod_lst[i]*1000}")
print("\n")

# Enkelt lokasjon med naermest tilnaerming til ettersporsel
print("Lokasjon nærmest etterspørselen:", wind_location_list[smallest_location_index])







