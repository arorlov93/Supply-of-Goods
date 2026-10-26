# -*- coding: utf-8 -*-
"""Версионирование имён файлов изображений.

Задача. В site/_headers для /media/* стоит
`Cache-Control: public, max-age=31536000, immutable`, то есть «храни год и
не перепроверяй». Это правильная настройка для статики, но она верна
только при одном условии: имя файла меняется вместе с содержимым. У нас
имена переиспользовались, кадр заменялся под тем же pallets-wall.webp, и у
всех, кто заходил раньше, в браузере на год оставалась прежняя картинка.
Снаружи это выглядит как «ты не заменил фотографию», хотя на сервере лежит
новая.

Решение обычное: в имя добавляется восемь знаков хэша содержимого,
pallets-wall.a1b2c3d4.webp. Меняется кадр - меняется адрес, кэш
промахивается и браузер берёт новый файл сам. При этом год хранения
остаётся честным.

Запуск: python3.13 tools/media-version.py
Повторный запуск пересчитывает хэши и правит ссылки, старые версии удаляет.
"""
import hashlib, pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MEDIA = SITE / "media"
# уже версионированное имя: basename.<8 знаков>.ext
VERSIONED = re.compile(r"^(.+)\.[0-9a-f]{8}$")


def short(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def base_name(stem):
    m = VERSIONED.match(stem)
    return m.group(1) if m else stem


def main():
    # 1. свести к базовым именам: снять прежние версии
    for f in sorted(MEDIA.iterdir()):
        if f.suffix.lower() not in (".jpg", ".webp"):
            continue
        b = base_name(f.stem)
        if b != f.stem:
            target = f.with_name(b + f.suffix)
            if target.exists():
                f.unlink()          # дубль прежней версии
            else:
                f.rename(target)

    # 2. посчитать хэши и переименовать
    mapping = {}
    for f in sorted(MEDIA.iterdir()):
        if f.suffix.lower() not in (".jpg", ".webp"):
            continue
        h = short(f)
        new = f.with_name(f"{f.stem}.{h}{f.suffix}")
        f.rename(new)
        mapping[f"media/{f.name}"] = f"media/{new.name}"

    # 3. переписать ссылки на страницах
    pages = 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()
        # сначала снять прежние версии, иначе хэш налипнет на хэш
        s = re.sub(r"(media/[A-Za-z0-9_-]+)\.[0-9a-f]{8}(\.(?:jpg|webp))", r"\1\2", s)
        for old, new in mapping.items():
            s = s.replace(old, new)
        if s != s0:
            p.write_text(s)
            pages += 1

    # 4. титры ссылаются на имена файлов, их тоже привести в порядок
    cred = MEDIA / "CREDITS.json"
    if cred.exists():
        t = cred.read_text()
        t = re.sub(r'"([A-Za-z0-9_-]+)\.[0-9a-f]{8}\.jpg"', r'"\1.jpg"', t)
        cred.write_text(t)

    print(f"файлов версионировано: {len(mapping)}, страниц обновлено: {pages}")


if __name__ == "__main__":
    main()
