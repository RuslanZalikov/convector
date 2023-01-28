import json

class LabelStudio:
    def __init__(self, dictData: dict):
        self.dictData = dictData
        self.Size = {"width" : self.dictData["annotations"][0]["result"][0]["original_width"],
                     "height" : self.dictData["annotations"][0]["result"][0]["original_height"]}
        self.dictID = {value["id"]: dict() for value in self.dictData["annotations"][0]["result"]}
        for value in self.dictData["annotations"][0]["result"]:
            temp_value = value.get("value")
            if value.get("type") == "labels":
                self.dictID[value.get("id")]["labels"] = temp_value.get("labels")[0]
            if value.get("type") == "textarea":
                self.dictID[value.get("id")]["text"] = temp_value.get("text")[0]
            if value.get("type") == "rectangle":
                self.dictID[value.get("id")]["coord"] = dict()
                self.dictID[value.get("id")]["coord"]["x"] = temp_value.get("x")
                self.dictID[value.get("id")]["coord"]["y"] = temp_value.get("y")
                self.dictID[value.get("id")]["coord"]["width"] = temp_value.get("width")
                self.dictID[value.get("id")]["coord"]["height"] = temp_value.get("height")
                self.dictID[value.get("id")]["coord"]["rotation"] = temp_value.get("rotation")

    def print_info(self, choice="LabelStudio"):
        if choice == "LabelStudio":
            print(self.dictID)
        if choice == "Donut":
            self.parse_to_donut()
            print(self.dictResult)
    def parse_to_donut(self):
        self.dictResult = dict()

        self.dictResult["gt_parse"] = dict()
        self.dictResult["meta"] = dict()
        self.dictResult["valid_line"] = []
        self.dictResult["roi"] = dict()
        self.dictResult["repeating_symbol"] = []
        self.dictResult["dontcare"] = []


    #meta
        self.dictResult["meta"]["version"] = None
        self.dictResult["meta"]["split"] = None
        self.dictResult["meta"]["image_id"] = None
        self.dictResult["meta"]["image_size"] = dict()
        self.dictResult["meta"]["image_size"]["width"] = self.Size["width"]
        self.dictResult["meta"]["image_size"]["height"] = self.Size["height"]


    #gt_parse
        for value in self.dictID.keys():
            self.dictResult["gt_parse"][self.dictID.get(value).get("labels")] = self.dictID.get(value).get("text")


    #valid_line
        count = 0
        for value in self.dictID.keys():
            count += 1
            self.dictResult["valid_line"].append({
                "words": [],
                "category": self.dictID.get(value).get("labels"),
                "group_id": count,
                "sub_group_id": None
            })
            self.dictResult["valid_line"][count-1]["words"].append({
                # "quad": dict(),
                "is_key": None,
                "row_id": count,
                "text": self.dictID.get(value).get("text")
            })
            temp_field = field(self.dictID.get(value).get("coord").get("x"), self.dictID.get(value).get("coord").get("y"), self.dictID.get(value).get("coord").get("width"), self.dictID.get(value).get("coord").get("height"))
            self.dictResult["valid_line"][count-1]["words"][0]["quad"] = {
                "x1": temp_field.x1,    "y1": temp_field.y1,
                "x2": temp_field.x2,    "y2": temp_field.y2,
                "x3": temp_field.x3,    "y3": temp_field.y3,
                "x4": temp_field.x4,    "y4": temp_field.y4
            }


class Donut:
    def __init__(self, DataDonutField: set):
        self.Data = dict()
        self.Data["gt_parse"] = None
        self.Data["meta"] = None
        self.Data["valid_line"] = []



class field:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y
        self.x3 = x + w
        self.y3 = y + h
        self.x4 = x
        self.y4 = y + h
