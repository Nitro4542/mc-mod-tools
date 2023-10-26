"""A GUI for mc_mod_tools using Kivy"""
# Import all necessary libraries
from configparser import ConfigParser
from kivy.config import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from mc_mod_tools import ModTools

# Create an instance of ModTools class
tools = ModTools()

# Load configuration
config_file = ConfigParser()
config_file.read('config.ini')

# Disable multitouch emulation in Kivy
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class MainView(GridLayout):
    """Main menu"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.add_widget(Image(source='assets/mc-mod-tools.png'))

        self.version = Label(text=config_file.get('DONT-TOUCH', 'version'))
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
        """Switches view to backupView"""
        app.screen_manager.current = 'backupView'

    def install_button_behaviour(self, *args):
        """Switches view to installChoiceView"""
        app.screen_manager.current = 'installChoiceView'

    def remove_button_behaviour(self, *args):
        """Switches view to removeView"""
        app.screen_manager.current = 'removeView'


class BackupView(GridLayout):
    """Backup menu"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.mytitle = Label(text='Backup mods', font_size=32, bold=True)
        self.add_widget(self.mytitle)

        self.button_actions = GridLayout(cols=2, size_hint=(0.1, 0.1))
        self.add_widget(self.button_actions)

        self.backup_view_cancel_button = Button(size_hint=(0.25, 0.25), text='Cancel')
        self.backup_view_cancel_button.bind(on_press=self.backup_view_cancel_button_behaviour)
        self.button_actions.add_widget(self.backup_view_cancel_button)

        self.backup_view_start_button = Button(size_hint=(0.25, 0.25), text='Start')
        self.backup_view_start_button.bind(on_press=self.backup_view_start_button_behaviour)
        self.button_actions.add_widget(self.backup_view_start_button)

    def backup_view_start_button_behaviour(self, *args):
        """Creates backup and switches view to actionCompletedView"""
        tools.create_backup(None)
        app.screen_manager.current = 'actionCompletedView'

    def backup_view_cancel_button_behaviour(self, *args):
        """Switches view back to mainView"""
        app.screen_manager.current = 'mainView'


class InstallChoiceView(GridLayout):
    """Install-selection menu: Select how to install your mod pack"""
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
        """Switches view to installZipView"""
        app.screen_manager.current = 'installZipView'

    def install_folder_button_behaviour(self, *args):
        """Switches view to installFolderView"""
        app.screen_manager.current = 'installFolderView'


class InstallZipView(GridLayout):
    """Menu for installing mods from a zip file"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.mytitle = Label(text='Install mods from ZIP', font_size=32, bold=True)
        self.add_widget(self.mytitle)

        self.zippathinput = TextInput(multiline=False, size_hint=(0.1, 0.1))
        self.add_widget(self.zippathinput)

        self.button_actions = GridLayout(cols=2, size_hint=(0.1, 0.1))
        self.add_widget(self.button_actions)

        self.install_zip_cancel_button = Button(size_hint=(0.25, 0.25), text='Cancel')
        self.install_zip_cancel_button.bind(on_press=self.install_zip_cancel_button_behaviour)
        self.button_actions.add_widget(self.install_zip_cancel_button)

        self.install_zip_start_button = Button(size_hint=(0.25, 0.25), text='Start')
        self.install_zip_start_button.bind(on_press=self.install_zip_start_button_behaviour)
        self.button_actions.add_widget(self.install_zip_start_button)

    def install_zip_start_button_behaviour(self, *args):
        """Installs mods from zip file and switches view to actionCompletedView"""
        tools.install_mods_zip(self.zippathinput.text)
        app.screen_manager.current = 'actionCompletedView'

    def install_zip_cancel_button_behaviour(self, *args):
        """Switches view to mainView"""
        app.screen_manager.current = 'mainView'


class InstallFolderView(GridLayout):
    """Menu for installing mods from a folder"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.mytitle = Label(text='Install mods from folder', font_size=32, bold=True)
        self.add_widget(self.mytitle)

        self.folderpathinput = TextInput(multiline=False, size_hint=(0.1, 0.1))
        self.add_widget(self.folderpathinput)

        self.button_actions = GridLayout(cols=2, size_hint=(0.1, 0.1))
        self.add_widget(self.button_actions)

        self.install_folder_cancel_button = Button(size_hint=(0.25, 0.25), text='Cancel')
        self.install_folder_cancel_button.bind(on_press=self.install_folder_cancel_button_behaviour)
        self.button_actions.add_widget(self.install_folder_cancel_button)

        self.install_folder_start_button = Button(size_hint=(0.25, 0.25), text='Start')
        self.install_folder_start_button.bind(on_press=self.install_folder_start_button_behaviour)
        self.button_actions.add_widget(self.install_folder_start_button)

    def install_folder_start_button_behaviour(self, *args):
        """Installs mods from folder and switches view to actionCompletedView"""
        tools.install_mods(self.folderpathinput.text)
        app.screen_manager.current = 'actionCompletedView'

    def install_folder_cancel_button_behaviour(self, *args):
        """Switches view to mainView"""
        app.screen_manager.current = 'mainView'


class RemoveView(GridLayout):
    """Menu for removing your mods"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.mytitle = Label(text='Remove all of your mods', font_size=32, bold=True)
        self.add_widget(self.mytitle)

        self.button_actions = GridLayout(cols=2, size_hint=(0.1, 0.1))
        self.add_widget(self.button_actions)

        self.remove_view_cancel_button = Button(size_hint=(0.25, 0.25), text='Cancel')
        self.remove_view_cancel_button.bind(on_press=self.remove_view_cancel_button_behaviour)
        self.button_actions.add_widget(self.remove_view_cancel_button)

        self.remove_view_start_button = Button(size_hint=(0.25, 0.25), text='Start')
        self.remove_view_start_button.bind(on_press=self.remove_view_start_button_behaviour)
        self.button_actions.add_widget(self.remove_view_start_button)

    def remove_view_start_button_behaviour(self, *args):
        """Deletes all mods and switches view to mainView"""
        tools.delete_mods()
        app.screen_manager.current = 'actionCompletedView'

    def remove_view_cancel_button_behaviour(self, *args):
        """Switches view to mainView"""
        app.screen_manager.current = 'mainView'


class ActionCompletedView(GridLayout):
    """What you'll see once you completed an action"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.mytitle = Label(text='Action completed.', font_size=32, bold=True)
        self.add_widget(self.mytitle)

        self.button_actions = GridLayout(cols=2, size_hint=(0.1, 0.1))
        self.add_widget(self.button_actions)

        self.action_completed_submit_button = Button(size_hint=(0.25, 0.25), text='Submit')
        self.action_completed_submit_button.bind(on_press=self.action_completed_button_behaviour)
        self.button_actions.add_widget(self.action_completed_submit_button)

    def action_completed_button_behaviour(self, *args):
        """Switches view to mainView"""
        app.screen_manager.current = 'mainView'


class MyApp(App):
    """Needed for ScreenManager"""
    def build(self):
        self.title = 'mc-mod-gui'
        self.screen_manager = ScreenManager()
        self.icon = 'assets/mc-mod-tools.ico'

        self.main_view = MainView()
        screen = Screen(name='mainView')
        screen.add_widget(self.main_view)
        self.screen_manager.add_widget(screen)

        self.backup_view = BackupView()
        screen = Screen(name='backupView')
        screen.add_widget(self.backup_view)
        self.screen_manager.add_widget(screen)

        self.install_choice_view = InstallChoiceView()
        screen = Screen(name='installChoiceView')
        screen.add_widget(self.install_choice_view)
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

        self.action_completed_view = ActionCompletedView()
        screen = Screen(name='actionCompletedView')
        screen.add_widget(self.action_completed_view)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    app = MyApp()
    app.run()
