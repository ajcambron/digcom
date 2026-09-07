// Renders BellTimer.computeState() output to the DOM. Kept separate from
// bell-timer.js so the schedule math stays portable (no DOM assumptions)
// for reuse by a future LED-array controller.
(function () {
  var PHASE_COLORS = ['#3b82f6', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444'];

  function pad2(n) { return n < 10 ? '0' + n : '' + n; }

  function formatClock(totalSeconds) {
    var s = Math.max(0, totalSeconds);
    var m = Math.floor(s / 60);
    var sec = Math.floor(s % 60);
    return pad2(m) + ':' + pad2(sec);
  }

  function unlockAudio() {
    if (window.__bellAudioCtx) return window.__bellAudioCtx;
    var Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return null;
    window.__bellAudioCtx = new Ctx();
    return window.__bellAudioCtx;
  }

  function chime() {
    var ctx = window.__bellAudioCtx;
    if (!ctx) return;
    var osc = ctx.createOscillator();
    var gain = ctx.createGain();
    osc.frequency.value = 880;
    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.6);
  }

  document.addEventListener('click', unlockAudio, { once: true });
  document.addEventListener('keydown', unlockAudio, { once: true });

  function render(schedule, phases) {
    var els = {
      periodName: document.getElementById('period-name'),
      phaseName: document.getElementById('phase-name'),
      clock: document.getElementById('clock'),
      sub: document.getElementById('sub-label'),
      strip: document.getElementById('phase-strip'),
      stage: document.getElementById('stage')
    };

    var lastKey = null;

    function tick() {
      var state = window.BellTimer.computeState(schedule, phases, new Date());
      var key = state.status + ':' + (state.period ? state.period.id : '') + ':' + state.phaseIndex;

      if (state.status === 'after_school') {
        els.periodName.textContent = 'School Day Complete';
        els.phaseName.textContent = '';
        els.clock.textContent = '--:--';
        els.sub.textContent = '';
        els.strip.innerHTML = '';
        els.stage.style.background = '#111827';
      } else if (state.status === 'passing') {
        els.periodName.textContent = 'Passing Time';
        els.phaseName.textContent = 'Next: ' + state.nextPeriod.name;
        els.clock.textContent = formatClock(state.secondsUntilNext);
        els.sub.textContent = 'until ' + state.nextPeriod.name + ' begins';
        els.strip.innerHTML = '';
        els.stage.style.background = '#1f2937';
      } else {
        els.periodName.textContent = state.period.name;
        els.stage.style.background = '#0b1220';

        if (state.period.type === 'block' && !state.buffer) {
          els.phaseName.textContent = state.phase.name;
          els.clock.textContent = formatClock(state.secondsLeftInPhase);
          els.sub.textContent = 'remaining in this phase · ' + formatClock(state.secondsLeftInPeriod) + ' left in ' + state.period.name;

          els.strip.innerHTML = '';
          phases.forEach(function (ph, idx) {
            var seg = document.createElement('div');
            seg.className = 'phase-seg';
            seg.style.flex = ph.minutes;
            seg.style.background = idx < state.phaseIndex ? '#374151' : (idx === state.phaseIndex ? PHASE_COLORS[idx % PHASE_COLORS.length] : '#1f2937');
            seg.title = ph.name;
            els.strip.appendChild(seg);
          });
        } else if (state.period.type === 'block' && state.buffer) {
          els.phaseName.textContent = 'Wrap-up buffer';
          els.clock.textContent = formatClock(state.secondsLeftInPeriod);
          els.sub.textContent = 'all scripted phases complete · bell rings soon';
          els.strip.innerHTML = '';
        } else {
          els.phaseName.textContent = '';
          els.clock.textContent = formatClock(state.secondsLeftInPeriod);
          els.sub.textContent = 'remaining in ' + state.period.name;
          els.strip.innerHTML = '';
        }
      }

      if (lastKey !== null && lastKey !== key) {
        chime();
      }
      lastKey = key;
    }

    tick();
    setInterval(tick, 1000);
  }

  window.BellTimerDisplay = { render: render };
})();
