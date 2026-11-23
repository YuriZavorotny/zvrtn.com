# Исходники zvrtn.com

Папка с подчёркиванием: GitHub Pages (Jekyll) её не публикует.

## Сборка сайта

```
cd _src
python3 build.py .. index.html
```

Пишет готовые HTML-файлы прямо в корень репозитория (index, about, contact, case-*.html).
Ассеты (big/, img/, og/, v/, фавиконки) лежат в корне репо и генератором не трогаются.

- `build.py` — генератор: CSS, разметка, скрипты, тексты кейсов. CSS внутри %-форматируемой строки: литеральный % пишется как %%.
- `content_src.py` — исходная разметка и тексты, которые build.py дорабатывает.
- `home_gl.src.js` — WebGL-слой (видео на главной и в шапках кейсов, искажение при прокрутке).
- `scramble.src.js` — эффект перебора букв в подписях.

Проверка после сборки: `git diff --stat` должен показывать только то, что меняли.

## Ролики-прототипы (proto/)

Кликабельный прототип из скриншотов: экраны, хотспоты с ховером, курсор, клик-рипл, рендер покадрово.

```
cd _src/proto
python3 -m http.server 8765 &          # плеер грузит конфиги и картинки отсюда
node render5.js az3                     # кадры в fr_az3/
ffmpeg -framerate 30 -i fr_az3/%05d.jpg -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p -movflags +faststart out.mp4
```

- `player3.html?cfg=<name>.json` — плеер. Конфиг: img (префикс файлов в img/), h (высота экрана), start, screens, hs (хотспоты: s экран, id, box [x0,y0,x1,y1,radius], to экран, hov картинка ховера, plain без серого ховера, sb для сайдбара), steps (["click"|"hover", id]), cur0 (стартовая позиция курсора), endHold.
- `render5.js` — актуальный рендер (Azure, az3.json). `render3.js` — им сняты ролики Sweed (sec1..sec5.json).
- `img/` — экраны в 2000 px: sweed-NN, azure-NN (azure-02c/02f/02h/01h — производные).
- `orig/` — исходные скриншоты Azure до правок. `fix_meta2.py`, `tbl.py`, `unchk.py` делают из них отредактированные экраны (тексты набираются шрифтом Selawik из fonts/, вспомогательные функции в `retitle.py`).
- Готовые ролики кладутся в корень репо в v/ (mp4 + jpg-постер из первого кадра).
