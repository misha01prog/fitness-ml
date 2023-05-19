default persistent.men_style = True
default persistent.navigation_return_button_style = True
default persistent.navigation_menu_content_style = True
default persistent.quick_menu_style = True
default persistent.quick_menu_align = True


default persistent.gal_screen = False

screen configs():
    tag menu

    add "black"

    side "c":
        area (20, 20, 1040, 1880)

        viewport id "configuration_viewport":
            draggable True
            scrollbars None

            vbox:

                null height 5
                bar ysize 5 xsize 1040

                text "persistent.men_style"
                text "%s" %persistent.men_style

                text "persistent.navigation_return_button_style"
                text "%s" %persistent.navigation_return_button_style

                text "persistent.navigation_menu_content_style"
                text "%s" %persistent.navigation_menu_content_style

                text "persistent.quick_menu_style"
                text "%s" %persistent.quick_menu_style

                text "persistent.quick_menu_align"
                text "%s" %persistent.quick_menu_align

                null height 50

                textbutton _("Return") action Return()