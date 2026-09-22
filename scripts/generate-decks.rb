#!/usr/bin/env ruby
# encoding: UTF-8
# Generates a reveal.js deck for a lesson from its front matter + vocab includes,
# matching the visual system in assets/css/revealjs-decks.css (1000x562 canvas,
# slide-dark/slide-light sections, eyebrow/big-title/subtitle/card/footer-tag).
# Usage: ruby scripts/generate-decks.rb path/to/lesson.md [path/to/lesson2.md ...]

require 'yaml'
require 'date'

ROOT = File.expand_path('..', __dir__)

def front_matter(path)
  text = File.read(path, encoding: 'UTF-8')
  return nil unless text.start_with?('---')
  parts = text.split(/^---\s*$/, 3)
  YAML.safe_load(parts[1], permitted_classes: [Date, Time])
end

def vocab_terms(vocab_files)
  terms = []
  vocab_files.each do |vf|
    path = File.join(ROOT, '_includes', vf)
    next unless File.exist?(path)
    File.read(path).scan(/\*\*(.+?)\*\*/).each { |m| terms << m[0] }
  end
  terms.uniq.first(8)
end

def h(str)
  str.to_s.gsub('&', '&amp;').gsub('<', '&lt;').gsub('>', '&gt;').gsub('"', '&quot;')
end

def build_deck(md_path)
  fm = front_matter(md_path)
  return unless fm && fm['lesson']
  l = fm['lesson']
  course = l['course']
  unit = l['unit']
  number = l['number']
  title = fm['title'].to_s.sub(/^[^|]+\|\s*/, '').sub(/\s*\(Teacher\)$/, '')
  target = (l.dig('the_seven', 'target') || '').to_s
  connection = (l.dig('the_seven', 'connection') || '').to_s
  standard = l['standard'].to_s
  vocab = vocab_terms(l['vocab'] || [])
  out_path = File.join(ROOT, 'assets', 'presentations', "#{course.downcase}#{unit}-#{number.to_s.split('.').last}.html")

  eyebrow = "#{course} #{number} &middot; #{course == 'FDD' ? 'FOUNDATIONS' : 'APPLICATIONS'} OF DIGITAL DESIGN"
  target_sentence = target.empty? ? title : target[0].upcase + target[1..]

  vocab_cards = vocab.map { |t| "    <div class=\"word-card\">#{h(t)}</div>" }.join("\n")

  slides = []

  slides << <<~SLIDE
    <section class="slide-dark">
    <div class="eyebrow">#{eyebrow}</div>
    <h1 class="big-title">#{h(title)}</h1>
    <div class="subtitle">#{h(connection.empty? ? "Today's lesson" : connection.split('.').first + '.')}</div>
    <div class="footer-tag">#{course} #{number}</div>
    <aside class="notes">Welcome. Hold up today's guided notes handout if one exists.</aside>
    </section>
  SLIDE

  unless vocab.empty?
    slides << <<~SLIDE
      <section class="slide-light">
      <div class="eyebrow">GET READY</div>
      <h2 class="big-title">Today's Key Terms</h2>
      <div class="subtitle">Keep these visible. We'll use every one of them today.</div>
      <div class="word-grid">
      #{vocab_cards}
      </div>
      <div class="footer-tag">#{course} #{number} &middot; Key Terms</div>
      <aside class="notes">Read the key terms aloud together before starting Direct Instruction.</aside>
      </section>
    SLIDE
  end

  slides << <<~SLIDE
    <section class="slide-light">
    <div class="eyebrow"><span class="num-badge">1</span>TARGET FOR TODAY</div>
    <h2 class="big-title">What You'll Be Able To Do</h2>
    <div class="card">#{h(target_sentence)}</div>
    <div class="footer-tag">#{course} #{number} &middot; Target</div>
    <aside class="notes">State today's target plainly before Direct Instruction begins.</aside>
    </section>
  SLIDE

  slides << <<~SLIDE
    <section class="slide-light">
    <div class="eyebrow">STANDARD</div>
    <h2 class="big-title">Where This Fits</h2>
    <div class="card">#{h(standard)}</div>
    <div class="footer-tag">#{course} #{number} &middot; Standard</div>
    <aside class="notes">Optional: note which ACP domain or enrichment goal this lesson supports.</aside>
    </section>
  SLIDE

  slides << <<~SLIDE
    <section class="slide-dark">
    <div class="eyebrow">NOW DISCUSS</div>
    <h2 class="big-title">Turn &amp; Talk</h2>
    <div class="card" style="background: var(--navy-deep); border-color: var(--ice); color: var(--white);">#{h(target_sentence)} What's the trickiest part of that, and why?</div>
    <div class="subtitle">Think &rarr; Pair &rarr; Share &middot; 2 minutes</div>
    <div class="footer-tag">#{course} #{number} &middot; Wrap-Up</div>
    <aside class="notes">Think-Pair-Share, 90 seconds, cold-call 2-3 pairs.</aside>
    </section>
  SLIDE

  html = <<~HTML
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>#{h(course)} #{h(number)} Deck</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/assets/lib/revealjs/dist/reveal.css">
    <link rel="stylesheet" href="/assets/css/revealjs-decks.css">
    </head>
    <body>
    <div class="reveal">
     <div class="slides">
    #{slides.join("\n")}
     </div>
    </div>
    <script src="/assets/lib/revealjs/dist/reveal.js"></script>
    <script src="/assets/js/revealjs-deck-common.js"></script>
    <script>
     Reveal.initialize({
      hash: true,
      controls: true,
      progress: true,
      center: true,
      transition: 'fade',
      width: 1000,
      height: 562,
      margin: 0.06
     });
    </script>
    </body>
    </html>
  HTML

  File.write(out_path, html)
  puts "Wrote #{out_path}"
end

ARGV.each { |p| build_deck(p) }
