# This file contains options that can be changed to customize your app.



# Basics

define config.name = _("FitnessML")
define gui.show_name = True
define config.version = "1.0"
define build.name = "FitnessML"


# Gestures

define config.gestures = { "e" : "rollback" , "w" : "rollforward", }
define config.dispatch_gesture = None


# Sounds and music

define config.has_sound = True
define config.has_music = True
define config.has_voice = True
define config.default_music_volume = 1.0
define config.default_sfx_volume = 1.0
define config.default_voice_volume = 1.0
define config.sample_sound = "audio/Danse Macabre - Big Change.mp3"
define config.sample_voice = "audio/Danse Macabre - Big Hit 1.mp3"


# Transitions

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = fade
define config.end_game_transition = dissolve


# Window management

define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


# Preference defaults

default preferences.text_cps = 50
default preferences.afm_time = 15
define config.hw_video = True
define config.save_on_mobile_background = True
define config.quit_on_mobile_background = False


# Save directory

define config.save_directory = "VKR_25"


# Icon

define config.window_icon = "gui/window_icon.png"

# Build configuration

init python:

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.classify('game/**.png', 'archive')
    build.classify('game/**.jpg', 'archive')
    build.classify('game/**.ttf', 'archive')

    build.documentation('*.html')
    build.documentation('*.txt')