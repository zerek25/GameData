# coding:utf-8
import os
from datetime import datetime
import xlwings as xw

# 创建无工作簿不显示的新excel文件
app = xw.App(visible=False, add_book=False)

COLORS = {
    "grey": "#DBDCDF",
    "white": "#F0F0F0",
    "genshin": {
        "primary": "#3E4556",
        "text": "#DEC492",
    },
    "starrail": {
        "primary": "#201D1D",
        "text": "#E7C681",
    }
}


# 使用xlwings生成excel文件
def generate_excel(data, file_name, path, color_type="genshin"):
    # 判断目录是否存在，不存在则生成目录
    if not os.path.exists(path):
        os.makedirs(path)
    # 新建文件
    wb = app.books.add()
    for sheet_data in data:
        # 表格范围
        col_num = len(sheet_data["list"][0])
        row_num = len(sheet_data["list"])
        # 新建数据表
        ws = wb.sheets.add(sheet_data["sheet_name"])
        # 写入数据
        # 表头
        ws.range((1, 1), (1, col_num)).merge()
        ws.range((1, 1)).value = sheet_data.get("title", "表格图片")
        ws.range((2, 1), (2, col_num)).merge()
        ws.range((2, 1)).value = sheet_data.get("subtitle", "By 烂柯Lankei")
        # 数据
        ws.range((3, 1)).value = sheet_data["list"]
        # 表尾
        ws.range((row_num + 3, 1), (row_num + 3, col_num)).merge()
        ws.range((row_num + 3, 1)).value = "生成于  " + datetime.now().strftime("%Y-%m-%d %H:%M")
        ws.range((row_num + 4, 1), (row_num + 4, col_num)).merge()
        ws.range((row_num + 4, 1)).value = sheet_data.get("version", "米游社: 烂柯Lankei")

        # 区分各部分
        table = ws.used_range
        title = table.rows(1)
        subtitle = table.rows(2)
        header = table.rows(3)
        time = table.rows(-1)
        version = table.rows(0)

        # 设置表样式
        # 整体设置
        # 设置列宽
        column_widths = get_column_widths(sheet_data["list"], 2)
        for col in range(len(table.columns)):
            width = column_widths[col - 1]
            table.columns(col).column_width = width

        # 设置间隔色
        for row in range(len(table.rows)):
            if row % 2 == 0:
                table.rows(row).color = COLORS["white"]
            else:
                table.rows(row).color = COLORS["grey"]

        # 设置边框
        border_line = 1
        border_color = 2
        table.api.Borders(8).LineStyle = border_line
        table.api.Borders(8).ColorIndex = border_color
        table.api.Borders(9).LineStyle = border_line
        table.api.Borders(9).ColorIndex = border_color
        table.api.Borders(7).LineStyle = border_line
        table.api.Borders(7).ColorIndex = border_color
        table.api.Borders(10).LineStyle = border_line
        table.api.Borders(10).ColorIndex = border_color
        table.api.Borders(12).LineStyle = border_line
        table.api.Borders(12).ColorIndex = border_color
        table.api.Borders(11).LineStyle = border_line
        table.api.Borders(11).ColorIndex = border_color

        # 设置全局单元格样式
        table.font.size = 12
        header.font.name = "微软雅黑"
        table.api.WrapText = True
        table.api.HorizontalAlignment = -4108
        table.api.VerticalAlignment = -4108
        table.autofit()

        # 设置标题样式
        title.font.size = 24
        title.font.name = "楷体"
        title.color = COLORS[color_type]["primary"]
        title.font.color = COLORS[color_type]["text"]
        title.api.WrapText = False
        title.font.bold = True
        title.api.HorizontalAlignment = -4108

        # 设置副标题样式
        subtitle.font.size = 10
        subtitle.font.name = "楷体"
        subtitle.color = COLORS[color_type]["primary"]
        subtitle.font.color = COLORS[color_type]["text"]
        subtitle.api.WrapText = False
        subtitle.font.bold = False
        subtitle.api.HorizontalAlignment = -4108

        # 设置表头样式
        header.font.size = 12
        header.font.name = "微软雅黑"
        header.color = COLORS[color_type]["primary"]
        header.font.color = COLORS[color_type]["text"]
        header.api.WrapText = False
        header.font.bold = True
        header.api.HorizontalAlignment = -4108

        # 设置时间样式
        time.font.size = 10
        time.font.name = "楷体"
        time.color = COLORS[color_type]["primary"]
        time.font.color = COLORS[color_type]["text"]
        time.api.WrapText = False
        time.font.bold = False
        time.api.HorizontalAlignment = -4108

        # 设置版本信息样式
        version.font.size = 10
        version.font.name = "楷体"
        version.color = COLORS[color_type]["primary"]
        version.font.color = COLORS[color_type]["text"]
        version.api.WrapText = False
        version.font.bold = False
        version.api.HorizontalAlignment = -4108

    # 删除默认工作簿
    wb.sheets["sheet1"].delete()

    # 保存excel文件
    wb.save(path + "/" + file_name + ".xlsx")
    wb.close()


# 使用xlwings生成表格图片
def generate_image(data, path, color_type="genshin"):
    # 检测路径是否存在
    if not os.path.exists(path):
        os.mkdir(path)
    # 新建数据表
    wb = app.books.add()

    for sheet_data in data:
        # 表格范围
        col_num = len(sheet_data["list"][0])
        row_num = len(sheet_data["list"])
        # 新建数据表
        ws = wb.sheets.add(sheet_data["sheet_name"])
        # 写入数据
        # 表头
        ws.range((1, 1), (1, col_num)).merge()
        ws.range((1, 1)).value = sheet_data.get("title", "表格图片")
        ws.range((2, 1), (2, col_num)).merge()
        ws.range((2, 1)).value = sheet_data.get("subtitle", "By 烂柯Lankei")
        # 数据
        ws.range((3, 1)).value = sheet_data["list"]
        # 表尾
        ws.range((row_num + 3, 1), (row_num + 3, col_num)).merge()
        ws.range((row_num + 3, 1)).value = "生成于 " + datetime.now().strftime("%Y-%m-%d")
        ws.range((row_num + 4, 1), (row_num + 4, col_num)).merge()
        ws.range((row_num + 4, 1)).value = sheet_data.get("version", "米游社: 烂柯Lankei")

        # 区分各部分
        table = ws.used_range
        title = table.rows(1)
        subtitle = table.rows(2)
        header = table.rows(3)
        time = table.rows(-1)
        version = table.rows(0)

        # 设置表样式
        # 整体设置
        # 设置列宽
        column_widths = get_column_widths(sheet_data["list"], 2)
        for col in range(len(table.columns)):
            width = column_widths[col - 1]
            table.columns(col).column_width = width

        # 设置间隔色
        for row in range(len(table.rows)):
            if row % 2 == 0:
                table.rows(row).color = COLORS["white"]
            else:
                table.rows(row).color = COLORS["grey"]

        # 设置边框
        border_line = 1
        border_color = 2
        table.api.Borders(8).LineStyle = border_line
        table.api.Borders(8).ColorIndex = border_color
        table.api.Borders(9).LineStyle = border_line
        table.api.Borders(9).ColorIndex = border_color
        table.api.Borders(7).LineStyle = border_line
        table.api.Borders(7).ColorIndex = border_color
        table.api.Borders(10).LineStyle = border_line
        table.api.Borders(10).ColorIndex = border_color
        table.api.Borders(12).LineStyle = border_line
        table.api.Borders(12).ColorIndex = border_color
        table.api.Borders(11).LineStyle = border_line
        table.api.Borders(11).ColorIndex = border_color

        # 设置全局单元格样式
        table.font.size = 24
        table.font.name = "霞鹜文楷"
        table.api.WrapText = True
        table.api.HorizontalAlignment = -4108
        table.api.VerticalAlignment = -4108
        table.autofit()

        # 设置标题样式
        title.font.size = 48
        title.font.name = "钉钉进步体"
        title.color = COLORS[color_type]["primary"]
        title.font.color = COLORS[color_type]["text"]
        title.api.WrapText = False
        title.font.bold = True
        title.api.HorizontalAlignment = -4108

        # 设置副标题样式
        subtitle.font.size = 20
        subtitle.font.name = "钉钉进步体"
        subtitle.color = COLORS[color_type]["primary"]
        subtitle.font.color = COLORS[color_type]["text"]
        subtitle.api.WrapText = False
        subtitle.font.bold = False
        subtitle.api.HorizontalAlignment = -4108

        # 设置表头样式
        header.font.size = 24
        header.font.name = "霞鹜文楷等宽"
        header.color = COLORS[color_type]["primary"]
        header.font.color = COLORS[color_type]["text"]
        header.api.WrapText = False
        header.font.bold = True
        header.api.HorizontalAlignment = -4108

        # 设置时间样式
        time.font.size = 20
        time.font.name = "钉钉进步体"
        time.color = COLORS[color_type]["primary"]
        time.font.color = COLORS[color_type]["text"]
        time.api.WrapText = False
        time.font.bold = False
        time.api.HorizontalAlignment = -4108

        # 设置版本信息样式
        version.font.size = 20
        version.font.name = "钉钉进步体"
        version.color = COLORS[color_type]["primary"]
        version.font.color = COLORS[color_type]["text"]
        version.api.WrapText = False
        version.font.bold = False
        version.api.HorizontalAlignment = -4108

        # 导出图片
        file_path = os.path.join(path, "{}.png".format(sheet_data["sheet_name"]))
        ws.used_range.to_png(file_path)
        # 添加水印


# 计算列宽
def get_column_widths(value, times=1):
    data_sets = []
    column_widths = []
    row_num = len(value)
    column_num = len(value[0])

    for i in range(column_num):
        data_sets.append([])
        for j in range(row_num):
            if value[j][i]:
                data_sets[i].append(len(str(value[j][i])))

    for data_set in data_sets:
        if len(data_set) == 0:
            width = 8
        else:
            width = int(sum(data_set) / len(data_set) / 5) * 8 + 8
        width = 40 if width > 40 else width
        width = width * times
        column_widths.append(width)
    return column_widths
