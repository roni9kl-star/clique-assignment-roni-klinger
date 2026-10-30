# My Solution — Clique Daily Check-in

A Python command line tool that identifies members who need a check-in and displays a reminder popup, a priority chart, and a daily contact plan.

## How to Run

Open a terminal in the project folder and enter the `src` directory:

```bash
cd src
```

Display the top five members:

```bash
python starter.py --top 5
```

Close the reminder popup to view the detailed report in the terminal.

To demonstrate the program with a date suitable for the supplied data:

```bash
python starter.py --top 5 --date 2025-11-06
```

To run without the popup:

```bash
python starter.py --top 5 --no-popup
```

The popup requires tkinter and a graphical desktop. If it is unavailable, the terminal report is still displayed.

All commands must be run from `src`.


## Run Tests

```bash
python -m unittest test_starter.py -v
```


---



## Assumptions

- I counted days using UTC dates, without taking the contact time into account.
- If a member has no contact record, I included them but did not add points for the contact gap.
- I assumed each member has only one contact record and that it is their latest one.
- I assumed the input files are valid and member IDs are unique numbers.
- If two members have the same score, I put the one with the longer contact gap first. A member with no contact record comes first in a tie. If there is still a tie, I use the smaller member ID.
- I show only the requested number of members, even if there is a tie at the cutoff.




## What I Would Improve With More Time

- With more contact history, I would look at each member's usual contact pattern. For someone usually contacted daily, a three-day gap could deserve attention even before seven days have passed.
I would add this as a separate alert without changing the assignment's seven day rule.
The current data includes only the latest contact, so there is not enough information to identify a pattern.
- Add clearer error messages for missing files or invalid data.
- Allow the program to run from any folder, without having to enter `src`.





# Clique — Home Assignment for Internship Candidates

## Welcome!

Hi there,

Thank you for applying to join Clique — a social-tech startup building tools that help elderly communities stay connected and make it easier for coordinators and volunteers to manage communication and care.

We're not testing how much you already know — we're looking for curious, proactive people who enjoy exploring problems and finding simple, thoughtful solutions.

You're welcome to use AI tools (like ChatGPT, Copilot, etc.) if they help you learn or speed things up — but please make sure you understand every line of your code and can explain your reasoning. During the next stage, we might ask you to modify or extend your own code live, so being familiar with your solution is essential.

Keep it clean, creative, and clear — we care more about your thinking than perfection.

Have fun and show us how you approach challenges 🌿

---

## The Goal

Build a simple web-based or command-line tool that helps community coordinators see which members might need a check-in today.

You can use any programming language or framework you're comfortable with — Python, JavaScript, TypeScript, Java, etc.

**You have up to 2 hours to work on it and 48 hours to submit your results.**

---

## The Data

You'll receive three small files:

### `members.csv`

```csv
member_id,full_name,age,preferred_channel,risk_flags
1,Ruth Cohen,82,call,lives_alone
2,Joseph Levi,76,sms,
3,Sarah Adler,90,whatsapp,lives_alone;recent_discharge
4,Danny Israel,68,call,
```

### `last_contacts.csv`

```csv
member_id,last_contact_utc,outcome
1,2025-10-30T08:00:00Z,ok
2,2025-10-28T17:00:00Z,no_answer
3,2025-10-27T09:00:00Z,escalate
4,2025-10-20T10:00:00Z,ok
```

### `holidays.json`

```json
["2025-11-07", "2025-12-25"]
```

---

## The Task

Create a small program that determines which members are "due for a check-in" today, and in what order of priority.

### 1. Who qualifies for a check-in?

A member should appear in the list if:

- They haven't been contacted for at least 7 days (or have no record yet).
- Today is not a holiday (based on `holidays.json`).
- Their preferred communication channel exists.

### 2. Priority score

For each member, calculate a `priority_score`:

- **+3** if they have `recent_discharge`
- **+2** if they have `lives_alone`
- **+1** if age ≥ 80
- **+1** if their last contact outcome was `no_answer`
- **+** `days_since_last_contact / 7` (a fractional bonus for longer gaps)

Then, sort descending by priority score.

### 3. Output

Print or return a list of the top members who need attention today, showing:

- `member_id`
- `full_name`
- `priority_score`
- `recommended_window`

**Example output:**

```
member_id  full_name      priority_score  recommended_window
3          Sarah Adler    7.8             morning
2          Joseph Levi    5.1             afternoon
```

**Hint:** for members aged 80+, recommend `"morning"`, otherwise `"afternoon"`.

### 4. Interface

Choose one of the following:

**Command-line version:**
```bash
checkin --top 5
```

**Web/API version:**
```
GET /due?top=5
```

Either version is fine — keep it simple.

---

## Minimum Requirements

- ✅ Code that runs and produces the expected output.
- ✅ At least 2–3 basic test cases, including one edge case (e.g., holiday or missing last contact).
- ✅ A short README file that explains:
  - How to run your solution.
  - What assumptions you made.
  - What you would improve if you had more time.

---

## Submission

Please send a GitHub link or a ZIP file with your code and README.

- **Estimated time:** up to 2 hours.
- **Submission deadline:** within 48 hours of receiving this task.

---

## Tips

- Focus on clarity and reasoning — not fancy libraries.
- Use clear variable names and comments to explain your logic.
- If something is unclear, make a reasonable assumption and note it in the README.
- Bonus points for small, thoughtful touches (like readable output formatting).

---

## Getting Started

This repository includes starter files in both Python and JavaScript to help you get started. You can find them in the `src/` directory:

- `src/starter.py` — Python starter template
- `src/starter.js` — Node.js starter template

Feel free to modify these files or start from scratch — whatever works best for you!

The data files can be found in the `data/` directory. You may need to generate the CSV files using the provided script, or create sample data based on the examples above.

---

## Good Luck! 🍀

**The Clique Team**  
*Connecting communities. Empowering people.*

