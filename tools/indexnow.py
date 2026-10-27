# -*- coding: utf-8 -*-
"""Подача адресов сайта в поисковые индексы через IndexNow.

Зачем это, а не «подождать, пока найдут». Поисковик приходит на новый
сайт тогда, когда сочтёт нужным, и ждать можно неделями. IndexNow
переворачивает порядок: мы сами говорим «вот эти адреса, заберите». Это
общий протокол, его принимают Bing, Yandex, Seznam и Naver одним
запросом, подача в любой из них расходится по остальным.

Почему это важнее, чем кажется. За поиском ChatGPT стоит индекс Bing,
за DuckDuckGo тоже. То есть попадание в Bing это не «ещё одна поисковая
система помимо Google», а условие, при котором языковая модель вообще
способна нас процитировать. Google в IndexNow не участвует, ему нужна
Search Console, и это делается руками владельца.

Про ключ. Протокол требует положить на сайт файл с ключом, чтобы
подтвердить, что адреса подаёт владелец домена. Этот файл по замыслу
открыт и читается кем угодно по известному адресу, то есть секретом он
не является: украв его, посторонний сможет только попросить поисковик
перечитать наши же страницы. Поэтому он лежит в репозитории рядом с
сайтом, иначе при следующей выкладке просто исчезнет.

Запуск:
    python3.13 tools/indexnow.py          подать все адреса из карты сайта
    python3.13 tools/indexnow.py <адрес>  подать один адрес
"""
import json, pathlib, re, secrets, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
HOST = "ispgroupgc.com"
API = "https://api.indexnow.org/indexnow"


def key():
    """Ключ берётся из файла, а если его нет, заводится один раз."""
    existing = sorted(SITE.glob("indexnow-*.txt"))
    if existing:
        return existing[0].stem.replace("indexnow-", ""), existing[0]
    k = secrets.token_hex(16)
    f = SITE / f"indexnow-{k}.txt"
    f.write_text(k)
    print(f"  заведён ключ, файл {f.name}")
    return k, f


def urls():
    sm = (SITE / "sitemap.xml").read_text()
    return re.findall(r"<loc>([^<]+)</loc>", sm)


def main():
    k, f = key()
    key_url = f"https://{HOST}/{f.name}"

    # файл с ключом обязан отдаваться, иначе подача будет отвергнута
    got = subprocess.run(["curl", "-sS", "--max-time", "25", key_url],
                         capture_output=True, text=True).stdout.strip()
    if got != k:
        print(f"  файл ключа не отдаётся по адресу {key_url}")
        print("  сначала выложи сайт, потом запусти снова")
        return 1

    lst = [sys.argv[1]] if len(sys.argv) > 1 else urls()
    body = json.dumps({"host": HOST, "key": k, "keyLocation": key_url, "urlList": lst})
    r = subprocess.run(
        ["curl", "-sS", "--max-time", "60", "-X", "POST", API,
         "-H", "Content-Type: application/json; charset=utf-8",
         "--data-binary", "@-", "-w", "\n%{http_code}"],
        input=body, capture_output=True, text=True)
    out = (r.stdout or "").strip().splitlines()
    code = out[-1] if out else "0"
    if len(out) > 1:
        print("  ответ сервиса:", " ".join(out[:-1])[:200])

    # 200 принято, 202 принято и ключ проверяется
    print(f"  подано адресов: {len(lst)}, код ответа: {code}")
    return 0 if code in ("200", "202") else 1


if __name__ == "__main__":
    sys.exit(main())
