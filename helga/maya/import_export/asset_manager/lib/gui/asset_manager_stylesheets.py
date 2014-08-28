
"""
asset_manager_stylesheets
==========================================

Module that has only one method.

#. get_stylesheet
"""













#Import
#------------------------------------------------------------------

#Import variable
do_reload = True


#asset_manager

#asset_manager_globals
from lib import asset_manager_globals
if(do_reload):reload(asset_manager_globals)







#Globals
#------------------------------------------------------------------

#Pathes
TOOL_ROOT_PATH = asset_manager_globals.TOOL_ROOT_PATH
MEDIA_PATH = asset_manager_globals.MEDIA_PATH
ICONS_PATH = asset_manager_globals.ICONS_PATH

#Fonts
FUTURA_LT_LIGHT = asset_manager_globals.FUTURA_LT_LIGHT

#Header
HEADER_IMAGE = asset_manager_globals.HEADER_IMAGE

#Transparency
TABLEVIEW_EDITOR_TRANSPARENCY = asset_manager_globals.TABLEVIEW_EDITOR_TRANSPARENCY

#AssetManager colors
BRIGHT_ORANGE = asset_manager_globals.BRIGHT_ORANGE
DARK_ORANGE = asset_manager_globals.DARK_ORANGE
BRIGHT_BLUE = asset_manager_globals.BRIGHT_BLUE
DARK_BLUE = asset_manager_globals.DARK_BLUE
BRIGHT_GREY = asset_manager_globals.BRIGHT_GREY
GREY = asset_manager_globals.GREY
DARK_GREY = asset_manager_globals.DARK_GREY






#get_stylesheet
#------------------------------------------------------------------

def get_stylesheet():
    """
    Return stylesheet string, defining all stylesheets for AssetManager.
    """

    #ss_dict
    ss_dict = {'icon_path' : HEADER_IMAGE,
                'futura_lt_light' : FUTURA_LT_LIGHT,
                'bright_orange' : BRIGHT_ORANGE.name(),
                'bright_orange_transparent' : 'rgba({0},{1},{2},{3})'.format(BRIGHT_ORANGE.red(), BRIGHT_ORANGE.green(), BRIGHT_ORANGE.blue(), TABLEVIEW_EDITOR_TRANSPARENCY),
                'dark_orange' : DARK_ORANGE.name(),
                'dark_orange_transparent' : 'rgba({0},{1},{2},{3})'.format(DARK_ORANGE.red(), DARK_ORANGE.green(), DARK_ORANGE.blue(), TABLEVIEW_EDITOR_TRANSPARENCY),
                'bright_blue' : BRIGHT_BLUE.name(),
                'bright_blue_transparent' : 'rgba({0},{1},{2},{3})'.format(BRIGHT_BLUE.red(), BRIGHT_BLUE.green(), BRIGHT_BLUE.blue(), TABLEVIEW_EDITOR_TRANSPARENCY),
                'dark_blue' : DARK_BLUE.name(),
                'dark_blue_transparent' : 'rgba({0},{1},{2},{3})'.format(DARK_BLUE.red(), DARK_BLUE.green(), DARK_BLUE.blue(), TABLEVIEW_EDITOR_TRANSPARENCY),
			    'bright_grey' : BRIGHT_GREY.name(),
                'bright_grey_transparent' : 'rgba({0},{1},{2},{3})'.format(BRIGHT_GREY.red(), BRIGHT_GREY.green(), BRIGHT_GREY.blue(), TABLEVIEW_EDITOR_TRANSPARENCY),
			    'grey' : GREY.name(),
                'grey_transparent' : 'rgba({0},{1},{2},{3})'.format(GREY.red(), GREY.green(), GREY.blue(), TABLEVIEW_EDITOR_TRANSPARENCY),
			    'dark_grey' : DARK_GREY.name(),
                'dark_grey_transparent' : 'rgba({0},{1},{2},{3})'.format(DARK_GREY.red(), DARK_GREY.green(), DARK_GREY.blue(), TABLEVIEW_EDITOR_TRANSPARENCY)}


    #str_stylesheet
    str_stylesheet = " \
\
\
/* QWidget */\
QWidget { background-color: %(dark_grey)s; \
            font-family: \"%(futura_lt_light)s\"; \
            font-size: 14pt; \
            selection-background-color: %(bright_blue)s; \
} \
\
\
/* QWidget - wdgt_header_icon */\
QWidget#wdgt_header_icon { border-image: url(%(icon_path)s); } \
\
\
\
\
\
\
/* QToolTip */\
QToolTip { background-color: %(dark_grey)s; \
            font-size: 14pt; \
            color: %(bright_grey)s; \
            border-left: none; \
            border-top: 1px solid %(bright_orange)s; \
            border-bottom: none; \
            border-right: none; \
} \
\
\
\
\
\
\
/* QLabel - lbl_explanation_header */\
QLabel#lbl_explanation_header { background-color: transparent; \
                                font-weight: bold; \
                                font-size: 20pt; \
                                color: %(bright_grey)s; \
                                margin-top: 10; \
                                margin-left: 10; \
                                margin-bottom: 4; \
                                margin-right: 10; \
} \
\
\
/* QLabel - lbl_explanation_text */\
QLabel#lbl_explanation_text { background-color: transparent; \
                                color: %(bright_grey)s; \
                                margin-top: 4; \
                                margin-left: 10; \
                                margin-bottom: 4; \
                                margin-right: 10; \
} \
\
\
\
\
\
\
/* QProgressBar */\
QProgressBar { border: none;\
                 background-color: %(dark_grey)s;\
                 text-align: center;\
} \
\
\
\
\
\
\
\
\
/* QLineEdit */\
QLineEdit { border: none;\
            background-color: %(grey)s;\
} \
\
\
\
\
\
\
\
\
/* QMenuBar - mnubar_dev */\
QMenuBar#mnubar_dev { background-color: transparent;\
                        border-left: none; \
                        border-right: none; \
                        border-bottom: none; \
                        border-top: none; \
} \
\
\
/* QMenuBar - mnubar_dev - item */\
QMenuBar#mnubar_dev::item { background: transparent;\
                            margin-left: 8; \
                            margin-right: 8; \
                            border-left: none; \
                            border-right: none; \
                            border-bottom: none; \
                            border-top: none; \
} \
\
\
/* QMenuBar - mnubar_dev - item - selected */\
QMenuBar#mnubar_dev::item:selected { background: transparent;\
                                        color: %(bright_orange)s; \
                                        border-left: none; \
                                        border-right: none; \
                                        border-bottom: none; \
                                        border-top: none; \
} \
\
\
/* QMenuBar - mnubar_dev - item - pressed */\
QMenuBar#mnubar_dev::item:pressed { background: transparent;\
                                        color: %(dark_orange)s; \
                                        border-left: none; \
                                        border-right: none; \
                                        border-bottom: none; \
                                        border-top: none; \
} \
\
\
\
\
\
\
\
\
/* QMenu - separator */\
QMenu::separator { background: %(bright_orange)s;\
                    height: 1px; \
                    margin-left: 8; \
                    margin-right: 8; \
                    border-left: none; \
                    border-right: none; \
                    border-bottom: none; \
                    border-top: none; \
} \
\
\
/* QMenu - mnu_threads */\
QMenu#mnu_threads { background-color: %(dark_grey)s;\
                    border-left: none; \
                    border-right: none; \
                    border-bottom: none; \
                    border-top: none; \
} \
\
\
/* QMenu - mnu_threads - item */\
QMenu#mnu_threads::item { background: transparent;\
                            margin-left: 8; \
                            margin-right: 8; \
                            border: none;\
} \
\
\
/* QMenu - mnu_threads - item - selected */\
QMenu#mnu_threads::item:selected { color: %(dark_orange)s;\
                                    border: none; \
} \
\
\
/* QMenu - mnu_gui */\
QMenu#mnu_gui { background-color: %(dark_grey)s;\
                border-left: none; \
                border-right: none; \
                border-bottom: none; \
                border-top: none; \
} \
\
\
/* QMenu - mnu_gui - item */\
QMenu#mnu_gui::item { background: transparent;\
                        margin-left: 8; \
                        margin-right: 8; \
                        border: none;\
} \
\
\
/* QMenu - mnu_gui - item - selected */\
QMenu#mnu_gui::item:selected { color: %(dark_orange)s;\
                                border: none; \
} \
\
\
\
\
\
\
\
\
/* QScrollBar */\
QScrollBar { background: %(dark_grey)s; \
                    border: none; \
} \
\
\
\
\
\
\
/* QTableCornerButton */\
QTableCornerButton { background-color: %(grey)s; \
                        border: none; \
}\
\
\
/* QTableCornerButton - section */\
QTableCornerButton::section { background-color: %(grey)s; \
                                border: none; \
}\
\
\
\
\
\
\
/* ShotMetadataView */\
ShotMetadataView { background-color: %(grey)s; \
                    selection-background-color: qlineargradient(spread:pad, x1:0.7, y1:0.9, x2:1, y2:1, \
                    stop:0 %(grey)s, \
                    stop:1 %(bright_orange_transparent)s); \
                    border-left: none; \
                    border-top: none; \
                    border-bottom: none; \
                    border-right: none; \
} \
\
\
\
\
\
\
/* QHeaderView - shot_metadata_view_hor_header*/\
QHeaderView#shot_metadata_view_hor_header{ background-color: %(grey)s; \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: none; \
} \
\
\
/* QHeaderView - shot_metadata_view_hor_header - section */\
QHeaderView#shot_metadata_view_hor_header::section { background-color: qlineargradient(spread:reflect, x1:0.06, y1:0.04, x2:0, y2:0, \
                                                    stop:0.8 %(grey)s, \
                                                    stop:1 %(dark_orange)s); \
                                                    font-weight: bold; \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: 1px solid %(bright_grey)s; \
} \
\
\
/* QHeaderView - shot_metadata_view_ver_header */\
QHeaderView#shot_metadata_view_ver_header { background-color: %(grey)s; \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: none; \
} \
\
\
/* QHeaderView - shot_metadata_view_ver_header - section */\
QHeaderView#shot_metadata_view_ver_header::section { background-color: %(grey)s; \
                                                    border-left: none; \
                                                    border-top: none; \
                                                    border-bottom: none; \
                                                    border-right: none; \
} \
\
\
\
\
\
\
/* ShotMetadataContextMenu */\
ShotMetadataContextMenu { background-color: %(dark_grey_transparent)s; \
                            color: %(bright_grey)s; \
                            border-left: none; \
                            border-top: 1px solid %(bright_orange)s; \
                            border-bottom: none; \
                            border-right: none; \
} \
\
\
/* ShotMetadataContextMenu -item - selected */\
ShotMetadataContextMenu::item:selected { background-color: %(bright_orange_transparent)s; \
} \
\
\
\
\
\
\
/* TableViewEditorFramerange */\
/* This widget has a transparent background. Below are the stylesheets for the */\
/* children of this widget. */\
\
\
/* QSpinBox - spnbx_frame */\
QSpinBox#spnbx_frame { background-color: transparent; \
                        border-left: none; \
                        border-top: 1px solid %(bright_orange_transparent)s; \
                        border-bottom: 1px solid %(bright_orange_transparent)s; \
                        border-right: none; \
} \
\
\
/* QWidget - wdgt_table_view_editor_framerange_main */\
QWidget#wdgt_table_view_editor_framerange_main { background-color: %(grey_transparent)s; \
                                                    border: 1px solid %(bright_orange_transparent)s; \
} \
\
\
/* QWidget - wdgt_frame */\
QWidget#wdgt_frame { background-color: transparent; \
} \
\
\
/* QWidget - wdgt_range_and_time_slider */\
QWidget#wdgt_range_and_time_slider { background-color: transparent; \
} \
\
\
/* QWidget - wdgt_frame_slider */\
QWidget#wdgt_frame_slider { background-color: transparent; \
                            border-left: none; \
                            border-top: none; \
                            border-bottom: none; \
                            border-right: none; \
} \
\
\
/* QWidget - wdgt_frame_slider_left */\
QWidget#wdgt_frame_slider_left { background-color: qlineargradient(spread:reflect, x1:0.3, y1:0, x2:0, y2:0, \
                                                                    stop:0.45 transparent, \
                                                                    stop:0.5 %(dark_orange_transparent)s, \
                                                                    stop:0.55 transparent); \
} \
\
\
/* QWidget - wdgt_frame_slider_right */\
QWidget#wdgt_frame_slider_right { background-color: qlineargradient(spread:reflect, x1:0.1, y1:0, x2:0, y2:0, \
                                                                    stop:0.45 transparent, \
                                                                    stop:0.5 %(dark_orange_transparent)s, \
                                                                    stop:0.55 transparent); \
} \
\
\
/* AssetManagerHoverButton - btn_get_current_frame*/\
AssetManagerHoverButton#btn_get_current_frame { background-color: %(bright_grey_transparent)s; \
                                                color: %(bright_grey)s; \
                                                border: none; \
} \
\
\
/* QWidget - wdgt_range_slider */\
QWidget#wdgt_range_slider { background-color: transparent; \
                            border-left: none; \
                            border-top: none; \
                            border-bottom: none; \
                            border-right: none; \
} \
\
\
/* QWidget - wdgt_range_scrollbar */\
QWidget#wdgt_range_scrollbar { background-color: transparent; \
} \
\
\
/* QWidget - wdgt_range_slider_left */\
QWidget#wdgt_range_slider_left { background-color: %(dark_grey_transparent)s; \
} \
\
\
/* QWidget - wdgt_range_slider_middle */\
QWidget#wdgt_range_slider_middle { background-color: %(bright_grey_transparent)s; \
} \
\
\
/* QWidget - wdgt_range_slider_right */\
QWidget#wdgt_range_slider_right { background-color: %(dark_grey_transparent)s; \
} \
\
\
/* QLabel - lbl_framesource */\
QLabel#lbl_framesource { background-color: transparent; \
} \
\
\
/* AssetManagerHoverButton - btn_complete_range_start*/\
AssetManagerHoverButton#btn_complete_range_start { background-color: %(grey_transparent)s; \
                                                    color: %(bright_grey)s; \
                                                    border: 1px solid %(bright_orange_transparent)s; \
} \
\
\
/* AssetManagerHoverButton - btn_current_range_start*/\
AssetManagerHoverButton#btn_current_range_start { background-color: %(dark_orange_transparent)s; \
                                                    color: %(bright_grey)s; \
                                                    border: 1px solid %(bright_orange_transparent)s; \
} \
\
\
/* AssetManagerHoverButton - btn_complete_range_end*/\
AssetManagerHoverButton#btn_complete_range_end { background-color: %(grey_transparent)s; \
                                                    color: %(bright_grey)s; \
                                                    border: 1px solid %(bright_orange_transparent)s; \
} \
\
\
/* AssetManagerHoverButton - btn_current_range_end*/\
AssetManagerHoverButton#btn_current_range_end { background-color: %(dark_orange_transparent)s; \
                                                color: %(bright_grey)s; \
                                                border: 1px solid %(bright_orange_transparent)s; \
} \
\
\
\
\
\
\
/* TableViewEditorNodepicker */\
/* This widget has a transparent background. Below are the stylesheets for the */\
/* children of this widget. */\
\
\
/* QWidget - wdgt_table_view_editor_nodepicker_main */\
QWidget#wdgt_table_view_editor_nodepicker_main { background-color: %(grey_transparent)s; \
                                                    border: 1px solid %(bright_orange_transparent)s; \
} \
\
\
/* QLabel - lbl_nodetype */\
QLabel#lbl_nodetype { background-color: %(grey_transparent)s; \
} \
\
\
/* QLineEdit - le_filter */\
QLineEdit#le_filter { background-color: %(dark_grey_transparent)s; \
                        border: 1px solid %(dark_orange_transparent)s; \
} \
\
\
/* QListView - node_view */\
QListView#node_view { background-color: %(grey_transparent)s; \
                        alternate-background-color: %(dark_grey_transparent)s; \
                        border-left: none; \
                        border-top: none; \
                        border-bottom: none; \
                        border-right: none; \
} \
\
\
/* QListView - node_view - item selected */\
QListView#node_view::item:selected { background-color: %(bright_orange)s; \
                                        border-left: none; \
                                        border-top: none; \
                                        border-bottom: none; \
                                        border-right: none; \
} \
\
\
\
\
\
\
/* AssetManagerSliderAction */\
/* QWidgetAction that draws a slider and an LCD Display */\
\
\
/* AssetManagerSliderAction - QLabel */\
QLabel#AssetManagerSliderActionQLabel { background-color: transparent; \
                                        margin-left: 8; \
                                        margin-right: 8; \
} \
\
\
/* AssetManagerSliderAction - QWidget */\
QWidget#AssetManagerSliderActionQWidget { background-color: transparent; \
                                            margin-left: 8; \
                                            margin-right: 8; \
} \
\
\
/* AssetManagerSliderAction - QSlider - groove - horizontal */\
QSlider#AssetManagerSliderActionQSlider::groove:horizontal { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \
                                                                stop:0 transparent, \
                                                                stop:1 %(bright_orange)s); \
                                                                height: 1px; \
                                                                margin-left: 8; \
                                                                margin-right: 8; \
} \
\
\
/* AssetManagerSliderAction - QSlider - handle - horizontal */\
QSlider#AssetManagerSliderActionQSlider::handle:horizontal { background: %(bright_grey)s; \
                                                                width: 20px; \
} \
\
\
/* AssetManagerSliderAction - QLCDNumber */\
QLCDNumber#AssetManagerSliderActionQLCDNumber { background: transparent; \
                                                color: %(bright_orange)s; \
                                                border: none; \
} \
\
\
\
\
\
\
/* AssetManagerPreExportDialog */\
AssetManagerPreExportDialog { background-color: transparent; \
                                font-size: 14pt; \
                                color: red; \
                                border-left: none; \
                                border-top: 1px solid %(bright_orange)s; \
                                border-bottom: none; \
                                border-right: none; \
} \
\
\
/* QLabel - lbl_question */\
QLabel#lbl_question { background-color: transparent; \
                        color: %(bright_grey)s; \
} \
\
\
/* QCheckBox - chkbx_remember_choice */\
QCheckBox#chkbx_remember_choice { background: transparent; \
                                    font-size: 14pt; \
                                    color: %(bright_grey)s; \
} \
\
\
"%ss_dict

    return str_stylesheet
