# lv_pm_mpy

**[lvgl-pm](https://github.com/LanFly/lvgl-pm)** 的 micropython 版本

一个适用于 micropython LVGL 的页面管理器

## 使用示例

```python
import lv_pm

opt = lv_pm.lv_pm_open_options(lv_pm.lv_pm_open_options.LV_PM_ANIMA_SLIDE)
page1 = lv_pm.lv_pm_page(page_page1_onLoad, page_page1_unLoad)
page2 = lv_pm.lv_pm_page(page_page2_onLoad, page_page2_unLoad)

pm = lv_pm.lv_pm()
pm.add_page(page1)
pm.add_page(page2)

pm.open_page(1, opt)
```

## 编写页面

```python

def page_page1_onLoad(page):
  print("lifecycle: page1 onLoad")
  page.set_style_bg_color(lv.color_make(237, 175, 5), lv.STATE.DEFAULT)
  label = lv.label(page)
  label.set_text("hello page1")
  label.center()

def page_page1_unLoad(page):
  print("lifecycle: page1 unLoad")
```
