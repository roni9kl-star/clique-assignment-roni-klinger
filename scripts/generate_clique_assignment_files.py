import os
import csv
import json
import random
from datetime import datetime, timedelta
from textwrap import dedent

BASE_DIR = "clique_home_assignment"
DATA_DIR = os.path.join(BASE_DIR, "data")
SRC_DIR = os.path.join(BASE_DIR, "src")

NUM_MEMBERS = 50  # adjust if you want more or fewer mock users

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SRC_DIR, exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(dedent(content).strip() + "\n")
    print(f"✅ Created: {path}")

def generate_mock_members(n=NUM_MEMBERS):
    first_names = ["Ruth", "Sarah", "Hanna", "Miriam", "Leah", "Esther", "Rachel", "Naomi", "David", "Joseph", "Eli", "Moshe", "Aaron", "Isaac", "Daniel", "Jacob"]
    last_names = ["Cohen", "Levi", "Israel", "Adler", "Katz", "Regev", "Shapira", "Baruch", "Amar", "Rosen", "Dahan", "Mizrahi", "Peretz", "Alon", "Halevi"]
    channels = ["call", "sms", "whatsapp"]
    risk_options = ["", "lives_alone", "recent_discharge", "lives_alone;recent_discharge"]

    rows = [["member_id", "full_name", "age", "preferred_channel", "risk_flags"]]
    for i in range(1, n + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"
        age = random.randint(60, 95)
        channel = random.choice(channels)
        risk = random.choices(risk_options, weights=[0.5, 0.25, 0.15, 0.1])[0]
        rows.append([i, name, age, channel, risk])
    return rows

def generate_mock_last_contacts(members):
    outcomes = ["ok", "no_answer", "escalate"]
    rows = [["member_id", "last_contact_utc", "outcome"]]
    now = datetime.utcnow()
    for i in range(1, len(members)):
        days_ago = random.randint(0, 20)
        dt = now - timedelta(days=days_ago, hours=random.randint(0, 23))
        outcome = random.choice(outcomes)
        rows.append([i, dt.strftime("%Y-%m-%dT%H:%M:%SZ"), outcome])
    return rows

def save_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"✅ Created CSV: {path}")

def generate_data_files():
    members = generate_mock_members()
    save_csv(os.path.join(DATA_DIR, "members.csv"), members)

    last_contacts = generate_mock_last_contacts(members)
    save_csv(os.path.join(DATA_DIR, "last_contacts.csv"), last_contacts)

    holidays = [
        "2025-11-07",
        "2025-12-25",
        "2026-01-01",
        "2026-04-13"
    ]
    with open(os.path.join(DATA_DIR, "holidays.json"), "w", encoding="utf-8") as f:
        json.dump(holidays, f, indent=2)
    print(f"✅ Created JSON: {os.path.join(DATA_DIR, 'holidays.json')}")

def create_readme():
    readme = """
    # Clique – Home Assignment

    Hi 👋  
    Welcome to the home assignment for **Clique**, a platform helping elderly communities stay connected.

    Your goal is to create a small program that determines which members are *due for a check-in today* and in what order of priority.

    ---

    ## 🧩 Your Task
    You’ll find three data files in the `/data` folder:
    - `members.csv` – details of community members  
    - `last_contacts.csv` – when each member was last contacted  
    - `holidays.json` – dates when no check-ins should occur  

    Your program should:
    1. Determine which members need a new check-in.
    2. Calculate a priority score for each member.
    3. Output a sorted list of top members (to console or API response).

    ---

    ## 🧠 Notes
    - You can use any language you prefer.
    - Place your code inside `/src`.
    - Add at least 2–3 simple unit tests.
    - Make sure your program runs locally.

    ---

    ## 🧪 How to Submit
    - Push your solution to GitHub or send it as a ZIP file.  
    - Include this README updated with:
      - How to run your solution  
      - Any assumptions you made  
      - What you’d improve with more time  

    ---

    ## ❤️ Reminder
    You may use AI tools (like ChatGPT or Copilot) to help you —  
    but make sure you **understand every line of your code**.  
    We might ask you to explain or extend it in a live session.

    Have fun and good luck 🌿  
    — The Clique Team
    """
    write_file(os.path.join(BASE_DIR, "README_template.md"), readme)

def create_starters():
    starter_py = """
    import csv
    import json
    from datetime import datetime, timezone

    # === Clique Home Assignment Starter (Python) ===
    # You may freely modify this file or start from scratch.
    # The data files are located in ../data/

    DATA_PATH = "../data"

    def load_data():
        with open(f"{DATA_PATH}/members.csv") as f:
            members = list(csv.DictReader(f))
        with open(f"{DATA_PATH}/last_contacts.csv") as f:
            last_contacts = list(csv.DictReader(f))
        with open(f"{DATA_PATH}/holidays.json") as f:
            holidays = json.load(f)
        return members, last_contacts, holidays

    def calculate_due_members(members, last_contacts, holidays):
        # TODO: Implement logic from the assignment
        # 1. Determine who needs a check-in
        # 2. Compute priority_score
        # 3. Sort and return list
        return []

    def main():
        members, last_contacts, holidays = load_data()
        results = calculate_due_members(members, last_contacts, holidays)
        print("Members due for check-in:")
        for m in results:
            print(m)

    if __name__ == "__main__":
        main()
    """
    write_file(os.path.join(SRC_DIR, "starter.py"), starter_py)

    starter_js = """
    // === Clique Home Assignment Starter (Node.js) ===
    // You may freely modify this file or start from scratch.

    import fs from "fs";
    import path from "path";

    const DATA_PATH = "../data";

    function loadCSV(filename) {
      const text = fs.readFileSync(path.join(DATA_PATH, filename), "utf8");
      const [headerLine, ...lines] = text.trim().split("\\n");
      const headers = headerLine.split(",");
      return lines.map(line => {
        const values = line.split(",");
        const obj = {};
        headers.forEach((h, i) => (obj[h] = values[i]));
        return obj;
      });
    }

    function loadData() {
      const members = loadCSV("members.csv");
      const lastContacts = loadCSV("last_contacts.csv");
      const holidays = JSON.parse(fs.readFileSync(path.join(DATA_PATH, "holidays.json")));
      return { members, lastContacts, holidays };
    }

    function calculateDueMembers({ members, lastContacts, holidays }) {
      // TODO: Implement the assignment logic here
      return [];
    }

    function main() {
      const data = loadData();
      const result = calculateDueMembers(data);
      console.log("Members due for check-in:");
      console.log(result);
    }

    main();
    """
    write_file(os.path.join(SRC_DIR, "starter.js"), starter_js)

def create_gitignore():
    gitignore = """
    __pycache__/
    *.pyc
    .env
    node_modules/
    """
    write_file(os.path.join(BASE_DIR, ".gitignore"), gitignore)

def main():
    ensure_dirs()
    generate_data_files()
    create_readme()
    create_starters()
    create_gitignore()
    print("\n🎉 All assignment files successfully generated in 'clique_home_assignment/'")

if __name__ == "__main__":
    main()
