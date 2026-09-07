// Fully automatic, wall-clock-driven class schedule timer.
//
// No start/stop button: BellTimer.computeState() is a pure function of
// (schedule, phases, now) that derives the current period/phase from the
// system clock alone, so the display is always correct on load, after a
// refresh, or after an overnight reboot with no user interaction.
//
// computeState() has no DOM or browser dependency on purpose — it's the
// piece meant to be reused as-is (or ported) by a future LED-array
// controller (e.g. an NTP-synced ESP32/Raspberry Pi reading the same
// _data/bell_schedule.yml + _data/lesson_phases.yml) so the physical
// display and this page never drift out of sync with each other.
(function (global) {
  function parseHM(hm) {
    var parts = hm.split(':');
    return parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
  }

  function minutesOfDay(date) {
    return date.getHours() * 60 + date.getMinutes() + date.getSeconds() / 60 + date.getMilliseconds() / 60000;
  }

  // schedule: array of { id, name, start: "HH:MM", end: "HH:MM", type: "block"|"plain" }
  // phases: array of { id, name, minutes } applied in order to type:"block" periods
  function computeState(schedule, phases, now) {
    var nowMin = minutesOfDay(now);
    var periods = schedule.map(function (p) {
      return {
        id: p.id,
        name: p.name,
        type: p.type,
        startMin: parseHM(p.start),
        endMin: parseHM(p.end)
      };
    });

    var phaseMinutes = phases.reduce(function (sum, ph) { return sum + ph.minutes; }, 0);

    var active = null;
    for (var i = 0; i < periods.length; i++) {
      if (nowMin >= periods[i].startMin && nowMin < periods[i].endMin) {
        active = periods[i];
        break;
      }
    }

    if (!active) {
      var next = null;
      for (var j = 0; j < periods.length; j++) {
        if (periods[j].startMin > nowMin) { next = periods[j]; break; }
      }
      return {
        status: next ? 'passing' : 'after_school',
        period: null,
        phase: null,
        nextPeriod: next ? { id: next.id, name: next.name, start: next.startMin } : null,
        secondsUntilNext: next ? Math.round((next.startMin - nowMin) * 60) : null,
        secondsLeftInPeriod: null,
        phaseIndex: -1,
        phaseCount: phases.length
      };
    }

    var elapsed = nowMin - active.startMin;
    var secondsLeftInPeriod = Math.round((active.endMin - nowMin) * 60);

    if (active.type !== 'block') {
      return {
        status: 'period',
        period: { id: active.id, name: active.name, type: active.type },
        phase: null,
        nextPeriod: null,
        secondsUntilNext: null,
        secondsLeftInPeriod: secondsLeftInPeriod,
        phaseIndex: -1,
        phaseCount: 0
      };
    }

    // Walk the phase boundaries to find which one "elapsed" minutes falls in.
    var cursor = 0;
    var matched = null;
    var matchedIndex = -1;
    for (var k = 0; k < phases.length; k++) {
      var phaseStart = cursor;
      var phaseEnd = cursor + phases[k].minutes;
      if (elapsed < phaseEnd) {
        matched = { id: phases[k].id, name: phases[k].name, minutes: phases[k].minutes };
        matchedIndex = k;
        var secondsLeftInPhase = Math.round((phaseEnd - elapsed) * 60);
        return {
          status: 'period',
          period: { id: active.id, name: active.name, type: active.type },
          phase: matched,
          secondsLeftInPhase: secondsLeftInPhase,
          nextPeriod: null,
          secondsUntilNext: null,
          secondsLeftInPeriod: secondsLeftInPeriod,
          phaseIndex: matchedIndex,
          phaseCount: phases.length
        };
      }
      cursor = phaseEnd;
    }

    // Past the last scripted phase (e.g. bell rings later than the 78-min
    // plan calls for) but still inside the period: show a buffer state
    // instead of pretending a phase is still running.
    return {
      status: 'period',
      period: { id: active.id, name: active.name, type: active.type },
      phase: null,
      secondsLeftInPhase: 0,
      nextPeriod: null,
      secondsUntilNext: null,
      secondsLeftInPeriod: secondsLeftInPeriod,
      phaseIndex: phases.length,
      phaseCount: phases.length,
      buffer: true
    };
  }

  global.BellTimer = {
    computeState: computeState,
    parseHM: parseHM,
    minutesOfDay: minutesOfDay
  };
})(typeof window !== 'undefined' ? window : globalThis);
