import lvgl as lv
import lv_anima

def _appear_complete_cb(pm_page, options):
    if pm_page.willAppear:
        pm_page.willAppear(pm_page.page)

def _back_appear_complete_cb(pm_page, options):
    if pm_page.didAppear:
        pm_page.didAppear(pm_page.page)

def _disAppear_complete_cb(pm_page, options):
    # todo
    if options.anima == lv_pm_open_options.LV_PM_ANIMA_NONE:
        pm_page.page.add_flag(lv.obj.FLAG.HIDDEN)
    if pm_page.willDisappear:
        pm_page.willDisappear(pm_page.page)
    if options.open_tag == lv_pm_open_options.LV_PM_TARGET_SELF:
        pm_page.unLoad(pm_page.page)
        pm_page.page.clean()

def _back_disAppear_complete_cb(pm_page, options):
    # todo
    if options.anima == lv_pm_open_options.LV_PM_ANIMA_NONE:
        pm_page.page.add_flag(lv.obj.FLAG.HIDDEN)
    if pm_page.didDisappear:
        pm_page.didDisappear(pm_page.page)
    pm_page.unLoad(pm_page.page)
    pm_page.page.clean()


class lv_pm_open_options():
    LV_PM_ANIMA_NONE = 0
    LV_PM_ANIMA_SLIDE = 1
    LV_PM_ANIMA_SLIDE_SCALE = 2
    LV_PM_ANIMA_POPUP = 3

    LV_PM_ANIMA_TOP = 0
    LV_PM_ANIMA_RIGHT = 1
    LV_PM_ANIMA_BOTTOM = 2
    LV_PM_ANIMA_LEFT = 3

    # open in new page
    LV_PM_TARGET_NEW = 0
    # replace current page
    LV_PM_TARGET_SELF = 1
    # close all page and open in new page
    LV_PM_TARGET_RESET = 2
    def __init__(self, anima=LV_PM_ANIMA_NONE, anima_dir=LV_PM_ANIMA_TOP, open_tag=LV_PM_TARGET_NEW) -> None:
        self.anima = anima
        self.anima_dir = anima_dir
        self.open_tag = open_tag 

class lv_pm_page():
    def __init__(self, onLoad, unLoad, willAppear=None, didAppear=None, willDisappear=None, didDisappear=None) -> None:
        self.page = lv.obj(lv.screen_active())
        self.page.set_style_border_width(0, lv.STATE.DEFAULT)
        self.page.set_style_radius(0, lv.STATE.DEFAULT)
        self.page.set_style_pad_all(0, lv.STATE.DEFAULT)
        self.page.add_flag(lv.obj.FLAG.HIDDEN)
        self.page.set_height(lv.screen_active().get_height())
        self.page.set_width(lv.screen_active().get_width())

        self.onLoad = onLoad
        self.willAppear = willAppear
        self.didAppear = didAppear
        self.willDisappear = willDisappear
        self.didDisappear = didDisappear
        self.unLoad = unLoad

        self.__back = False
        self.__options = None

class lv_pm():
    def __init__(self):
        self.history_len = 0
        self.history = {}
        self.router = []
        # turn off the scroll bar
        lv.screen_active().set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
    
    def add_page(self, page):
        self.router.append(page)
        return len(self.router) - 1
    
    def open_page(self, id, options):
        if (id > len(self.router) - 1) or id < 0:
            return False, "id err"
        self.history[self.history_len] = id
        pm_page = self.router[id]
        if options:
            pm_page.__options = options
        pm_page.__back = False
        if self.history_len > 0:
            prev_pm_page = self.router[self.history[self.history_len - 1]]
            prev_pm_page.__back = False
            if prev_pm_page.willDisappear:
                prev_pm_page.willDisappear(prev_pm_page.page)
            lv_anima._pm_anima_disAppear(prev_pm_page, pm_page.__options, _disAppear_complete_cb)
        pm_page.onLoad(pm_page.page)
        pm_page.page.remove_flag(lv.obj.FLAG.HIDDEN)
        if pm_page.willAppear:
            pm_page.willAppear(pm_page.page)
        lv_anima._pm_anima_appear(pm_page, pm_page.__options, _appear_complete_cb)
        if options.open_tag == lv_pm_open_options.LV_PM_TARGET_SELF:
            if self.history_len:
                self.history[self.history_len - 1] = self.history[self.history_len]
            else:
                self.history_len += 1
        else:
            self.history_len += 1
        return True
    
    def back(self):
        if self.history_len < 2:
            return False, "history_len < 2"
        pm_page = self.router[self.history[self.history_len - 1]]
        pm_page.__back = True
        if pm_page.willDisappear:
            pm_page.willDisappear(pm_page.page)

        lv_anima._pm_anima_disAppear(pm_page, pm_page.__options, _back_disAppear_complete_cb)

        self.history_len -= 1
        prev_pm_page = self.router[self.history[self.history_len - 1]]
        prev_pm_page.__back = True
        if prev_pm_page.willDisappear:
            prev_pm_page.willDisappear(prev_pm_page.page)

        prev_pm_page.page.remove_flag(lv.obj.FLAG.HIDDEN)
        lv_anima._pm_anima_appear(prev_pm_page, pm_page.__options, _back_appear_complete_cb)
        return True
