from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput


class MainView(GridLayout):  # main menu
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
        self.button_actions.add_widget(self.backup_button)

        self.install_button = Button(text='Install', size_hint=(1, 0.5))
        self.install_button.bind(on_press=self.install_button_behaviour)
        self.button_actions.add_widget(self.install_button)

        self.remove_button = Button(text='Remove', size_hint=(1, 0.5))
        self.remove_button.bind(on_press=self.remove_button_behaviour)
        self.button_actions.add_widget(self.remove_button)

    def backup_button_behaviour(self, *args):
        app.screen_manager.current = 'backupView'

    def install_button_behaviour(self, *args):
        app.screen_manager.current = 'installchoiceView'

    def remove_button_behaviour(self, *args):
        app.screen_manager.current = 'removeView'


class BackupView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InstallChoiceView(GridLayout):  # install selection menu
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.button_actions = GridLayout(cols=2)
        self.add_widget(self.button_actions)

        self.install_zip_button = Button(text='Install from ZIP', size_hint=(1, 0.5))
        self.install_zip_button.bind(on_press=self.install_zip_button_behaviour)
        self.button_actions.add_widget(self.install_zip_button)

        self.install_folder_button = Button(text='Install from folder', size_hint=(1, 0.5))
        self.install_folder_button.bind(on_press=self.install_folder_button_behaviour)
        self.button_actions.add_widget(self.install_folder_button)

    def install_zip_button_behaviour(self, *args):
        app.screen_manager.current = 'installZipView'

    def install_folder_button_behaviour(self, *args):
        app.screen_manager.current = 'installFolderView'


class InstallZipView(GridLayout):  # Zip installer menu
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.mytitle = Label(text='Install mods from ZIP', font_size=32)
        self.add_widget(self.mytitle)

        self.zippathinput = TextInput(multiline=False, padding=(5, 5), size_hint=(0.6, 0.5))
        self.add_widget(self.zippathinput)

        self.button_actions = GridLayout(cols=2)
        self.add_widget(self.button_actions)

        self.install_zip_cancel_button = Button(text='Cancel', size_hint=(0.25, 0.25), padding=(5, 5))
        self.install_zip_cancel_button.bind(on_press=self.install_zip_cancel_button_behaviour)
        self.button_actions.add_widget(self.install_zip_cancel_button)

        self.install_zip_start_button = Button(text='Start', size_hint=(0.25, 0.25), padding=(5, 5))
        self.install_zip_start_button.bind(on_press=self.install_zip_start_button_behaviour)
        self.button_actions.add_widget(self.install_zip_start_button)

    def install_zip_start_button_behaviour(self, *args):
        print('Install started.')

    def install_zip_cancel_button_behaviour(self, *args):
        print('Install canceled.')
        quit()


class InstallFolderView(GridLayout):  # Folder installer menu
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.mytitle = Label(text='Install mods from folder', font_size=32)
        self.add_widget(self.mytitle)

        self.folderpathinput = TextInput(multiline=False, padding=(5, 5), size_hint=(0.6, 0.5))
        self.add_widget(self.folderpathinput)

        self.button_actions = GridLayout(cols=2)
        self.add_widget(self.button_actions)

        self.install_folder_cancel_button = Button(text='Cancel', size_hint=(0.25, 0.25), padding=(5, 5))
        self.install_folder_cancel_button.bind(on_press=self.install_folder_cancel_button_behaviour)
        self.button_actions.add_widget(self.install_folder_cancel_button)

        self.install_folder_start_button = Button(text='Start', size_hint=(0.25, 0.25), padding=(5, 5))
        self.install_folder_start_button.bind(on_press=self.install_folder_start_button_behaviour)
        self.button_actions.add_widget(self.install_folder_start_button)

    def install_folder_start_button_behaviour(self, *args):
        print('Install started.')

    def install_folder_cancel_button_behaviour(self, *args):
        print('Install canceled.')
        quit()
class RemoveView(GridLayout):  # remove menu
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }


class MyApp(App):
    def build(self):
        self.title = 'mc-mod-gui'
        self.screen_manager = ScreenManager()

        self.main_view = MainView()
        screen = Screen(name='mainView')
        screen.add_widget(self.main_view)
        self.screen_manager.add_widget(screen)

        self.backup_view = BackupView()
        screen = Screen(name='backupView')
        screen.add_widget(self.backup_view)
        self.screen_manager.add_widget(screen)

        self.installchoice_view = InstallChoiceView()
        screen = Screen(name='installchoiceView')
        screen.add_widget(self.installchoice_view)
        self.screen_manager.add_widget(screen)

        self.remove_view = RemoveView()
        screen = Screen(name='removeView')
        screen.add_widget(self.remove_view)
        self.screen_manager.add_widget(screen)

        self.install_zip_view = InstallZipView()
        screen = Screen(name='installZipView')
        screen.add_widget(self.install_zip_view)
        self.screen_manager.add_widget(screen)

        self.install_folder_view = InstallFolderView()
        screen = Screen(name='installFolderView')
        screen.add_widget(self.install_folder_view)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    app = MyApp()
    app.run()
