import json
import readJSON
from readJSON import test_list, python_data, all_IDs, member_type_list
print(test_list)
load_classes = {
    "0":"Snow",
    "1":"Wind",
    "2":"Seismic",
    "3":"Roof Live",
    "4":"Floor Live",
    "5": "Dead"}


"""class Load():
    def __init__(self, StartTrib, EndTrib, StartLoc, EndLoc, Comments, IsFullLength, Loads):
        self.StartTrib = get_start_Trib

def get_all_loads(python_data):
    print(python_data)"""


all_loads = []
for i in range(len(member_type_list)):
    if member_type_list[i] == "Beam":
        direction = "HorizontalY"
    if member_type_list[i] == "Column":
        direction = "VerticalZ"
    jump_to_load_defs = python_data[i+1][f"{direction}AxisLoadData"]["LoadGroups"]["0"]["LoadDefs"]
    load_dict = {}
    load_dict["OnMember"] = f"m{i+1}"
    load_dict["Loads"] = []
    for j in range(len(jump_to_load_defs)):
        load_dict["Loads"].append({})
        load_dict["Loads"][j]["LoadID"] = j+1
        load_dict["Loads"][j]["Comments"] = jump_to_load_defs[j]["Comments"]
        load_dict["Loads"][j]["StartTrib_W"] = jump_to_load_defs[j]["StartTribWidth"]
        load_dict["Loads"][j]["EndTrib_W"] = jump_to_load_defs[j]["EndTribWidth"]
        load_dict["Loads"][j]["StartLoc"] = round(jump_to_load_defs[j]["StartLocation"]/12,2)
        load_dict["Loads"][j]["EndLoc"] = round(jump_to_load_defs[j]["EndLocation"]/12,2)
        load_dict["Loads"][j]["IsFullLength"] = jump_to_load_defs[j]["IsFullLength"]
        load_dict["Loads"][j]["LoadsByClass"] = {}
        #Deduce Load Type
        load_dict["Loads"][j]["Units"] = "(PSF)"
        multiplier = 144 #(PSI to PSF)
        #WIll have to decypher this later. Problem is it defaults to 12 inches trib. Will have to experiment with "Load Type" key
        #if load_dict["Loads"][j]["StartTrib_W"] == load_dict["Loads"][j]["EndTrib_W"] and load_dict["Loads"][j]["EndTrib_W"] == 12:
            #load_dict["Loads"][j]["Units"] = "(plf)"
            #multiplier = 12
        if load_dict["Loads"][j]["StartLoc"] == load_dict["Loads"][j]["EndLoc"]:
            load_dict["Loads"][j]["Units"] = "(#)"
            multiplier = 1 #(No Change)
        
        for k in range(len(load_classes)):
            if jump_to_load_defs[j]['Loads'][f'{k}']['StartMagnitude'] != 0 and jump_to_load_defs[j]['Loads'][f'{k}']['EndMagnitude'] != 0:
                load_dict["Loads"][j]["LoadsByClass"][f'{k}'] = {}
                load_dict["Loads"][j]["LoadsByClass"][f'{k}']["StartMag"] = round(jump_to_load_defs[j]['Loads'][f'{k}']['StartMagnitude']*multiplier,2)
                load_dict["Loads"][j]["LoadsByClass"][f'{k}']["EndMag"] = round(jump_to_load_defs[j]["Loads"][f'{k}']["EndMagnitude"]*multiplier,2)
    all_loads.append(load_dict)
print(all_loads)    

with open("loadsData.json","w") as f:
    json_str = json.dumps(all_loads)
    f.write(json_str)