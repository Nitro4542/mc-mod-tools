from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


class MainView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.add_widget(Image(source='assets/mc-mod-tools.png'))

        self.version = Label(text='v0.0.4-alpha')
        self.add_widget(self.version)

        self.button_actions = GridLayout(cols=4)
        self.add_widget(self.button_actions)

        self.backup_button = Button(text='Backup', size_hint=(1, 0.5))
        self.backup_button.bind(on_press=self.backup_button_behaviour)
        self.add_widget(self.backup_button)

        self.install_button = Button(text='Install', size_hint=(1, 0.5))
        self.install_button.bind(on_press=self.install_button_behaviour)
        self.add_widget(self.install_button)

    def backup_button_behaviour(self, *args):
        app.screen_manager.current = 'backupView'

    def install_button_behaviour(self, *args):
        app.screen_manager.current = 'installView'


class BackupView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InstallView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.main_view = MainView()
        screen = Screen(name='mainView')
        screen.add_widget(self.main_view)
        self.screen_manager.add_widget(screen)

        self.backup_view = BackupView()
        screen = Screen(name='backupView')
        screen.add_widget(self.backup_view)
        self.screen_manager.add_widget(screen)

        self.install_view = InstallView()
        screen = Screen(name='installView')
        screen.add_widget(self.install_view)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    app = MyApp()
    app.run()
