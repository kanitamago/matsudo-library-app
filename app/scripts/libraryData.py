import openpyxl

wb = openpyxl.load_workbook('app/datafile/matsudo.xlsx')

#sheet is 図書館
library = wb["図書館"]

#列名
#(None, '名称', '郵便番号', '住所', '電話番号', '緯度', '経度')
columns = ["ID", "名称", "郵便番号", "住所", "電話番号", "緯度", "経度"]

#整形データ
results = []

for row in list(library.values)[1:]:
    info = {}
    for col, val in zip(columns, row):
        info[col] = val
    results.append(info)

def get_library_position(library_data):
    latitudes = []
    longitudes = []
    names = []
    for library in library_data:
        latitude = library["緯度"]
        longitude = library["経度"]
        name = library["名称"]
        latitudes.append(latitude)
        longitudes.append(longitude)
        names.append(name)
    return zip(latitudes, longitudes, names)

def get_library_names():
    global results
    names = []
    for library in results:
        name = library["名称"]
        names.append(name)
    return names
