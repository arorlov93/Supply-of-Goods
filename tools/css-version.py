# -*- coding: utf-8 -*-
"""Версионирование имени таблицы стилей.

Зачем. Снимки у нас давно версионные: media/name.a1b2c3d4.webp, и для
/media/* стоит кэш на год immutable. С таблицей стилей так не сделали, и
она подключалась простым /css/formwork.css. Cloudflare отдаёт её с
max-age=14400, то есть четыре часа браузер показывает прежнюю копию и
даже не спрашивает сервер, изменилась ли она.

Чем это обернулось. Я поправил в стилях липкое оглавление, выложил,
проверил инструментом и отчитался, что готово. У владельца на телефоне
блок продолжал висеть: его браузер четыре часа держал прежний файл.
Проверка инструментом этого не видит, он каждый раз ходит с пустым
кэшем. То есть ошибка была не в правке, а в том, что правка до человека
не доезжала, и отчёт «починено» был неверным.

Как чинится. Имя файла меняется вместе с содержимым, как у снимков.
Новое содержимое - новый адрес - кэш промахивается и браузер берёт файл
сам, сколько бы ни стояло в max-age. Заодно в _headers для /css/* можно
ставить честный год: имя гарантирует свежесть.

Почему копия, а не переименование. У снимков исходник не нужен, а стили
правятся руками, и удобно, когда файл всегда лежит по одному и тому же
имени. Поэтому site/css/formwork.css остаётся источником, рядом кладётся
formwork.<хэш>.css, страницы ссылаются на него, прежние хэшированные
копии удаляются.

Запуск: python3.13 tools/css-version.py
Повторный запуск при неизменных стилях ничего не делает.
"""
import hashlib, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CSSDIR = SITE / "css"
BASE = "formwork"

LINK = re.compile(r'href="/css/%s(?:\.[0-9a-f]{8})?\.css"' % BASE)


def main():
    src = CSSDIR / f"{BASE}.css"
    if not src.is_file():
        print("нет", src)
        return 1

    h = hashlib.sha256(src.read_bytes()).hexdigest()[:8]
    target = CSSDIR / f"{BASE}.{h}.css"
    if not target.exists():
        shutil.copy2(src, target)

    # прежние версии убираем: на них уже никто не сошлётся, а лежать они
    # будут вечно, потому что кэш для /css/* теперь годовой
    for f in CSSDIR.glob(f"{BASE}.*.css"):
        if f.name != target.name and re.fullmatch(rf"{BASE}\.[0-9a-f]{{8}}\.css", f.name):
            f.unlink()

    new = 'href="/css/%s.%s.css"' % (BASE, h)
    pages = 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        t = LINK.sub(new, s)
        if t != s:
            p.write_text(t)
            pages += 1

    print(f"  стили: {target.name}, страниц обновлено: {pages}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
