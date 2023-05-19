# Quick Menu screen

default in_nvl = False
default quick_menu = True


screen quick_menu():

    zorder 100

    if quick_menu:
            use quick_menu_b


screen quick_menu_b():
    frame:

        xfill True
        ypos 0
        has hbox
        style_prefix "touch_quick"

        xalign 0.5
        yalign 0.8
        spacing 35

        textbutton _("Назад") action Rollback()
        textbutton _("Главное меню") action renpy.full_restart


style quick_menu_frame:
    xfill True
    ysize 150

    background Frame("gui/overlay/menu_top.png", gui.frame_borders, tile=gui.frame_tile)
    padding gui.frame_borders.padding

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


style touch_quick_button is default
style touch_quick_button_text is button_text

style touch_quick_button:
    properties gui.button_properties("touch_quick_button")

style touch_quick_button_text:
    properties gui.button_text_properties("touch_quick_button")
