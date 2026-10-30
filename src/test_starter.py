import unittest
from datetime import date

from starter import calculate_due_members


class CheckinTests(unittest.TestCase):

    # Check the priority score and recommended contact window.
    def test_priority_score(self):

        # Create a member with all priority factors.
        member = {
            "member_id": "1",
            "full_name": "Ruth Cohen",
            "age": "85",
            "preferred_channel": "call",
            "risk_flags": "lives_alone;recent_discharge"
        }

        # Set an unanswered contact from 14 days ago.
        contact = {
            "member_id": "1",
            "last_contact_utc": "2025-10-23T08:00:00Z",
            "outcome": "no_answer"
        }

        # Calculate the results for a fixed date.
        results = calculate_due_members(
            [member], [contact], [], date(2025, 11, 6)
        )

        # Verify
        self.assertEqual(len(results), 1)
        self.assertAlmostEqual(results[0]["priority_score"], 9)
        self.assertEqual(results[0]["recommended_window"], "morning")

    # Check that no members are returned on a holiday.
    def test_holiday(self):

        # Create a member who would otherwise qualify.
        member = {
            "member_id": "1",
            "full_name": "Ruth Cohen",
            "age": "85",
            "preferred_channel": "call",
            "risk_flags": ""
        }

        # Calculate the results with today listed as a holiday.
        results = calculate_due_members(
            [member], [], ["2025-11-06"], date(2025, 11, 6)
        )

        # Verify
        self.assertEqual(results, [])

    # Check that a member without a contact record is included.
    def test_missing_contact(self):

        # Create a member under 80 with no risk flags.
        member = {
            "member_id": "1",
            "full_name": "Joseph Levi",
            "age": "70",
            "preferred_channel": "sms",
            "risk_flags": ""
        }

        # Calculate the results without any contact records.
        results = calculate_due_members(
            [member], [], [], date(2025, 11, 6)
        )

        # Verify
        self.assertEqual(len(results), 1)
        self.assertIsNone(results[0]["days_since_last_contact"])
        self.assertEqual(results[0]["priority_score"], 0)
        self.assertEqual(results[0]["recommended_window"], "afternoon")

    # Check that a longer contact gap wins a tie at the top-five boundary.
    def test_tie_at_top_five(self):

        # Prepare empty member and contact lists.
        members = []
        contacts = []

        # Create four high-priority members to fill the first four places.
        for member_id in range(1, 5):
            members.append({
                "member_id": str(member_id),
                "full_name": f"Member {member_id}",
                "age": "85",
                "preferred_channel": "call",
                "risk_flags": "recent_discharge"
            })

            # Give each member a contact record from 14 days ago.
            contacts.append({
                "member_id": str(member_id),
                "last_contact_utc": "2025-10-23T08:00:00Z",
                "outcome": "ok"
            })

        # Create member 5 with an age bonus of one point.
        members.append({
            "member_id": "5",
            "full_name": "Shorter Gap",
            "age": "85",
            "preferred_channel": "call",
            "risk_flags": ""
        })

        # Add a seven day gap, giving member 5 a total score of two.
        contacts.append({
            "member_id": "5",
            "last_contact_utc": "2025-10-30T08:00:00Z",
            "outcome": "ok"
        })

        # Create member 6 without age or risk bonuses.
        members.append({
            "member_id": "6",
            "full_name": "Longer Gap",
            "age": "70",
            "preferred_channel": "sms",
            "risk_flags": ""
        })

        # Add a fourteen-day gap, giving member 6 the same score of two.
        contacts.append({
            "member_id": "6",
            "last_contact_utc": "2025-10-23T08:00:00Z",
            "outcome": "ok"
        })

        # Calculate and sort all eligible members.
        results = calculate_due_members(
            members, contacts, [], date(2025, 11, 6)
        )

        top_five = results[:5]

        # Verify
        self.assertEqual(results[4]["priority_score"], 2)
        self.assertEqual(results[5]["priority_score"], 2)
        self.assertEqual(top_five[4]["member_id"], "6")
        self.assertEqual(results[5]["member_id"], "5")


# Run the tests when this file is executed directly.
if __name__ == "__main__":
    unittest.main()