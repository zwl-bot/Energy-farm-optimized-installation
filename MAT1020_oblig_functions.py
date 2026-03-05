import numpy as np
from numpy.linalg import inv
import csv
import matplotlib.pyplot as plt


########## Oppgave 1 ##########

## Simplier way to read the .csv-file
def createTableCSV(filename):
    with open(filename, "r") as f: 
        table = list(csv.reader(f, delimiter=','))
    
    location_list = table[0][1:] # list of corresponding locations
    
    # convert 2nd column and so on into float values
    cols = len(table[0]); rows = len(table)
    table_new = [table[l][1:cols] for l in range(1, rows)]
    for i in range(rows-1):
        for j in range(cols-1):
            table_new[i][j] = float(table_new[i][j]) # turn str to float values
    
    table_new = np.array(table_new) # convert to array format for simplicity
    return table_new, location_list


## Represent values from each column as one set of values
def makeTableList(table):
    table_list = [[]]*(len(table[0])) # convert table by slicing each column
    for i in range(len(table_list)):
        table_list[i] = table[:, i:i+1]
    table_list = np.array(table_list) 
    return table_list


## Plot capacity factor for all locations in one plot
def plotLocations(table_new, location_list, title_name, span=None):
    table_list = [[]]*(len(table_new[0])) # convert table by slicing each column
    days = np.arange(1, len(table_new)+1) # x-axis
    
    for i in range(len(table_list)):
        table_list[i] = table_new[:, i:i+1]
    
    table_list = np.array(table_list)
    
    if span == None:
        for j in range(len(table_list)):
            plt.plot(days, table_list[j], label=f"{location_list[j]}")
        plt.xlabel("Dager")
        plt.ylabel("Kapasitetsfaktorer")
        plt.legend(); plt.title(title_name); plt.show()    
    else:
        for j in range(len(table_list)):
            plt.plot(days[span[0]:span[1]], table_list[j][span[0]:span[1]], label=f"{location_list[j]}")
        plt.xlabel("Dager")
        plt.ylabel("Kapasitetsfaktorer")
        plt.legend(); plt.title(title_name); plt.show()
    return



## Plot capacity factor for each location separately
def plotEachLocation(table_list, location_list, title_name, span=None):
    days = np.arange(1, len(table_list)+1) # x-axis
    table_new = makeTableList(table_list)
    
    if span == None:
        ind = 0
        for table in table_new:
            plt.plot(days, table, label = f"{location_list[ind]}")
            plt.xlabel("Dager"); plt.ylabel("Kapasitetsfaktorer")
            plt.legend(); plt.title(title_name); plt.show()
            ind += 1
    else:
        ind = 0
        for table in table_new:
            plt.plot(days[span[0]:span[1]], table[span[0]:span[1]], label = f"{location_list[ind]}")
            plt.xlabel("Dager"); plt.ylabel("Kapasitetsfaktorer")
            plt.legend(); plt.title(title_name); plt.show()
            ind += 1
    return


## Find mean value of each set in table_list
def findAverage(table_list):
    n = len(table_list[0])
    average_list = np.zeros(len(table_list))    
    for i in range(len(table_list)):
        average_list[i] = np.sum(table_list[i])
    average_list = average_list/n
    return average_list


## Find variance and standard deviation of each set in table_list
def findVarianceStandardDeviation(table_list, average_list):
    n = len(table_list[0]); var_list = []
    for tab, avg in zip(table_list, average_list):
        curr_var_table = (tab - avg)**2 # can do this due to numpy array structure
        curr_var = np.sum(curr_var_table) / n # variance for current location
        var_list.append(curr_var)
    
    var_list = np.array(var_list) # list of variance for each corresponding location
    sd_list = np.sqrt(var_list) # list of standard deviation for each corresponding location
    
    return var_list, sd_list


## Find covariance between location k and l (here its 0-indexing)
def covariance(table_list, avg_list, k, l):
    r_k, r_l = avg_list[k], avg_list[l]; n = len(table_list[0])
    c = 0
    for i in range(n):
        c += (table_list[k][i] - r_k)*(table_list[l][i] - r_l)
    return c/n


## Fnd the covariance matrix
def createCovarianceMatrix(table_list, avg_list, var_list):
    d = len(avg_list); C = np.zeros(shape=(d,d))
	
    for i in range(d): # fill diagonals of C first
        C[i, i] = var_list[i]

    # fill in the rest of C (by upper triangular and symmetry)
    for row in range(d-1):
        for col in range(row+1, d):
            curr_cov = covariance(table_list, avg_list, row, col)
            C[row, col] = curr_cov; C[col, row] = curr_cov
    return C


## Find correlation between location k and l (here its 0-indexing)
def correlation(C, sd_list, k, l):
    sd_k, sd_l = sd_list[k], sd_list[l]; return C[k,l] / (sd_k * sd_l)


## Find the correlation matrix
def createCorrelationMatrix(C, sd_list):
    d = len(sd_list); R = np.ones(shape=(d,d))
	
	# fill in the rest of R (by upper triangluar and symmetry)
    for row in range(d-1):
        for col in range(row+1, d):
            curr_cor = correlation(C, sd_list, row, col)
            R[row, col] = curr_cor; R[col, row] = curr_cor
    return R




########## Oppgave 2 ##########

## Create table based on netto energy usage in Norway
def createTableCSV_Norway(filename):
    with open(filename, "r") as f:
        table = list(csv.reader(f, delimiter=','))
    
    # convert 2nd column and so on into float values
    cols = len(table[0]); rows = len(table)
    table_new = [table[l][:cols] for l in range(1, rows)] # ignore first row of table
    for i in range(len(table_new)):
        for j in range(cols):
            table_new[i][j] = int(table_new[i][j]) # turn str to int values
    
    table_new = np.array(table_new) # convert to array format for simplicity
    return table_new



## Find average energy usage per hour based on data
def findAverageEnergyUsage(table):
    total_days = 0; total_energy = 0
    for curr_stats in table:
        if curr_stats[0] % 4 == 0: # leap year
            total_days += 366
        else: 
            total_days += 365
        total_energy += curr_stats[1] # GWh
    total_hours = total_days*24
    avg_energy_hour = round(total_energy/total_hours, 4)
    return avg_energy_hour



## Find optimal installment of capacity for all locations
def findOptimalInstalledCapacity(mu_E, C, r_hat):
    rT = np.array([r_hat]); r = rT.T; rrT = r@rT
    cr = C + rrT; cr_inv = inv(cr)
    return mu_E*(cr_inv@r)


## Return smallest value and it's corresponding index
def findMin(lst):
    smallest = lst[0]; smallest_index = 0
    for i in range(1, len(lst)):
        if lst[i] < smallest:
            smallest = lst[i]; smallest_index = i
    return smallest, smallest_index


## Remove row nr and column nr, and return the new 2D-array
def removeRowCol(C, row_index, col_index):
    """
    Parameters
    ----------
    C : array (2D-array, dxd-matrise)
        Kovariansmatrisen for alle lokasjoner
    row_index : int
        Rad nr (0-indeksering)
    col_index : int
        Kolonne nr (0-indeksering)

    Returns
    -------
    new_C : array (2D-array, dxd-matrise)
        Ny kovariansmatrisen for de resterende lokasjonene
    """
    new_C = np.delete(C, row_index, axis=0); new_C = np.delete(new_C, col_index, axis=1) 
    return new_C



## Find the final optimal installment of capacity for all locations
def findOptimalInstalledCapacityFinal(mu_E, C, r_hat, locations):
    """
    Parameters
    ----------
    mu_E : float/int
        Forventet ettersporsel av strom per time
    C : array (2D-array, dxd-matrise)
        Kovariansmatrisen for alle lokasjoner
    r_hat : array
        Array av forventet kapasitetsfaktor i hver lokasjon
    locations : list
        Liste med navn paa alle lokasjoner

    Returns
    -------
    w_star : array
        Liste over installert kapasitet i hver korresponderende lokasjon
    """
    w_star = np.zeros(len(locations))
    
    this_locations = locations[:] # make copy of locations (list)
    this_r_hat = r_hat.copy() # make copy of r_hat (array)
    this_C = C.copy() # make copy of C (2D-array)
    
    curr_w = findOptimalInstalledCapacity(mu_E, C, r_hat)
    
    while True: 
        if len(this_locations) == 0:
            break
        
        curr_r, curr_r_index = findMin(curr_w)
        if curr_r < 0:
            this_locations.pop(curr_r_index)
            this_r_hat = np.delete(this_r_hat, curr_r_index)
            this_C = removeRowCol(this_C, curr_r_index, curr_r_index)
            curr_w = findOptimalInstalledCapacity(mu_E, this_C, this_r_hat)
        else: 
            for w, l in zip(curr_w, this_locations): 
                curr_index = locations.index(l)
                w_star[curr_index] = w
            break
    return w_star


########## Oppgave 3 ##########

## For each location, find its optimal installed capacity
def findOptimalInstalledCapacity1D(mu_E, sd_k, r_k):
    """
    Parameters
    ----------
    mu_E : float
        Forventet ettersporsel
    sd_k : float
        Standardavvik til kapasitetsfaktor i lokasjon k
    r_k : float
        Forventet kapasitetsfaktor i lokasjon k

    Returns
    -------
    w : float
        Installert kapasitet i lokasjon k
    """
    w = mu_E * r_k / (sd_k**2 + r_k**2)
    return w



## for each location, find the smallest difference to the demand
def minimizeDemand(mu_E, sd_list, r_list):
    """
    Parameters
    ----------
    mu_E : float
        Forventet ettersporsel
    sd_list : array
        Liste over standardavvik til kapasitetsfaktor i hver lokasjon
    r_list : array
        Liste over forventet kapasitetsfaktor i hver lokasjon

    Returns
    -------
    w_list : array
        Installert kapasitet for hver lokasjon uten aa ta hensyn til andre lokasjoner
    w_diff : array
        Differansen mellom installert kapasitet og ettersporsel i hver lokasjon
    w_min_index : int
        Indeks nr paa lokasjonen med minst avvik til ettersporsel (0-indeksering)
    """
    w_list = np.zeros(len(sd_list))
    
    for k in range(len(sd_list)):
        w_list[k] = findOptimalInstalledCapacity1D(mu_E, sd_list[k], r_list[k])
    #print(w_list)
    w_diff = abs(w_list - mu_E)
    
    w_min = w_diff[0]; w_min_index = 0
    for i in range(1, len(sd_list)):
        if w_diff[i] < w_min:
            w_min = w_diff[i]; w_min_index = i
    
    return w_list, w_diff, w_min_index

