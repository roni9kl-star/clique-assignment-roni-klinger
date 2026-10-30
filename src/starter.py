import csv
import json
from datetime import datetime, timezone
import argparse

DATA_PATH = "../data"
WARNING_DAYS = 14

# Define terminal colors and reset formatting.
RED = "\033[31m"
YELLOW = "\033[33m"
PURPLE = "\033[35m"
CYAN_BOLD = "\033[1;36m"
GREEN = "\033[32m"
RESET = "\033[0m"


def load_data():
    # Use utf-8-sig to support files with a UTF-8 byte order mark.
    with open(f"{DATA_PATH}/members.csv", encoding="utf-8-sig") as file:
        members = list(csv.DictReader(file))

    with open(f"{DATA_PATH}/last_contacts.csv", encoding="utf-8-sig") as file:
        last_contacts = list(csv.DictReader(file))

    with open(f"{DATA_PATH}/holidays.json", encoding="utf-8-sig") as file:
        holidays = json.load(file)

    return members, last_contacts, holidays


def calculate_due_members(members, last_contacts, holidays, today):
    # Return no members if the selected date is a holiday.
    if today.isoformat() in holidays:
        return []

    contacts_by_id = {}

    for contact in last_contacts:
        member_id = contact["member_id"]
        contacts_by_id[member_id] = contact

    due_members = []

    # Check each member's eligibility and priority.
    for member in members:
        preferred_channel = member["preferred_channel"].strip()

        # Skip members without a communication channel.
        if not preferred_channel:
            continue

        # Find the member's contact record
        member_id = member["member_id"]
        contact = contacts_by_id.get(member_id)

        # Use default values when no contact record exists.
        days_since_last_contact = None
        last_outcome = "No previous contact"

        # Calculate the contact gap
        if contact is not None:
            # Convert the UTC timestamp to a date.
            last_contact_date = datetime.strptime(
                contact["last_contact_utc"],
                "%Y-%m-%dT%H:%M:%SZ"
            ).date()

            # Calculate calendar days since the last contact.
            days_since_last_contact = (today - last_contact_date).days
            last_outcome = contact["outcome"]

            if days_since_last_contact < 7:
                continue

        age = int(member["age"])

        # Split risk flags and remove empty values.
        risk_flags = []

        for flag in member["risk_flags"].split(";"):
            if flag.strip():
                risk_flags.append(flag.strip())

        priority_score = 0
        priority_reasons = []

        # Three points for a recent hospital discharge.
        if "recent_discharge" in risk_flags:
            priority_score += 3
            priority_reasons.append("Recent discharge (+3)")

        # Two points for living alone.
        if "lives_alone" in risk_flags:
            priority_score += 2
            priority_reasons.append("Lives alone (+2)")

        # One point for members aged 80 or older.
        if age >= 80:
            priority_score += 1
            priority_reasons.append("Age 80+ (+1)")

        # One point for an unanswered last contact.
        if last_outcome == "no_answer":
            priority_score += 1
            priority_reasons.append("Last attempt: no answer (+1)")

        # Add a time-gap bonus only when the contact date is known.
        if days_since_last_contact is not None:
            gap_bonus = days_since_last_contact / 7
            priority_score += gap_bonus
            priority_reasons.append(
                f"Contact gap (+{gap_bonus:.2f})"
            )

        # Recommend morning for ages 80+ and afternoon otherwise.
        recommended_window = "afternoon"

        if age >= 80:
            recommended_window = "morning"

        contact_warning = ""

        if days_since_last_contact is None:
            contact_warning = "No previous contact recorded"
        elif days_since_last_contact > WARNING_DAYS:
            contact_warning = (
                f"More than {WARNING_DAYS} days without contact"
            )

        # Store the member's calculated results and display details.
        due_members.append({
            "member_id": member_id,
            "full_name": member["full_name"],
            "priority_score": priority_score,
            "recommended_window": recommended_window,
            "age": age,
            "preferred_channel": preferred_channel,
            "days_since_last_contact": days_since_last_contact,
            "last_outcome": last_outcome,
            "priority_reasons": priority_reasons,
            "contact_warning": contact_warning
        })

    # Sort by score and gap descending then ID ascending.
    due_members.sort(
        key=lambda member: (
            -member["priority_score"],
            -(
                member["days_since_last_contact"]
                if member["days_since_last_contact"] is not None
                else float("inf")
            ),
            int(member["member_id"])
        )
    )

    return due_members


# Show selected names and the number of additional eligible members.
def show_checkin_popup(selected_members, remaining_count):
    # Skip the popup when no members were selected.
    if not selected_members:
        return

    # Calculate the total number of eligible members.
    total_count = len(selected_members) + remaining_count

    # Prepare the popup introduction.
    lines = [
        f"{total_count} members need a check-in today.",
        "",
        f"Top {len(selected_members)} by priority:",
        ""
    ]

    # Add selected names in priority order.
    for position, member in enumerate(selected_members, start=1):
        lines.append(f"{position}. {member['full_name']}")

    # Mention eligible members outside the selection.
    if remaining_count > 0:
        lines.append("")
        lines.append(
            f"{remaining_count} additional members also need a check-in."
        )
        lines.append("Increase --top to display more members.")

    # Continue without a popup if tkinter is unavailable.
    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError:
        print("Popup unavailable: tkinter is not installed.")
        return

    # Keep a reference to the window for cleanup.
    root = None

    try:
        # Create and hide the main window.
        root = tk.Tk()
        root.withdraw()

        # Wait for the user to close the reminder.
        messagebox.showwarning(
            "Clique - Check-in Reminder",
            "\n".join(lines),
            parent=root
        )

    # Continue with terminal output if a window cannot open.
    except tk.TclError:
        print("Popup unavailable: no graphical display could be opened.")

    # Close the hidden window after the reminder finishes.
    finally:
        if root is not None:
            root.destroy()


# Display a bar chart of the selected priority scores.
def print_priority_graph(selected_members):
    # Skip the chart when the selection is empty.
    if not selected_members:
        return

    print("\nPRIORITY AT A GLANCE")
    print("-" * 76)

    highest_score = selected_members[0]["priority_score"]

    # Build one bar for each selected member.
    for member in selected_members:
        score = member["priority_score"]

        # Scale each bar to a maximum of 30 characters.
        if highest_score > 0:
            bar_length = round((score / highest_score) * 30)
        else:
            bar_length = 0

        # Create the bar and an optional warning marker.
        bar = "#" * bar_length
        warning_marker = ""

        if member["contact_warning"]:
            warning_marker = f"{YELLOW} *{RESET}"

        print(
            f"{member['member_id']:>3} | "
            f"{member['full_name']:<22} "
            f"{bar:<30} "
            f"{RED}{score:>6.2f}{RESET}"
            f"{warning_marker}"
        )

    # Explain the chart scale and warning marker.
    print("\nBars are relative to the highest score.")
    print(
        f"{YELLOW}*{RESET} No contact record, "
        f"or a contact gap over {WARNING_DAYS} days."
    )


# Display the selected members grouped by contact window.
def print_checkin_plan(selected_members):

    print("\nYOUR CHECK-IN PLAN")
    print("All selected members, grouped by recommended contact window.")

    # Display the morning group before the afternoon group.
    for window in ["morning", "afternoon"]:
        if window == "morning":
            window_color = GREEN
        else:
            window_color = PURPLE

        print(f"\n{window_color}{window.upper()}{RESET}")
        print("-" * 76)

        # Group members while preserving their priority order.
        members_in_window = [
            member
            for member in selected_members
            if member["recommended_window"] == window
        ]

        # Show a message when the group is empty.
        if not members_in_window:
            print("No selected members in this window.")
            continue

        # Display each member's contact details.
        for member in members_in_window:
            days = member["days_since_last_contact"]

            # Describe the contact gap or missing record.
            if days is None:
                contact_info = "No previous contact recorded"
            else:
                contact_info = f"{days} days since last contact"

            print(
                f"\n{CYAN_BOLD}{member['full_name']} "
                f"(#{member['member_id']}){RESET}"
            )

            print(
                f"  Priority: "
                f"{RED}{member['priority_score']:.2f}{RESET}"
            )

            print(
                f"  Age: {member['age']} | "
                f"Channel: {member['preferred_channel']} | "
                f"Window: {window_color}"
                f"{member['recommended_window']}{RESET}"
            )

            print(f"  Contact: {contact_info}")
            print(f"  Last outcome: {member['last_outcome']}")

            if member["contact_warning"]:
                print(
                    f"  {YELLOW}ATTENTION: "
                    f"{member['contact_warning']}{RESET}"
                )

            # Explain the factors contributing to the score.
            if member["priority_reasons"]:
                reasons = "; ".join(member["priority_reasons"])
                print(f"  Score breakdown: {reasons}")
            else:
                print("  Score breakdown: No additional priority points.")


# Display the daily summary, priority chart, and contact plan.
def print_daily_brief(results, selected_members, today, is_holiday):
    # Count eligible members outside the selection.
    remaining_count = len(results) - len(selected_members)

    # Print the report title and calculation date.
    print("\n" + "=" * 76)
    print("CLIQUE | DAILY CHECK-IN BRIEF")
    print(f"Date: {today.isoformat()} (UTC)")
    print("=" * 76)

    if is_holiday:
        print("Today is a listed holiday. No check-ins are scheduled.")
        return

    if not results:
        print("No members are due for a check-in today.")
        return

    print(
        f"Members due: {RED}{len(results)}{RESET} | "
        f"Showing: {len(selected_members)} | "
        f"Additional members due: {RED}{remaining_count}{RESET}"
    )

    # Remind the coordinator about members outside the selection.
    if remaining_count > 0:
        print(
            f"REMINDER: {RED}{remaining_count}{RESET} "
            "additional members need a check-in."
        )
        print("Increase --top to display more members.")

    print_priority_graph(selected_members)
    print_checkin_plan(selected_members)


def main():
    # Create the command-line argument parser.
    parser = argparse.ArgumentParser(
        description="Find community members due for a check-in."
    )

    # Set the number of members to display.
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of members to display (default: 5)"
    )

    # Allow a fixed date for demonstrations and testing.
    parser.add_argument(
        "--date",
        help="Use a specific UTC date in YYYY-MM-DD format"
    )

    # Allow terminal-only execution.
    parser.add_argument(
        "--no-popup",
        action="store_true",
        help="Display terminal output without opening a popup"
    )

    # Read the supplied command-line arguments.
    args = parser.parse_args()

    # Reject zero or negative selection sizes.
    if args.top < 1:
        parser.error("--top must be at least 1")

    # Use the current UTC date by default.
    today = datetime.now(timezone.utc).date()

    # Validate and use the supplied date.
    if args.date:
        try:
            today = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            parser.error(
                "--date must be a valid date in YYYY-MM-DD format"
            )

    members, last_contacts, holidays = load_data()

    # Calculate eligible members using the selected date.
    results = calculate_due_members(
        members, last_contacts, holidays, today
    )

    selected_members = results[:args.top]
    remaining_count = len(results) - len(selected_members)

    # Show the reminder unless the user disabled it.
    if not args.no_popup:
        show_checkin_popup(selected_members, remaining_count)

    is_holiday = today.isoformat() in holidays

    print_daily_brief(
        results, selected_members, today, is_holiday
    )


if __name__ == "__main__":
    main()