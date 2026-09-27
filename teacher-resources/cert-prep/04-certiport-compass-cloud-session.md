---
title: 4. Run a Compass Cloud Session
parent: Certification Test Prep
grandparent: Teacher Resources
nav_order: 4
---

# Run a Compass Cloud Testing Session
{: .no_toc }

Compass Cloud delivers Certiport exams through a lockdown desktop app on student machines, controlled by a proctor dashboard in your browser. A session has four phases: **create** it days ahead, **confirm** it the day before, **start and unlock** on exam day, then **close out**. Missing the confirm step is the most common way to lose a session.
{: .fs-5 .fw-300 }

<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## Before you start

{: .warning }
> Compass Cloud In-Center is for in-person testing at your CATC only. It is not a remote proctoring solution. Certiport retired the older EFH delivery on August 31, 2026, so Compass Cloud is now the path for classroom testing.

### Proctor role

- On your Certiport account: **My Profile → Roles → Become a Proctor**, then accept the Proctor Agreement.
- Your Organization Administrator associates you with the CATC with the **Proctor** box checked.
- Only a proctor selected on the session can confirm and start it. Once one proctor starts the session, it belongs to that proctor; nobody else can join it.

### Lab machines (talk to IT two weeks out)

| Requirement | Detail |
|:------------|:-------|
| Operating system | Windows 10/11, macOS Sonoma 14.x or later, or current ChromeOS |
| App | Compass Cloud desktop app installed on **every** testing machine. Installing needs local admin rights or managed-device deployment. |
| Hardware | Full keyboard, 2-button mouse, monitor at least 1280 × 800 |
| Bandwidth | At least 10 Mbps download **per workstation**. A 26-seat lab needs roughly 260 Mbps free during the session. |
| Browser | Chrome, Edge, or Safari present on the machine |

Download the installer: log in at certiport.com as Organization Administrator or Member, hover **Exam Delivery**, and select **Compass Cloud: Download & Installation** (Windows, Mac, or Chromebook).

### Proctor machine

A laptop or desktop at **1920 × 1080** or higher, in Chrome (Edge and Safari also work). The dashboard is dense; a small screen hides columns.

---

## Phase 1: Create the session (days ahead)

Sessions must be created at least 60 minutes before start. Create them 2 to 7 days ahead so vouchers and access codes are settled before the day.

1. Log in at **www.certiport.com**.
2. Switch role to **Proctor** or **Organization Administrator**.
3. Open session creation:
   - **Organization Administrator/Member:** hover **Exam Delivery** and select **Compass Cloud (In-Center & Remote): Create Session**.
   - **Proctor:** select **Compass Cloud – In classroom proctoring**, then **Create and manage exam sessions**.

<div class="uim">
  <div class="uim-browser">
    <div class="uim-bar"><div class="uim-dots"><span></span><span></span><span></span></div><div class="uim-url">certiport.com</div></div>
    <div class="uim-top certiport"><span>Certiport</span><span class="uim-user">Role: Organization Administrator <span class="uim-pin">2</span></span></div>
    <div class="uim-nav"><span>My Certiport</span><span>Org Profile</span><span class="on">Exam Delivery</span><span>Exam Groups</span><span>Vouchers</span></div>
    <div class="uim-main">
      <div class="uim-menu">
        <div class="uim-hl">Compass Cloud (In-Center &amp; Remote): Create Session <span class="uim-pin">3</span></div>
        <div>Compass Cloud: Download &amp; Installation</div>
        <div class="uim-dim">…</div>
      </div>
    </div>
  </div>
  <p class="uim-caption">Representation of the Exam Delivery menu for the Organization Administrator role. The calendar tool opens in a new tab.</p>
</div>

{: start="4"}
4. In the calendar tool, select **Create New Session**.
5. Fill in the session form:

| Field | Recommendation |
|:------|:---------------|
| **Session name** | `P3 Photoshop 2026-12-08` |
| **Select your CATC** | Your school |
| **Payment method** | **Center assigned voucher** for a class; see [Guide 3, Part C]({% link teacher-resources/cert-prep/03-certiport-register-students.md %}#part-c-vouchers) |
| **Exam group number** | Optional. The number from your Exam Group. |
| **Exam language** | English |
| **Exam Administrators (Proctors)** | Yourself, plus a backup proctor |
| **Date / Time** | Class start time. Toggle 12/24-hour if needed. |

6. Select **Next**. Choose up to **5** exam titles and enter the number of candidates for each (up to **50** total).
7. Select **Next**, check the review screen, and select **Submit**.

<div class="uim">
  <div class="uim-browser">
    <div class="uim-bar"><div class="uim-dots"><span></span><span></span><span></span></div><div class="uim-url">Compass Cloud · Create session</div></div>
    <div class="uim-top certiport"><span>Create New Session</span><span class="uim-user">Details · Exams · Review</span></div>
    <div class="uim-main">
      <div class="uim-grid2">
        <div class="uim-field"><label>Session name <span class="uim-pin">5</span></label><div class="uim-input">P3 Photoshop 2026-12-08</div></div>
        <div class="uim-field"><label>Select your CATC</label><div class="uim-input select">Your High School</div></div>
        <div class="uim-field"><label>Payment method</label><div class="uim-input select uim-hl">Center assigned voucher</div></div>
        <div class="uim-field"><label>Exam group number (optional)</label><div class="uim-input ph">000000</div></div>
        <div class="uim-field"><label>Exam language</label><div class="uim-input select">English</div></div>
        <div class="uim-field"><label>Exam Administrators (Proctors)</label><div class="uim-input select">Teacher, M.; Backup, A.</div></div>
      </div>
      <div class="uim-field"><label>Date / Time</label><div class="uim-row" style="margin:0"><div class="uim-input">Dec 8, 2026</div><div class="uim-input">9:40 AM</div><span class="uim-tag gray">12h / 24h</span></div></div>
      <div class="uim-card" style="margin:6px 0 10px">
        <div style="font-weight:600;margin-bottom:6px">Exam titles <span class="uim-pin">6</span> <span class="uim-dim" style="font-weight:400">(up to 5 titles · 50 candidates total)</span></div>
        <table class="uim-table">
          <tr><th></th><th>Exam title</th><th>Candidates</th></tr>
          <tr><td><span class="uim-check on" style="margin:0"></span></td><td>Visual Design using Adobe Photoshop</td><td><div class="uim-input" style="width:60px">24</div></td></tr>
          <tr><td><span class="uim-check" style="margin:0"></span></td><td>Graphic Design &amp; Illustration using Adobe Illustrator</td><td><div class="uim-input ph" style="width:60px">0</div></td></tr>
        </table>
      </div>
      <div class="uim-row uim-spread"><span class="uim-btn ghost">Back</span><span><span class="uim-pin">7</span><span class="uim-btn cp uim-hl">Submit</span></span></div>
    </div>
  </div>
  <p class="uim-caption">The real form spreads these fields across three screens (details, exams, review). Collapsed here into one drawing.</p>
</div>

{: .warning }
> **Read before you select Submit.**
> - Payment is taken the moment the session is created.
> - CATC, payment method, exam language, and exam titles **cannot be edited**. To change one, delete the session and create a new one.
> - You can change the number of candidates up to 1 hour before start.
> - You can cancel up to 1 hour before start. After that, the session is locked.

{: start="8"}
8. Watch for the confirmation email. It contains the **Access Codes**: one code per exam title. Every student taking the same exam uses the same code. Print them or put them on a slide you will show only at launch.

---

## Phase 2: Confirm the session (within 24 hours of start)

A new session shows an orange **Confirmation required** label. An unconfirmed session **cancels automatically 1 hour before start**. Sessions created fewer than 2 hours ahead confirm automatically.

{: start="9"}
9. The day before, log in at **www.certiport.com** and open the calendar tool.
10. Find the session in the upcoming list and select **Confirm session**.
11. The label turns green: **Confirmed**. A confirmation email follows.

<div class="uim">
  <div class="uim-browser">
    <div class="uim-bar"><div class="uim-dots"><span></span><span></span><span></span></div><div class="uim-url">Compass Cloud · Calendar</div></div>
    <div class="uim-top certiport"><span>Upcoming sessions</span><span class="uim-user"><span class="uim-btn">Create New Session</span></span></div>
    <div class="uim-main">
      <div class="uim-card" style="margin-bottom:10px">
        <div class="uim-row uim-spread" style="margin:0">
          <div><div style="font-weight:700">P3 Photoshop 2026-12-08</div><div class="uim-cap">Tue Dec 8 · 9:40 AM · 24 candidates</div></div>
          <div class="uim-row" style="margin:0"><span class="uim-tag orange">Confirmation required</span><span class="uim-btn cp uim-hl">Confirm session</span><span class="uim-pin">10</span><span class="uim-btn ghost">⋯</span></div>
        </div>
      </div>
      <div class="uim-card">
        <div class="uim-row uim-spread" style="margin:0">
          <div><div style="font-weight:700">P5 Premiere Pro 2026-12-09</div><div class="uim-cap">Wed Dec 9 · 12:15 PM · 19 candidates</div></div>
          <div class="uim-row" style="margin:0"><span class="uim-tag green">Confirmed</span><span class="uim-pin">11</span><span class="uim-btn cp disabled">Start session</span><span class="uim-btn ghost">⋯</span></div>
        </div>
      </div>
    </div>
  </div>
  <p class="uim-caption"><strong>Start session</strong> stays gray until 5 minutes before the scheduled time. The ⋯ menu holds cancel and <strong>Resume session</strong>.</p>
</div>

{: .important }
> Put a calendar reminder for the confirm step on your phone when you create the session. This is the step people forget.

---

## Phase 3: Exam day

### Timing rules

| Window | What happens |
|:-------|:-------------|
| 5 minutes before start | **Start session** becomes clickable. |
| Up to 15 minutes after start | Last chance to start the session. After that, it cannot launch. |
| 30 minutes after start | Candidates who have not started are locked out. |
| About 2 hours | Total session time for Adobe (Live-in-the-Application) exams. The exam itself runs 45 to 60 minutes. |

### Students seated (10 minutes before)

Students log in to the lab machine but do **not** open the Compass Cloud app yet. Hand out or display each student's username if they need it. Check consent forms at the door.

### Start the session

{: start="12"}
12. Log in at **www.certiport.com**, open the calendar tool, and select **Start session** on your session. The administration dashboard opens in a new tab.
13. Show the **Access Code** for the exam.

### Students launch the app

{: start="14"}
14. Students double-click the **Compass Cloud** icon. The machine locks down immediately: no Alt-Tab, no other programs. Until the exam launches, a student can still leave with **Close Window**.
15. Students enter their Certiport **username** and **password**, type the **Access Code**, and select **Continue**.
16. Students check the verification screen (name and exam title) and select **Next**. They land in the lobby and show up on your dashboard as **Unlock requested**.

<div class="uim">
  <div class="uim-window">
    <div class="uim-bar"><span class="uim-title">Compass Cloud</span><span class="uim-lock">LOCKDOWN</span></div>
    <div class="uim-main">
      <div class="uim-narrow uim-card">
        <div class="uim-h uim-center">Sign in</div>
        <div class="uim-field"><label>Certiport username <span class="uim-pin">15</span></label><div class="uim-input">jordan.rivera@example.com</div></div>
        <div class="uim-field"><label>Password</label><div class="uim-input ph">••••••••••••</div></div>
        <div class="uim-field"><label>Access Code</label><div class="uim-input uim-code uim-hl">XXXX-XXXX</div></div>
        <div class="uim-row uim-spread"><span class="uim-btn ghost">Close Window</span><span class="uim-btn cp">Continue</span></div>
      </div>
    </div>
  </div>
  <p class="uim-caption">Representation of the candidate app. It opens full screen; this drawing shows it windowed.</p>
</div>

<div class="uim">
  <div class="uim-window">
    <div class="uim-bar"><span class="uim-title">Compass Cloud</span><span class="uim-lock">LOCKDOWN</span></div>
    <div class="uim-main uim-center">
      <div class="uim-h">Lobby</div>
      <div class="uim-sub">Jordan Rivera · Visual Design using Adobe Photoshop</div>
      <div class="uim-banner" style="display:inline-block">Waiting for your Exam Administrator to unlock your exam</div>
      <div><span class="uim-btn cp disabled">Start exam</span></div>
      <p class="uim-dim" style="margin-top:8px;font-size:11px">Button turns active after the proctor selects Unlock (step 17).</p>
    </div>
  </div>
</div>

### Unlock candidates

{: start="17"}
17. On the dashboard, check each **Unlock requested** row against the student in the seat. Then either:
    - select the **three dots** at the end of a row and choose **Unlock**, or
    - select the **Unlock all** message at the top once the whole room is in the lobby.
18. Students select **Start exam**, accept the agreements, and work through the tutorial and exam.

<div class="uim">
  <div class="uim-browser">
    <div class="uim-bar"><div class="uim-dots"><span></span><span></span><span></span></div><div class="uim-url">Compass Cloud · Administration dashboard</div></div>
    <div class="uim-top certiport"><span>P3 Photoshop 2026-12-08</span><span class="uim-user"><span class="uim-btn">Need Help?</span></span></div>
    <div class="uim-main">
      <div class="uim-banner uim-row uim-spread" style="margin-bottom:10px"><span>3 candidates are waiting in the lobby.</span><span><span class="uim-link uim-hl">Unlock all</span><span class="uim-pin">17</span></span></div>
      <div class="uim-sub" style="font-weight:600;color:#1f2933">Visual Design using Adobe Photoshop</div>
      <table class="uim-table">
        <tr><th>Status</th><th>Name</th><th>Exam</th><th>Options</th></tr>
        <tr><td><span class="uim-tag orange">Unlock requested</span></td><td>Rivera, Jordan</td><td>Photoshop</td><td style="position:relative"><span class="uim-btn uim-hl">⋯</span>
          <div class="uim-menu" style="position:absolute;right:0;top:30px;z-index:2;text-align:left"><div><strong>Unlock</strong></div><div>Restart session</div></div></td></tr>
        <tr><td><span class="uim-tag orange">Unlock requested</span></td><td>Nguyen, Sam</td><td>Photoshop</td><td><span class="uim-btn">⋯</span></td></tr>
        <tr><td><span class="uim-tag blue">In progress</span></td><td>Okafor, Ada</td><td>Photoshop</td><td><span class="uim-btn">⋯</span></td></tr>
        <tr><td><span class="uim-tag green">Exam complete</span></td><td>Patel, Ravi</td><td>Photoshop</td><td><span class="uim-btn">⋯</span></td></tr>
      </table>
    </div>
  </div>
  <p class="uim-caption">Statuses shown are the ones named in Certiport's guide plus the obvious in-between state. Your dashboard may use slightly different labels.</p>
</div>

### During the exam

- Stay on the dashboard. Statuses update as students progress.
- **Frozen Adobe exam:** Adobe exams run in a virtual machine. If one hangs, select the **three dots** on that student's row, then **Restart session**.
- Once an exam begins, the student cannot exit until they finish or time runs out.
- **Need Help?** on the dashboard opens Certiport live chat.

---

## Phase 4: Close out

{: start="19"}
19. Students select **Finish the exam**, give optional feedback, and see their **Score Report** and **Exam Score Summary**. They select **End Exam Session** to leave the app.
20. When every row shows **Exam complete**, end the session (Certiport may show a short survey).
21. Return to the calendar, select your name in the top right, and select **Log out**.

Students can find results later under **My Certiport → My Transcript** (uncheck **Show Only Passed Exams** to see all attempts, then select **Score Report**).

---

## Exam-day checklist

Print this and tape it next to the proctor machine.

| Done | Item |
|:----:|:-----|
| ☐ | Session shows **Confirmed** (checked the day before) |
| ☐ | Access Code email printed or on a hidden slide |
| ☐ | Proctor laptop charged, Chrome open, logged in to certiport.com |
| ☐ | Consent forms collected for every student under 18 |
| ☐ | Username list at hand (from Guide 3, Part A4) |
| ☐ | Compass Cloud app icon present on every lab machine |
| ☐ | Students seated 10 minutes early; app **not** opened yet |
| ☐ | **Start session** selected between 5 minutes before and 15 minutes after start |
| ☐ | Every row matched to a face before **Unlock all** |
| ☐ | All rows **Exam complete** before ending the session |

## Troubleshooting

| Symptom | Fix |
|:--------|:----|
| Closed the dashboard tab by accident | Press **Ctrl+Shift+T** (Windows) or **Cmd+Shift+T** (Mac). If that fails: calendar → session's **three dots** → **Resume session**. |
| **Start session** is gray | Too early (opens 5 minutes before) or too late (closes 15 minutes after). |
| Session disappeared from the calendar | It was not confirmed and auto-cancelled 1 hour before start. Create a new one; it needs 60 minutes lead time. |
| Backup proctor cannot open the session | Only the proctor who selects **Start session** can run it. A backup has to be listed under Exam Administrators when the session is created, and has to be the one who starts it. |
| Student sees the wrong exam on the verification screen | Use **Change exam** if another title in this session fits; otherwise stop and fix before unlocking. |
| Student forgot password | Recovery needs username + secret question. Do it on a separate device; the lab machine is locked down. |
| Adobe exam frozen | Dashboard → student's **three dots** → **Restart session**. |
