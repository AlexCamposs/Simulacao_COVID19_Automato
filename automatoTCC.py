import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# Carregar o shapefile
gdf = gpd.read_file("MOH_PHU_BOUNDARY_7600122142074799332\MOH_PHU_BOUNDARY.shp")

# Dicionário de população real
populacao_real = {
    "York Region Public Health": 1173334,
    "Huron Perth Health Unit": 142931,
    "Region of Waterloo, Public Health": 587165,
    "Southwestern Public Health": 216533, #Oxford Elgin St. Thomas Health Unit
    "Hamilton Public Health Services": 569353,
    "Thunder Bay District Health Unit": 152885,
    "Peel Public Health": 1451022,
    "Lambton Public Health": 128154,
    "Wellington-Dufferin-Guelph Health Unit": 307283,
    "Brant County Health Unit": 144937,
    "Middlesex-London Health Unit": 500563,
    "Sudbury and District Health Unit": 202431,
    "Haliburton, Kawartha, Pine Ridge District Health Unit": 189183,
    "Niagara Region Public Health Department": 477941,
    "Chatham-Kent Health Unit": 104316,
    "Kingston, Frontenac and Lennox and Addington Health Unit": 206962,
    "Windsor-Essex County Health Unit": 422860,
    "Peterborough Public Health": 147681,
    "Grey Bruce Health Unit": 174301,
    "Eastern Ontario Health Unit": 210276,
    "North Bay Parry Sound District Health Unit": 129362,
    "Ottawa Public Health": 1017449,
    "Leeds, Grenville and Lanark District Health Unit": 179830,
    "Northwestern Health Unit": 77338,
    "Haldimand-Norfolk Health Unit": 116706,
    "Timiskaming Health Unit": 32394,
    "Renfrew County and District Health Unit": 107522,
    "Toronto Public Health": 2794356,
    "Halton Region Health Department": 596637,
    "Hastings and Prince Edward Counties Health Unit": 171450,
    "Simcoe Muskoka District Health Unit": 599843,
    "Durham Region Health Department": 696992,
    "Porcupine Health Unit": 81188,
    "Algoma Public Health Unit": 112764
}

# Identificar vizinhos e calcular correlações entre regiões
def shared_border_length(region1, region2):
    intersection = region1.geometry.intersection(region2.geometry)
    return intersection.length

def correlation_weight(region1, region2):
    perimeter1 = region1.geometry.length
    perimeter2 = region2.geometry.length
    shared_length = shared_border_length(region1, region2)
    weight1 = shared_length / perimeter1
    weight2 = shared_length / perimeter2
    return (weight1 + weight2) / 2

# Identificar vizinhos
neighbors = {}
for idx, region in gdf.iterrows():
    neighbors[idx] = gdf[gdf.geometry.touches(region.geometry)].index.tolist()

# Criar dicionário de regiões
region_data = {}

for idx, region in gdf.iterrows():
    region_name = region['NAME_ENG']
    population = populacao_real.get(region_name)
    region_data[region_name] = {
        "neighbors": [],
        "population": population,
        "S": population,
        "E": 0,
        "I": 0,
        "R": 0,
        "D": 0,
        "restricted": False
    }

# #começa pandemia em Toronto, Otawwa e Windsor Essex
region_data["Toronto Public Health"]["S"]-=1
region_data["Toronto Public Health"]["I"]+=1
region_data["Ottawa Public Health"]["S"]-=1
region_data["Ottawa Public Health"]["I"]+=1
region_data["Windsor-Essex County Health Unit"]["S"]-=1
region_data["Windsor-Essex County Health Unit"]["I"]+=1


# Calcular os pesos de correlação
for region_id, neighbors_list in neighbors.items():
    region_name = gdf.loc[region_id, 'NAME_ENG']
    for neighbor_id in neighbors_list:
        neighbor_name = gdf.loc[neighbor_id, 'NAME_ENG']
        region1 = gdf.loc[region_id]
        region2 = gdf.loc[neighbor_id]
        weight = correlation_weight(region1, region2)
        region_data[region_name]["neighbors"].append((neighbor_name, weight))
        region_data[neighbor_name]["neighbors"].append((region_name, weight))

# Parâmetros do modelo Windsor
beta = 0.20  # Taxa de transmissão
sigma = 1/5.4 # Taxa de progressão de E para I (incubação)
gamma = 1/10 # Taxa de recuperaçãoS
delta = 0.02 # Taxa de mortalidade
restriction_threshold = 0.0008 #%população para começar restrição de movimento
hysteresis_threshold = 0.00009 #%população para acabar restrição de movimento
fator_reducao = 0.20 # redução de contaminação se estiver com restrição de movimento


# Função para atualizar as regiões
def update_regions(day):
    new_states = {}
    for region in region_data:
        S, E, I, R, D = region_data[region]["S"], region_data[region]["E"], region_data[region]["I"], region_data[region]["R"], region_data[region]["D"]
        pop = region_data[region]["population"]

        # Verificar se a região entra/sai de restrição
        if I / pop >= restriction_threshold:
            region_data[region]["restricted"] = True
        elif I / pop < hysteresis_threshold:
            region_data[region]["restricted"] = False

        new_exposed = beta * S * I / pop
        
        for neighbor, correlation in region_data[region]["neighbors"]:
            new_exposed += correlation * beta * S * region_data[neighbor]["I"] / region_data[neighbor]["population"]

        if region_data[region]["restricted"] == True:
            new_exposed *= fator_reducao

        new_I = sigma * E
        new_R = gamma * I
        new_D = delta * I
        
        new_states[region] = {
            "S": S - new_exposed,
            "E": E + new_exposed - new_I,
            "I": I + new_I - new_R - new_D,
            "R": R + new_R,
            "D": D + new_D
        }
    
    for region in region_data:
        region_data[region].update(new_states[region])

# Simulação
num_days = 274 # dias simulados
time_series = {region: {key: [] for key in ["S", "E", "I", "R", "D"]} for region in region_data}
for day in range(num_days):
    update_regions(day)
    for region in region_data:
        for key in ["S", "E", "I", "R", "D"]:
            time_series[region][key].append(region_data[region][key])

# # Visualização dos resultados
# plt.figure(figsize=(12, 6))
# for region in region_data:
#     plt.plot(time_series[region]["I"], label=f"Infectados - {region}")
# plt.xlabel("Dias")
# plt.ylabel("Número de Infectados")
# plt.legend()
# plt.title("Propagação de Doença nas Regiões Reais")
# plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
# plt.subplots_adjust(right=0.56)
# plt.show()

# Carregar os dados reais de COVID-19
real_data = pd.read_csv("conposcovidloc.csv", parse_dates=["Case_Reported_Date"])

# Filtrar para o intervalo de datas
real_data_filtered = real_data[(real_data["Case_Reported_Date"] >= "2020-01-01") & 
                               (real_data["Case_Reported_Date"] <= "2020-10-01")]

# Filtrar apenas uma PHU
phu_data_filtered = real_data_filtered[real_data_filtered["Reporting_PHU"] == "Windsor-Essex County Health Unit"]

# Contar casos diários por data
daily_cases_phu = phu_data_filtered.groupby("Case_Reported_Date").size()

# Preencher os dias ausentes com 0 casos
daily_cases_phu = daily_cases_phu.reindex(pd.date_range(start="2020-01-01", end="2020-10-01", freq='D'), fill_value=0)

# Calcular os casos ativos (considerando 10 dias de infecção)
active_cases_phu = daily_cases_phu.rolling(window=10, min_periods=1).sum()

# Calcular os dias desde o início (para alinhar com os dados simulados)
active_cases_phu_days = (active_cases_phu.index - active_cases_phu.index.min()).days

# Plotando os casos reais ativos de PHU
plt.figure(figsize=(10, 3))  # formato mais largo e achatado
plt.plot(active_cases_phu_days, active_cases_phu, label="Casos Reais", color="tab:blue")

# Plotando os casos simulados ativos de PHU
plt.plot(time_series["Windsor-Essex County Health Unit"]["I"], label="Casos Simulados", color="tab:orange")

# Ajustes de eixos
plt.xlim(0, max(active_cases_phu_days))
plt.ylim(0, 400)
plt.margins(x=0, y=0)  # remove margens automáticas
plt.xlabel("Dias")
plt.ylabel("Número de Infectados")
plt.legend(loc="upper right", frameon=True)
plt.tight_layout()

# Salvar na pasta resultados
plt.savefig("resultados/windsor.png", dpi=300)
plt.close()
