import traceback
import runpy

try:
    runpy.run_module("app_main", run_name="__main__")
except Exception:
    err = traceback.format_exc()

    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.label import Label
    from kivy.uix.scrollview import ScrollView

    class ErrorApp(App):
        def build(self):
            label = Label(
                text=err,
                font_size="11sp",
                halign="left",
                valign="top",
                size_hint_y=None,
                text_size=(Window.width - 20, None),
            )
            label.bind(
                texture_size=lambda inst, size: setattr(inst, "height", size[1])
            )
            scroll = ScrollView()
            scroll.add_widget(label)
            return scroll

    ErrorApp().run()
