{%- comment -%}
  Standard stinger block for every lesson page. Stinger questions change every year and live only
  in each course's stinger deck, so lesson pages never write a stinger out; they point to the deck.
  Usage: {% include lesson-parts/stinger.md %}
{%- endcomment -%}
{%- assign stinger_course = page.lesson.course | default: "" -%}
{%- if stinger_course contains "ADD" -%}{%- assign stinger_deck = "/applications/add0/bellringers.html" -%}
{%- elsif stinger_course contains "PDD" -%}{%- assign stinger_deck = "/processes/pdd0/bellringers.html" -%}
{%- else -%}{%- assign stinger_deck = "/foundations/fdd0/bellringers.html" -%}{%- endif -%}
Answer today's stinger from the [stinger deck]({{ stinger_deck | relative_url }}) on your **Stinger
Response Sheet**: rewrite the question in your own words, answer it in at least 3 sentences, share
with a neighbor, copy their answer, then write 1–2 sentences on what your answers had in common.
