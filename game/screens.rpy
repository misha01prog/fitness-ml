# Initialization


init offset = -1


# Styles


style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################


init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos


# Input screen

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


# Choice screen 


screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 350
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")



# Main and Game Menu Screens

# Navigation screen 

screen navigation():

    tag menu

    if persistent.navigation_menu_content_style:

        frame:
            style_prefix "main_menu"

            at menu_appear_side

            grid 1 3:
                xalign 24
                yalign 0.5
                textbutton _("Главное меню") action renpy.full_restart
                textbutton _("Помощь") action ShowMenu("help")
                if not renpy.variant("mobile"):
                    textbutton _("Выход") action Quit(confirm = True)
                else:
                    null
                null

            if persistent.navigation_return_button_style:
                textbutton _("Закрыть") action Hide("navigation"), Return():
                    xalign 0.5
                    yalign 1.0

            else:
                fixed:
                    xmaximum 60
                    xalign 0.99
                    yalign 0.1
                    textbutton "≡" action Hide("navigation"), Return()


style navigation_menu_frame:
    xfill True
    ysize 300

    background Frame("gui/overlay/menu_bottom.png", gui.frame_borders, tile=gui.frame_tile)
    padding gui.frame_borders.padding
style navigation_menu_vbox is main_menu_vbox
style navigation_menu_text is main_menu_text


transform menu_appear_side:
    on show, replace:
        xpos -432
        linear 0.36 xpos 0
    on hide, replaced:
        linear 0.36 xpos -432





## Main Menu screen 

screen main_menu():

    tag menu

    style_prefix "main_menu"

    add gui.main_menu_background

    use mm_content


screen mm_content():


    if persistent.men_style:
        grid 2 1:

            xalign 0.5
            yalign 0.965
            spacing 20

            imagebutton:
                alt "Начать"
                auto new_game_button_image
                hover_foreground Text(_("Начать"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Начать"), xalign=0.5, yalign=0.5)
                action Start()
                tooltip _("Начать тренировку")

            imagebutton:
                alt "Помощь"
                auto settings_button_image
                hover_foreground Text(_("Помощь"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Помощь"), xalign=0.5, yalign=0.5)
                action ShowMenu("help")
                tooltip _("Как пользоваться приложением")

        if gui.show_name:

            vbox:
                xalign 0.5
                ypos 0.5
                text "Fitness ML":
                    style "main_menu_title"

                text "Тихонов М.Н. БИВ194":
                    style "main_menu_version"


    elif not persistent.men_style:

        frame:
            grid 1 3:
                xalign 0.5
                yalign 0.5

                spacing 30

                imagebutton:
                    alt "Начать"
                    auto new_game_button_image
                    hover_foreground Text(_("Начать"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Начать"), xalign=0.5, yalign=0.5)
                    action Start()
                    tooltip _("Начать тренировку")

                imagebutton:
                    alt "Помощь"
                    auto help_button_image
                    hover_foreground Text(_("Помощь"), xalign=0.5, yalign=0.5)
                    idle_foreground Text(_("Помощь"), xalign=0.5, yalign=0.5)
                    action ShowMenu("help")
                    tooltip _("Как пользоваться приложением")

                if not renpy.variant("mobile"):
                    imagebutton:
                        alt "Выход"
                        auto quit_button_image
                        hover_foreground Text(_("Выход"), xalign=0.5, yalign=0.5)
                        idle_foreground Text(_("Выход"), xalign=0.5, yalign=0.5)
                        action Quit(confirm=not main_menu)
                        tooltip _("Выйти из приложения")
                else:
                    null

            if gui.show_name:

                vbox:
                    xalign 1.0
                    ypos 1.0
                    text "[config.name!t]":
                        style "main_menu_title"

                    text "[config.version]":
                        style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 416
    yfill True

    background Frame("gui/overlay/menu_side.png", gui.frame_borders, tile=gui.frame_tile)
    padding gui.frame_borders.padding

style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")



screen nav_content():

    grid 2 1:

        xalign 0.5
        yalign 0.965
        spacing 20

        if main_menu:
            imagebutton:
                alt "Начать"
                auto new_game_button_image
                hover_foreground Text(_("Начать"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Начать"), xalign=0.5, yalign=0.5)
                action Start()
                tooltip _("Начать тренировку")

        imagebutton:
            alt "Вернуться"
            auto return_button_image
            hover_foreground Text(_("Вернуться"), xalign=0.5, yalign=0.5)
            idle_foreground Text(_("Вернуться"), xalign=0.5, yalign=0.5)
            action Return()
            tooltip _("Вернуться назад")


# Game Menu screen 

screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude

                else:

                    transclude
    use nav_content

    hbox:
        xalign 0.5
        label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 436
    top_padding 120

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 416
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 40
    top_margin 10

style game_menu_viewport:
    xsize 1080

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30


screen help():
    $ tooltip = GetTooltip()

    tag menu

    use game_menu(_("Помощь"), scroll="viewport"):

        style_prefix "help"

        null height 10
        bar ysize 10 xsize 1000
        null height 10

        vbox:
            use keyboard_content


screen keyboard_content():
    style_prefix "help"
    vbox:
        label _("Тренировка")
        text _("Нажмите 'Начать', чтобы подобрать оптимальную нагрузку и начать тренировку")

    vbox:
        label _("Редактирование параметров")
        text _("Чтобы отредактировать персональные параметры и подобрать оптимальную нагрузку")

    vbox:
        label _("Ручное изменение нагрузки")
        text _("Navigate the interface.")


default persistent.controller_kind = "ps"


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text

style help_text:
    size gui.text_size

style help_button:
    properties gui.button_properties("help_button")
    xmargin 8

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 250
    right_padding 20

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0


# Additional screens

# Confirm screen 

screen confirm(message, yes_action, no_action):

    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Да") action yes_action
                textbutton _("Нет") action no_action

    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


# Skip indicator screen 

screen skip_indicator():

    zorder 100

    if not renpy.get_screen("nvl"):
        style_prefix "skip"
    else:
        style_prefix "nvl_skip"

    frame:

        hbox:
            spacing 6

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    font "DejaVuSans.ttf"

style nvl_skip_frame is empty
style nvl_skip_text is gui_text
style nvl_skip_triangle is skip_text

style nvl_skip_frame:
    ypos gui.nvl_skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style nvl_skip_text:
    size gui.notify_text_size

# Notify screen 

screen notify(message):

    zorder 100

    if not renpy.get_screen("nvl"):
        style_prefix "notify"
    else:
        style_prefix "nvl_notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')



transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")

style nvl_notify_frame is empty
style nvl_notify_text is gui_text

style nvl_notify_frame:
    ypos gui.nvl_notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style nvl_notify_text:
    properties gui.text_properties("notify")

init -2:
    screen _gamepad_select(joysticks):


        use game_menu(_("Settings"), scroll="viewport"):

            vbox:
                xfill True

                label _("Select Gamepad to Calibrate")

                if not joysticks:
                    text _("No Gamepads Available")
                else:
                    for i, name in joysticks:
                        textbutton "[i]: [name]" action Return(i) size_group "joysticks"

                null height 20

                textbutton _("Cancel") action Return("cancel")

    screen _gamepad_control(name, control, kind, mappings, back, i, total):


        use game_menu(_("Settings"), scroll="viewport"):

            vbox:
                xfill True

                label _("Calibrating [name] ([i]/[total])")

                null height 20

                text _("Press or move the [control] [kind].")


                null height 20

                hbox:
                    textbutton _("Cancel") action Return("cancel")
                    if len(mappings) >= 2:
                        textbutton _("Skip (A)") action Return("skip")

                    if back and len(mappings) >= 3:
                        textbutton _("Back (B)") action Return(back)

            add _gamepad.EventWatcher(mappings)

screen underconstruction():

    tag menu
    use game_menu(_("Unavailable"), scroll="viewport"):

        vbox:
            null height 45
            style_prefix "about"
            xsize 1000


            text _("This Feature is currently unavailable"):
                xalign 0.5


# NVL screen 

screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            ypos 45

            use nvl_dialogue(dialogue)

        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")




# Mobile Variants


style pref_vbox:
    variant "medium"
    xsize 450

style game_menu_navigation_frame:
    variant "small"
    xsize 340

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 400

style slider_pref_vbox:
    variant "small"
    xsize None

style slider_pref_slider:
    variant "small"
    xsize 600
