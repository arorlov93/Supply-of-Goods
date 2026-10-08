# -*- coding: utf-8 -*-
"""Числовая полоса под героем. Конкуренты выносят объёмы (Interra: 4 300 товаров,
45 стран, 112 назначений). Мы выносим то, что посетитель может проверить кликом,
и ни одной придуманной цифры."""

EN = """
<section id="numbers">
  <div class="wrap">
    <span class="eyebrow">In numbers</span>
    <div class="lede">
      <h2>Everything here is checkable on this site</h2>
      <p class="intro">We do not publish tonnage or client names we cannot evidence. Each
        figure below links to the pages it is counted from, so you can verify it yourself
        before you write to us.</p>
    </div>
    <div class="nums">
      <div class="num"><b>20</b><span>Years of<br><a href="experience.html">supply work</a></span></div>
      <div class="num"><b>4</b><span><a href="corridors.html">Corridors</a><br>run end to end</span></div>
      <div class="num"><b>14</b><span>Gateway ports<br><a href="corridors.html">on those lanes</a></span></div>
      <div class="num"><b>6</b><span><a href="supply.html">Categories</a><br>supplied</span></div>
      <div class="num"><b>3</b><span>Verified producers<br>per enquiry</span></div>
    </div>
  </div>
</section>
"""

FR = """
<section id="numbers">
  <div class="wrap">
    <span class="eyebrow">En chiffres</span>
    <div class="lede">
      <h2>Tout ce qui suit est v&eacute;rifiable sur ce site</h2>
      <p class="intro">Nous ne publions ni tonnages ni noms de clients que nous ne pouvons
        pas prouver. Chaque chiffre renvoie aux pages d&rsquo;o&ugrave; il est compt&eacute;.</p>
    </div>
    <div class="nums">
      <div class="num"><b>20</b><span>Ans<br>d&rsquo;exp&eacute;rience</span></div>
      <div class="num"><b>4</b><span>Lignes exploit&eacute;es<br>de bout en bout</span></div>
      <div class="num"><b>14</b><span>Ports<br>sur ces lignes</span></div>
      <div class="num"><b>6</b><span>Cat&eacute;gories<br>fournies</span></div>
      <div class="num"><b>3</b><span>Producteurs v&eacute;rifi&eacute;s<br>par demande</span></div>
    </div>
  </div>
</section>
"""


def inject(path, block, css=None):
    s = open(path, encoding="utf-8").read()
    if 'id="numbers"' in s:
        import re
        s = re.sub(r'\n<section id="numbers">.*?</section>\n', "\n", s, flags=re.S)
    s = s.replace("</header>\n\n<main>", "</header>\n\n<main>\n" + block.strip() + "\n", 1)
    if css and ".nums{" not in s:
        i = s.rindex("</style>")
        s = s[:i] + css + s[i:]
    open(path, "w", encoding="utf-8").write(s)
