import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from lib.source_file import SourceFile
from lib.config import Config


class SourceFileViewer(object):

    def __init__(self, *args, **kwargs):
        Config().load_from_data({
            'CUSTOM_ROOT_PATH': 'custom',
            'Loader': {
                'WHITELIST': ['default.*'],
                'Clang': {
                    'LIB_PATH': '/usr/lib/llvm-14/lib/libclang-14.so',
                },
                'Raw': {
                    'TAB_SIZE': 8,
                },
            },
        })

        self.builder = Gtk.Builder()

        ui = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'glade_ui.glade')
        self.builder.add_from_file(ui)

        SIGNALS = {
            'on_WIN_main_destroy': Gtk.main_quit,
            'on_CB_content_mode_left_changed': self.on_CB_content_mode_left_changed,
            'on_CB_content_mode_right_changed': self.on_CB_content_mode_right_changed,
        }
        self.builder.connect_signals(SIGNALS)

        self.src_file = None

    @property
    def has_succeeded(self):
        return True

    def _load_content(self, textview, src_file):
        textview.get_buffer().set_text('\n'.join(src_file))

    def _on_content_mode_changed(self, side, *args):
        mode = self.builder.get_object(f'CB_content_mode_{side}').get_active_text()
        
        self._load_content(self.builder.get_object(f'TV_content_{side}'), self.src_file.get_content(mode))

    def on_CB_content_mode_left_changed(self, *args):
        self._on_content_mode_changed('left', *args)

    def on_CB_content_mode_right_changed(self, *args):
        self._on_content_mode_changed('right', *args)

    def _fill_CB_content_mode(self, side, store):
        self.builder.get_object(f'CB_content_mode_{side}').set_model(store)
        self.builder.get_object(f'CB_content_mode_{side}').set_active(0)

    def run(self):

        with open('test_file.c', 'r', encoding='utf-8') as f:
            self.src_file = SourceFile(f)

            content_mode_store = Gtk.ListStore(str)
            content_mode_store.append(['raw'])
            for mode in self.src_file.all_loaders_name:
                if mode == 'raw':
                    continue
                content_mode_store.append([mode])

            self._fill_CB_content_mode('left', content_mode_store)
            self._fill_CB_content_mode('right', content_mode_store)

            self.builder.get_object('WIN_main').show_all()

            Gtk.main()

