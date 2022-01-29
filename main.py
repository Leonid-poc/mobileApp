from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.window import Window

import matplotlib.pyplot as plt
import numpy as np

class MyApp(App):
    def build(self):
        self.x = np.arange(-25, 25, .1)
        plt.plot(self.x, eval('np.sin(self.x)'))
        plt.grid(True)
        plt.savefig('main.png')
        self.otvet_png = Image(source='main.png')


        self.formula1 = ''
        self.formula2 = ''
        self.focus = 0

        self.bl = BoxLayout(orientation='vertical', spacing=5)
        self.gl = GridLayout(cols=5, spacing = [5, 5], size_hint=(1, .7))
        # --------------------------Помощь------------------------------
        self.help_pop = BoxLayout(orientation='vertical')
        text1 = "\
        Данная программа была написана для построения графиков\
        -------------------------------------------------------------------------------------------------------------------------------------------------\
        \n!!! Внимание !!!\
        \nУбедительная просьба писать все операции через пробел, \
        \nиначе программа будет работать не корректно, например:\
        \n123 * x + 987 / x \
        \nили\
        \nsin(x) ** 2 - tg(x ** 2)\
        -------------------------------------------------------------------------------------------------------------------------------------------------\
        \nОбозначения:\
        \nпустая кнопка - пробел\
        \nlog2(8) == 3 - логарифм 8 по основанию 2 равен 3\
        \nln(e ** 2) == 2 - логарифм экспоненты в квадрате по основанию экспаненты равна 2\
        \n** - возведение в степень (2 ** 3 тобишь 2 в третьей степени)\
        \n* - умножить\
        \n/ - деление\
        "
        self.help_pop.add_widget(Label(text=text1, size_hint=(1, .8), text_size=(720, None), halign='center'))
        self.help_pop.add_widget(Button(text='Закрыть', on_press=self.close_pop, size_hint=(1, .2), background_color=[1,.08,.14, 1]))
        # -------------------------Настройки----------------------------
        self.set_pop = BoxLayout(orientation='vertical')
        self.set_pop.add_widget(Label(text='Цвет заднего фона', size_hint=(1, .2)))
        self.color_background = ColorPicker()
        self.set_pop.add_widget(self.color_background)
        self.set_pop.add_widget(Button(text='Принять', on_press=self.update_background, size_hint=(1, .2), background_color=[.05,1,.04, 1]))
        self.set_pop.add_widget(Button(text='Отклонить', on_press=self.close_pop, size_hint=(1, .2), background_color=[1,.08,.14, 1]))
        # ------------------Создание всплывающих окон-------------------
        self.settings = Popup(title='Настройки', content=self.set_pop)
        self.help = Popup(title='Помощь', title_color=[1, .98 ,0 , 1], content=self.help_pop)

        self.settings_l = BoxLayout(orientation='horizontal', padding=[10, 5, 10, 5], spacing=10, size_hint=(1, .1))
        self.settings_l.add_widget(Button(text='Помощь', on_press=self.help.open))
        self.settings_l.add_widget(Button(text='Настройки', on_press=self.settings.open))
        # ------------------Создание полей для ввода формул-------------
        self.input_l1 = BoxLayout(orientation='horizontal', spacing=5, size_hint=(1, 0.15), padding=[0, 0, 5, 0])
        self.input_l2 = BoxLayout(orientation='horizontal', spacing=5, size_hint=(1, 0.15), padding=[0, 0, 5, 0])

        self.y1 = Label(text='y1 = ', size_hint=(0.2, 1))
        self.y2 = Label(text='y2 = ', size_hint=(0.2, 1))
        self.input_l1.add_widget(self.y1)
        self.input_l2.add_widget(self.y2)
        self.text_inp1 = TextInput(size_hint=(0.8, 1), text='', on_double_tap=self.clear_inp)
        self.text_inp2 = TextInput(size_hint=(0.8, 1), text='', on_double_tap=self.clear_inp)
        self.input_l1.add_widget(self.text_inp1)
        self.input_l2.add_widget(self.text_inp2)
        # ----------Создание математический функций и цифр--------------
        self.gl.add_widget(Button(text='sin(', background_color=[1, .25, .78, 0.5], on_press=self.change, font_size=20))
        self.gl.add_widget(Button(text='cos(', background_color=[1, .25, .78, 0.5], on_press=self.change, font_size=20))
        self.gl.add_widget(Button(text='tg(', background_color=[1, .25, .78, 0.5], on_press=self.change, font_size=20))
        self.gl.add_widget(Button(text='ctg(', background_color=[1, .25, .78, 0.5], on_press=self.change, font_size=20))
        for i in ['π', '7', '8', '9', 'e', '+', '4', '5', '6', 'log2(', '-', '1', '2', '3', 'ln(', '*', '0', '/', '.', ' ']:
            self.gl.add_widget(Button(text=i, background_color=[1, .25, .78, 0.5], on_press=self.change, font_size=20))
        self.gl.add_widget(Button(text='=', background_color=[1, .25, .78, 0.5], on_press=self.result, font_size=20))
        # ----------------Изменение амплитуды графика-------------------
        self.bl_amplituda = BoxLayout(orientation='horizontal', size_hint_y = .1)
        self.amplituda_slider = Slider(min=0, max=100, value=25, on_touch_move=self.amplituda_move, on_touch_up=self.amplituda_up, value_track=True)
        self.amplituda_label = Label(text='25', size_hint_x = .1)
        self.bl_amplituda.add_widget(self.amplituda_slider)
        self.bl_amplituda.add_widget(self.amplituda_label)
        # -----------Добавление всего на главный экран------------------
        self.bl.add_widget(self.settings_l)
        self.bl.add_widget(self.otvet_png)
        self.bl.add_widget(self.bl_amplituda)
        self.bl.add_widget(self.input_l1)
        self.bl.add_widget(self.input_l2)
        self.bl.add_widget(self.gl)
        return self.bl

    def amplituda_move(self, widget, _):
        self.amplituda_label.text = str(round(widget.value))
    
    def amplituda_up(self, widget, _):
        s = round(widget.value)
        self.x = np.arange(-s, s, .1)


    def close_pop(self, widget):
        if widget.text.startswith('Отклонить'):
            self.settings.dismiss()
        elif widget.text.startswith('Закрыть'):
            self.help.dismiss()

    def update_background(self, widget):
        Window.clearcolor = list(self.color_background.color)
        s = Window.clearcolor
        if sum(s[:-1]) < 1.:
            self.y1.color = [1,1,1,1]
            self.y2.color = [1,1,1,1]
            self.amplituda_label = [1,1,1,1]
        else:
            self.y1.color = [0,0,0,1]
            self.y2.color = [0,0,0,1]
            self.amplituda_label = [0,0,0,1]
        self.settings.dismiss()

    def clear_inp(self, widget):
        widget.text = ''
        self.formula1, self.formula2 = '', ''

    def change(self, widget):
        if self.text_inp1.focus:
            self.focus = 0
        elif self.text_inp2.focus:
            self.focus = 1
        if not self.focus:
            self.text_inp1.focus = True
        else: self.text_inp2.focus = True

        if self.text_inp1.focus:
            self.text_inp1.text += widget.text
        else:
            self.text_inp2.text += widget.text


    def result(self, widget):
        self.formula1 = self.text_inp1.text
        self.formula2 = self.text_inp2.text
        try:
            plt.clf()
            plt.grid(True)
            if self.formula1:
                plt.plot(self.x, eval(self.formula1.replace('sin', 'np.sin').replace('cos', 'np.cos').replace('tg', 'np.tan').replace('ctg', '1/np.tan').
                replace('log2', 'np.log2').replace('ln', 'np.log').replace('e', 'np.e').replace('π', 'np.pi').replace('x', 'self.x')))
            if self.formula2:
                plt.plot(self.x, eval(self.formula2.replace('sin', 'np.sin').replace('cos', 'np.cos').replace('tg', 'np.tan').replace('ctg', '1/np.tan').
                replace('log2', 'np.log2').replace('ln', 'np.log').replace('e', 'np.e').replace('π', 'np.pi').replace('x', 'self.x')))
            plt.savefig('main.png')
            self.otvet_png.reload()
        except Exception as e:
            Popup(title='Уведомление', size_hint=(.5, .5), content=Label(text='Пожалуйста, проверьте что у вас \nвведены только значения\nкоторые есть на клавиатуре\nа также переменная "x"', halign='center')).open()


if __name__ == '__main__':
    MyApp().run()