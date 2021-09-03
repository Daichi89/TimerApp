from time import strftime
import re

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path


class StopWatchLayout(BoxLayout):
    """""
    Root Widget
    """""
    


class StopWatch(BoxLayout):
    def __init__(self, **kwargs):
        super(StopWatch, self).__init__(**kwargs)
        self.watch_prop = ObjectProperty(None)              # Display Time
        self.button_lay_prop = ObjectProperty(None)
        self.reset_prop= ObjectProperty(None)
        self.start_prop = ObjectProperty(None)
        self.ll_prop = ObjectProperty(None)
        self.lt_prop = ObjectProperty(None)
        self.lap_prop = ObjectProperty(None)
        self.time_prop = ObjectProperty(None)
        self.stop_watch = False
        self.total_past = 0.0
        self.font_ratio = 0  # 初期状態での texture_size.y に対する font_size の比率
        self.texture_ratio = 0  # 初期状態での texture_size.y に対する texture_size.x の比率
        self.buffer = None
        self.on_size_call = False
        self.stop_watch_pat = re.compile(r'(?:\[size=\d+\])?(?P<size>\d+)(?:\[/size\])?')
        self.onstart()

    def onstart(self):
        Clock.schedule_interval(self.update, 0)
        
    def update(self, nap):
        if self.stop_watch:
            self.total_past += nap
            minutes, seconds = divmod(self.total_past, 60)
            micro_size = int(self.watch_prop.font_size * 0.7)
            self.watch_prop.text = f"{int(minutes):02}:{int(seconds):02}.[size={micro_size}]{int(seconds * 100 % 100):02}[/size]"
            self.buffer = f"{int(minutes):02}:{int(seconds):02}.{int(seconds * 100 % 100):02}"
 
    def cb_start(self):
        self.start_prop.text = 'Start' if self.stop_watch else 'Stop'
        self.stop_watch = not self.stop_watch
        if self.start_prop.text == 'Stop':
            self.reset_prop.text = 'Lap'
        else:
            self.reset_prop.text = 'Reset'

    def cb_select(self):
        if self.start_prop.text == 'Start':
            self.cb_reset()
        else:
            self.cb_lap()

    def cb_reset(self):
        self.stop_watch = False
        self.total_past = 0.0
        self.start_prop.text = 'Start'
        micro_size = int(self.watch_prop.font_size * 0.7)
        self.watch_prop.text = f"00:00.[size={micro_size}]00[/size]"
        self.time_prop.text = "00:00.00"

    def cb_lap(self):
        self.time_prop.text = self.buffer

    def dm_size(self):
        if self.on_size_call:
            label_x, label_y = self.watch_prop.size

            # texture_size の 8 割に対してのサイズを基にする
            if (label_x / label_y) < self.texture_ratio:  # x 方向に対しての比率でフォントサイズを計算
                new_ratio = (label_x * 0.9) / self.texture_ratio
            else:  # y 方向に対しての比率でフォントサイズを計算
                new_ratio = label_y * 0.8

            self.watch_prop.font_size = self.font_ratio * new_ratio
            #self.root.time_prop.font_size = self.font_ratio * new_ratio
            stop_txt_lst = self.watch_prop.text.split('.')
            micro_size = int(self.watch_prop.font_size * 0.6)
            m = self.stop_watch_pat.search(stop_txt_lst[1])
            self.watch_prop.text = f"{stop_txt_lst[0]}.[size={micro_size}]{m.group('size')}[/size]"
            box_height = int(self.watch_prop.size[1] * 0.4)
            self.button_lay_prop.height = box_height
            self.button_lay_prop.padding = int(box_height * 0.15)
            self.button_lay_prop.spacing = int(box_height * 0.15)

        else:
            self.font_ratio = self.watch_prop.font_size / self.watch_prop.texture_size[1]
            self.texture_ratio = self.watch_prop.texture_size[0] / self.watch_prop.texture_size[1]

        self.on_size_call = True


class ClockApp(App):
    def build(self):
        self.stopwatch = StopWatch()


if __name__ == '__main__':
    #Window.clearcolor = get_color_from_hex('#ff6666')
    # resource_add_path(r"C:\Windows\Fonts")
    LabelBase.register(
        name='Roboto',
        fn_regular='Roboto-Thin.ttf',
        fn_bold='Roboto-Medium.ttf'
    )

    ClockApp().run()