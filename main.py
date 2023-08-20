# coding:utf-8
import wx
from starrail import process as srp
from starrail import database as srdb

from genshin import database as gidb


class GameData(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"成就数据提取", pos=wx.DefaultPosition,
                          size=wx.Size(800, 450), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.init_ui()
        self.Centre(wx.BOTH)

    def init_ui(self):
        panel = wx.Panel(self)

        gs = wx.GridSizer(2, 2, 5, 5)

        title_font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        bs_gi = wx.BoxSizer(wx.VERTICAL)

        gi_title = wx.StaticText(panel, -1, u"原神")
        gi_title.SetFont(title_font)
        bs_gi.Add(gi_title)

        gi_generate_image = wx.Button(panel, -1, "生成全成就图片")
        gi_generate_image.Bind(wx.EVT_BUTTON, self.export_gi_achievement_image)
        bs_gi.Add(gi_generate_image)

        gi_generate_excel = wx.Button(panel, -1, "生成全成就Excel")
        gi_generate_excel.Bind(wx.EVT_BUTTON, self.export_gi_achievement_excel)
        bs_gi.Add(gi_generate_excel)

        gs.Add(bs_gi)

        bs_sr = wx.BoxSizer(wx.VERTICAL)

        sr_title = wx.StaticText(panel, -1, u"崩坏：星穹铁道")
        sr_title.SetFont(title_font)
        bs_sr.Add(sr_title)

        sr_cloud_file = wx.Button(panel, -1, "开拓等级")
        sr_cloud_file.Bind(wx.EVT_BUTTON, self.export_sr_player_level_json)
        bs_sr.Add(sr_cloud_file)

        sr_daily_reward = wx.Button(panel, -1, "每日实训")
        sr_daily_reward.Bind(wx.EVT_BUTTON, self.export_sr_daily_reward_json)
        bs_sr.Add(sr_daily_reward)

        sr_message_contact = wx.Button(panel, -1, "个性签名")
        sr_message_contact.Bind(wx.EVT_BUTTON, self.export_sr_message_contact_json)
        bs_sr.Add(sr_message_contact)

        sr_generate_excel = wx.Button(panel, -1, "生成全成就Excel")
        sr_generate_excel.Bind(wx.EVT_BUTTON, self.export_sr_achievement_excel)
        bs_sr.Add(sr_generate_excel)

        sr_generate_image = wx.Button(panel, -1, "生成全成就图片")
        sr_generate_image.Bind(wx.EVT_BUTTON, self.export_sr_achievement_image)
        bs_sr.Add(sr_generate_image)

        sr_cloud_file = wx.Button(panel, -1, "UniCloud文件")
        sr_cloud_file.Bind(wx.EVT_BUTTON, self.export_sr_unicloud_json)
        bs_sr.Add(sr_cloud_file)

        gs.Add(bs_sr)

        panel.SetSizer(gs)

    @staticmethod
    def export_gi_achievement_image(e):
        gidb.export_achievement_image()
        print("全成就图片已生成")

    @staticmethod
    def export_gi_achievement_excel(e):
        gidb.export_achievement_excel()
        print("全成就Excel已生成")

    @staticmethod
    def export_sr_player_level_json(e):
        srp.process_player_level()

    @staticmethod
    def export_sr_daily_reward_json(e):
        srp.process_daily_reward()

    @staticmethod
    def export_sr_message_contact_json(e):
        srp.process_message_contact()

    @staticmethod
    def export_sr_achievement_excel(e):
        srdb.export_achievement_excel()
        print("全成就Excel已生成")

    @staticmethod
    def export_sr_achievement_image(e):
        srdb.export_achievement_image()
        print("全成就图片已生成")

    @staticmethod
    def export_sr_unicloud_json(e):
        srdb.export_unicloud_file()


def main():
    app = wx.App()
    gd = GameData(None)
    gd.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
