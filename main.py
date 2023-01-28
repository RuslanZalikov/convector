import json

import function as fn

def run():
    with open("test.json") as f:
        js = json.load(f)
    obj = fn.LabelStudio(js)
    obj.print_info(choice="LabelStudio")
    obj_donut = obj.parse_to_donut()
    obj.print_info(choice="Donut")

run()