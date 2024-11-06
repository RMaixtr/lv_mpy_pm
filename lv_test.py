
import lvgl as lv
from lv_utils import event_loop

def page_page1_onLoad(page):
  print("lifecycle: page1 onLoad")
  page.set_style_bg_color(lv.color_make(237, 175, 5), lv.STATE.DEFAULT)
  label = lv.label(page)
  label.set_text("hello page1")
  label.center()

def page_page1_unLoad(page):
  print("lifecycle: page1 unLoad")

def page_page2_onLoad(page):
  print("lifecycle: page2 onLoad")
  page.set_style_bg_color(lv.color_make(150, 199, 4), lv.STATE.DEFAULT)
  label = lv.label(page)
  label.set_text("hello page2")
  label.center()

def page_page2_unLoad(page):
  print("lifecycle: page2 unLoad")


lv.init()
event_loop = event_loop()
disp = lv.linux_fbdev_create()
lv.linux_fbdev_set_file(disp, "/dev/fb0")

import lv_pm
opt = lv_pm.lv_pm_open_options(lv_pm.lv_pm_open_options.LV_PM_ANIMA_SLIDE) # 
page1 = lv_pm.lv_pm_page(page_page1_onLoad, page_page1_unLoad)
page2 = lv_pm.lv_pm_page(page_page2_onLoad, page_page2_unLoad)

pm = lv_pm.lv_pm()
print(pm.add_page(page1))
print(pm.add_page(page2))

pm.open_page(0, opt)

openflag = False
import time
while True:

    time.sleep_ms(1000)
    if openflag:
        print('back', pm.back())
        openflag = False
    else:
        pm.open_page(1, opt)
        openflag = True