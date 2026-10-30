---
name: data-device-ribbon
description: Natural-language discovery and implementation smoke test for a Revit add-in.
model: claude-fable-5-1
runs: 1
max_turns: 80
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, WebSearch, WebFetch]
---
Create a Revit C# add-in that has its own ribbon with a single button that, when pressed, counts the number of Data Devices in the model and shows the counts in a modern-looking dialog box.

Make reasonable assumptions, state them, and create the project files in the working directory.
