from Functional.mappHar import analyst, get_scenario_fromDB, scenario_code

print("start analyst")
print("======================================")
analyst.main()
print("======================================")
print("end analyst")
print("======================================")
print("start write code")
print("======================================")
file = open("perf.py", "w", encoding='utf-8')

file_code = scenario_code.base_code()

scenarioList = get_scenario_fromDB.get_scenario_name()
for i in scenarioList:
    print(i["name_scenario"])
    scenarioDetail = get_scenario_fromDB.get_scenario_detail(i["name_scenario"])
    tmp_code = scenario_code.scenario_code(scenarioDetail)
    file_code = file_code + tmp_code

file.write(file_code)
file.close()
print("======================================")
print("end write code")
print("======================================")
