// === Clique Home Assignment Starter (Node.js) ===
// You may freely modify this file or start from scratch.

import fs from "fs";
import path from "path";

const DATA_PATH = "../data";

function loadCSV(filename) {
  const text = fs.readFileSync(path.join(DATA_PATH, filename), "utf8");
  const [headerLine, ...lines] = text.trim().split("\n");
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
