---
name: marketplace-publishing
description: Workflow for publishing skills and agents to the Revit-focused dotnet-skills fork. Covers adding content, updating manifests, validation, and release tagging.
---

> **Revit scope:** For Revit work, first read [revit-development](../revit-development/SKILL.md). Apply this skill only within the selected host/runtime and API-context boundaries; server examples concern companion services. Institutional preferences below remain intentional.


# Marketplace Publishing Workflow

This skill documents how to add skills and agents to this Revit-focused fork and publish releases.

## Repository Structure

```
dotnet-skills/
├── .claude-plugin/
│   ├── marketplace.json      # Marketplace catalog
│   └── plugin.json           # Plugin metadata + skill/agent registry
├── .github/workflows/
│   └── release.yml           # Release automation
├── skills/                   # Flat directories; prefixes identify topic
│   ├── revit-development/SKILL.md
│   ├── akka-best-practices/SKILL.md
│   ├── aspire-integration-testing/SKILL.md
│   ├── csharp-coding-standards/SKILL.md
│   └── ...
├── agents/
│   └── *.md                  # Agent definitions
└── scripts/
    └── validate-marketplace.sh
```

## Adding a New Skill

### Step 1: Choose a Flat Skill Name

Skills use flat directories with topic prefixes:

| Category | Purpose |
|----------|---------|
| `revit-*` | Revit API and add-in guidance |
| `akka-*` | Akka.NET actor patterns, testing, clustering |
| `aspire-*` | .NET Aspire orchestration, testing, configuration |
| `csharp-*` | C# language features, coding standards |
| `playwright-*`, `testcontainers`, `snapshot-testing` | Testing tools and frameworks |
| `marketplace-*`, `skills-index-*` | Repository maintenance |

Use an existing flat naming pattern. If a new prefix is introduced, update `scripts/generate-skill-index-snippets.sh` to classify it.

### Step 2: Create the Skill Folder

Create a flat skill folder with `SKILL.md` inside:

```
skills/<skill-name>/SKILL.md
```

Example: `skills/akka-cluster-sharding/SKILL.md`

### Step 3: Write the SKILL.md

```markdown
---
name: my-new-skill
description: Brief description of what this skill does and when to use it.
---

# My New Skill

## When to Use This Skill

Use this skill when:
- [List specific scenarios]

---

## Content

[Comprehensive guide with examples, patterns, and anti-patterns]
```

**Requirements:**
- `name` must be lowercase with hyphens (e.g., `cluster-sharding`)
- `description` should be 1-2 sentences explaining when Claude should use this skill
- Content should be 10-40KB covering the topic comprehensively
- Include concrete code examples with modern C# patterns

### Step 4: Register in plugin.json

Add the skill path to `.claude-plugin/plugin.json` in the `skills` array:

```json
{
  "skills": [
    "./skills/akka-best-practices",
    "./skills/akka-cluster-sharding"
  ]
}
```

### Step 5: Validate

Run the validation script:

```bash
./scripts/validate-marketplace.sh
./scripts/validate-codex-plugin.sh
./scripts/generate-skill-index-snippets.sh --update-readme
```

### Step 6: Commit Together

```bash
git add skills/akka-cluster-sharding/ .claude-plugin/plugin.json README.md
git commit -m "Add cluster-sharding skill for Akka.NET Cluster Sharding patterns"
```

---

## Adding a New Agent

### Step 1: Create the Agent File

Create a markdown file in `/agents/`:

```markdown
---
name: my-agent-name
description: Expert in [domain]. Specializes in [specific areas]. Use for [scenarios].
model: sonnet
color: blue
---

You are a [domain] specialist with deep expertise in [areas].

**Reference Materials:**
- [Official docs and resources]

**Core Expertise Areas:**
[List expertise areas]

**Diagnostic Approach:**
[How the agent analyzes problems]
```

**Requirements:**
- `name` must be lowercase with hyphens
- `model` must be one of: `haiku`, `sonnet`, `opus`
- `color` is optional (used for UI display)

### Step 2: Register in plugin.json

Add to the `agents` array:

```json
{
  "agents": [
    "./agents/akka-net-specialist.md",
    "./agents/my-agent-name.md"
  ]
}
```

### Step 3: Commit Together

```bash
git add agents/my-agent-name.md .claude-plugin/plugin.json
git commit -m "Add my-agent-name agent for [domain] expertise"
```

---

## Publishing a Release

### Versioning

Use the repository helper to update both plugin manifests and the Claude marketplace catalog in lockstep:

```bash
./scripts/bump-version.sh 1.9.0
```

Use semantic versioning (`MAJOR.MINOR.PATCH`):
- **MAJOR**: Breaking changes (renamed/removed skills)
- **MINOR**: New skills or agents added
- **PATCH**: Fixes or improvements to existing content

### Release Process

1. **Update all version fields in lockstep**

2. **Update `RELEASE_NOTES.md` and validate both marketplace targets**
   ```bash
   # Edit RELEASE_NOTES.md for this release.
   ./scripts/validate-marketplace.sh
   ./scripts/validate-codex-plugin.sh
   ./scripts/generate-skill-index-snippets.sh --update-readme
   ```

3. **Commit release content and version bump**
   ```bash
   git add .claude-plugin/plugin.json .claude-plugin/marketplace.json .codex-plugin/plugin.json RELEASE_NOTES.md README.md
   git commit -m "Release 1.9.0"
   ```

4. **Create and push the version tag**
   ```bash
   git tag v1.9.0
   git push origin v1.9.0
   ```

Do not push a hard-coded branch name as part of this release command. Release from the intended branch using the repository's normal branch workflow, then push the tag.

5. **GitHub Actions will automatically:**
   - Validate the marketplace structure
   - Create a GitHub release with auto-generated notes

---

## User Installation

Users install the complete plugin (all skills and agents):

```bash
# Add the marketplace (one-time)
/plugin marketplace add thewrz/revit-dotnet-skills

# Install the plugin (gets everything)
/plugin install revit-dotnet-skills

# Update to latest version
/plugin marketplace update
```

---

## Validation Checklist

Before committing:

- [ ] SKILL.md has valid YAML frontmatter with `name` and `description`
- [ ] Skill folder follows the flat naming convention
- [ ] Path added to `plugin.json` skills array
- [ ] Codex validator passes and README index snippets are regenerated
- [ ] For agents: `model` is specified (haiku/sonnet/opus)
- [ ] `./scripts/validate-marketplace.sh` passes

---

## Troubleshooting

### Skill not appearing after install

- Verify the path in plugin.json matches the folder structure
- Check that SKILL.md exists in the folder
- Try reinstalling: `/plugin uninstall revit-dotnet-skills && /plugin install revit-dotnet-skills`

### Validation errors

- Ensure JSON is valid: `jq . .claude-plugin/plugin.json`
- Check for trailing commas in arrays
- Verify all referenced folders contain SKILL.md

### Release not created

- Ensure tag follows semver format (`v1.0.0`)
- Check GitHub Actions logs for errors
- Verify plugin.json version matches the tag
