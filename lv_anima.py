import lv_pm
import lvgl as lv
import uctypes

POPUP_TOP_HEIGHT = 15


# I strongly advise against using user_data argument in Micropython for that purpose.
# user_data is used internally by the Micropython Bindings.
# You should keep the user_data argument as None in 99% of the cases.
# anima_datas = {}

appear_anima = lv.anim_t()
disAppear_anima = lv.anim_t()


class lv_pm_anima_data():
    def __init__(self, page, cb, options):
        self.page = page
        self.cb = cb
        self.options = options

def anima_ready_cb(anima_data: lv_pm_anima_data):
    anima_data.cb(anima_data.page, anima_data.options)

# ----------------------------------------------------------------------------------------------------------
# slide animation
# ----------------------------------------------------------------------------------------------------------

def _pm_slide_appear(anima_data: lv_pm_anima_data):
    width = lv.screen_active().get_width()
    appear_anima.init()
    appear_anima.set_var(anima_data.page.page)

    if anima_data.page.__back:
        appear_anima.set_values(-width, 0)
    else:
        appear_anima.set_values(width, 0)

    appear_anima.set_path_cb(lv.anim_t.path_ease_out)
    appear_anima.set_time(500)
    appear_anima.set_repeat_count(1)
    appear_anima.set_custom_exec_cb(lambda a,val: anima_data.page.page.set_x(val))
    appear_anima.set_start_cb(lambda a: anima_ready_cb(anima_data))
    appear_anima.start()

def _pm_slide_disAppear(anima_data: lv_pm_anima_data):
    width = lv.screen_active().get_width()
    disAppear_anima.init()
    disAppear_anima.set_var(anima_data.page.page)

    if anima_data.page.__back:
        disAppear_anima.set_values(0, width)
    else:
        disAppear_anima.set_values(0, -width)

    disAppear_anima.set_time(500)
    disAppear_anima.set_repeat_count(1)
    disAppear_anima.set_custom_exec_cb(lambda a,val: anima_data.page.page.set_x(val))
    disAppear_anima.set_start_cb(lambda a: anima_ready_cb(anima_data))
    disAppear_anima.set_path_cb(lv.anim_t.path_ease_out)
    disAppear_anima.start()

# ----------------------------------------------------------------------------------------------------------
#   popup animation
# ----------------------------------------------------------------------------------------------------------
def _pm_popup_appear(anima_data: lv_pm_anima_data):
    height = lv.screen_active().get_height()
    appear_anima.init()
    appear_anima.set_var(anima_data.page.page)

    if anima_data.page.__back:
        appear_anima.set_values(5, 0)
        anima_data.page.page.set_style_radius(0, lv.STATE.DEFAULT)
    else:
        appear_anima.set_values(height, POPUP_TOP_HEIGHT)
        anima_data.page.page.set_style_radius(10, lv.STATE.DEFAULT)

    appear_anima.set_path_cb(lv.anim_t.path_ease_out)
    appear_anima.set_time(500)
    appear_anima.set_repeat_count(1)
    appear_anima.set_custom_exec_cb(lambda a,val: anima_data.page.page.set_y(val))
    appear_anima.set_start_cb(lambda a: anima_ready_cb(anima_data))
    appear_anima.start()

def _pm_popup_disAppear(anima_data: lv_pm_anima_data):
    height = lv.screen_active().get_height()
    disAppear_anima.init()
    disAppear_anima.set_var(anima_data.page.page)

    if anima_data.page.__back:
        disAppear_anima.set_values(POPUP_TOP_HEIGHT, height)
        anima_data.page.page.set_style_radius(0, lv.STATE.DEFAULT)
    else:
        disAppear_anima.set_values(0, 5)
        anima_data.page.page.set_style_radius(10, lv.STATE.DEFAULT)

    disAppear_anima.set_time(500)
    disAppear_anima.set_repeat_count(1)
    disAppear_anima.set_custom_exec_cb(lambda a,val: anima_data.page.page.set_y(val))
    disAppear_anima.set_start_cb(lambda a: anima_ready_cb(anima_data))
    disAppear_anima.set_path_cb(lv.anim_t.path_ease_out)
    disAppear_anima.start()

# ----------------------------------------------------------------------------------------------------------
#   fade animation
# ----------------------------------------------------------------------------------------------------------

def _pm_fade_in(anima_data: lv_pm_anima_data):
    appear_anima.init() 
    appear_anima.set_var(anima_data.page.page)

    appear_anima.set_values(lv.OPA.TRANSP, lv.OPA.COVER)

    appear_anima.set_time(1000)
    appear_anima.set_repeat_count(1)
    appear_anima.set_path_cb(lv.anim_t.path_ease_out)
    appear_anima.set_custom_exec_cb(lambda a,val: anima_data.page.page.set_style_opa(val, lv.STATE.DEFAULT))
    appear_anima.set_start_cb(lambda a: anima_ready_cb(anima_data))
    appear_anima.start()

def _pm_fade_out(anima_data: lv_pm_anima_data):
    disAppear_anima.init()
    disAppear_anima.set_var(anima_data.page.page)

    disAppear_anima.set_values(lv.OPA.COVER, lv.OPA.TRANSP)

    disAppear_anima.set_time(1000)
    disAppear_anima.set_repeat_count(1)
    disAppear_anima.set_custom_exec_cb(lambda a,val: anima_data.page.page.set_style_opa(val, lv.STATE.DEFAULT))
    disAppear_anima.set_start_cb(lambda a: anima_ready_cb(anima_data))
    disAppear_anima.set_path_cb(lv.anim_t.path_ease_out)
    disAppear_anima.start()

def _pm_anima_appear(pm_page, behavior, cb):
    if (not behavior) or behavior.anima == lv_pm.lv_pm_open_options.LV_PM_ANIMA_NONE:
        cb(pm_page, behavior)
        return True
    
    anima_data = lv_pm_anima_data(pm_page, cb, behavior)
    if behavior.anima == lv_pm.lv_pm_open_options.LV_PM_ANIMA_SLIDE:
        _pm_slide_appear(anima_data)
    elif behavior.anima == lv_pm.lv_pm_open_options.LV_PM_ANIMA_FADE:
        _pm_fade_in(anima_data)
    elif behavior.anima == lv_pm.lv_pm_open_options.LV_PM_ANIMA_POPUP:
        _pm_popup_appear(anima_data)
    else:
        cb(pm_page, behavior)

def _pm_anima_disAppear(pm_page, behavior, cb):
    if (not behavior) or behavior.anima == lv_pm.lv_pm_open_options.LV_PM_ANIMA_NONE:
        cb(pm_page, behavior)
        return True
    anima_data = lv_pm_anima_data(pm_page, cb, behavior)

    if behavior.anima == lv_pm.lv_pm_open_options.LV_PM_ANIMA_SLIDE:
        _pm_slide_disAppear(anima_data)
    elif behavior.anima == lv_pm.lv_pm_open_options.LV_PM_ANIMA_FADE:
        _pm_fade_out(anima_data)
    elif behavior.anima == lv_pm.lv_pm_open_options.LV_PM_ANIMA_POPUP:
        _pm_popup_disAppear(anima_data)
    else:
        cb(pm_page, behavior)


