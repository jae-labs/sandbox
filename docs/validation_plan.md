# AIgile Framework E2E Validation Plan

> **For verification:** This plan walks through the entire AIgile SDLC workflow, testing every skill and loop transition by building a simple command-line Todo application.

**Goal:** Test every node, feedback loop, and installed skill in the `jae-labs/skills` catalog to evaluate triggering behavior and locate potential deficiencies.

**Workflow Engine:** AIgile SDLC (Spec-first, Test-first, Verification-driven)

---

## E2E Validation Checklist

Below is the step-by-step sequence of prompts you (the user) should input, what skills/nodes are targeted, and what we should verify at each step.

### Step 1: Initial Idea & Brainstorming
* **Prompt to send:**
  ```text
  I want to build a simple command-line Todo application in Python. Let's start by brainstorming the requirements, features, and target scope. Please use the brainstorming skill to explore this idea.
  ```
* **Target Skills:** `global-rules`, `brainstorming`
* **What to verify:**
  * Did the agent activate/read `global-rules` and `brainstorming`?
  * Did the brainstorming output cover user personas, core features, and architectural options?

---

### Step 2: Stress-Testing the Design (Grill-Me)
* **Prompt to send:**
  ```text
  This todo app looks clean, but before we write any specifications, please grill me on this design. Ask me hard questions about edge cases, data persistence options, and how we handle concurrent tasks or invalid inputs. Use the grill-me skill.
  ```
* **Target Skill:** `grill-me`
* **What to verify:**
  * Did the agent initiate an interactive interview?
  * Did the questions push on design assumptions (e.g., local storage vs database, error handling, date formats)?

---

### Step 3: Requirements Triage
* **Prompt to send:**
  ```text
  Based on our alignment from the grill session, let's create a formal issue description/specification and run it through triage to define the exact acceptance criteria, scope boundaries, and out-of-scope items. Use the triage skill.
  ```
* **Target Skill:** `triage`
* **What to verify:**
  * Did the agent produce a structured, triaged specification?
  * Are acceptance criteria clear, unambiguous, and testable?

---

### Step 4: Architecture Decision (ADR)
* **Prompt to send:**
  ```text
  We need to make a decision on data storage: should we use simple JSON file storage or SQLite? Let's record this as an Architecture Decision Record (ADR) in the repository. Please generate this ADR using the appropriate architecture guidelines.
  ```
* **Target Node:** Architecture Decision Record (ADR) / Architecture Notes
* **What to verify:**
  * Did the agent create a clean ADR file in the repo (e.g., under `docs/adr/0001-todo-storage-backend.md`)?
  * Does the ADR follow standard structure (Context, Decision, Consequences)?

---

### Step 5: Writing the Implementation Plan
* **Prompt to send:**
  ```text
  Now that the architecture is decided and the spec is triaged, let's convert this into an executable implementation plan with bite-sized TDD steps. Make sure to use the writing-plans skill and save the plan.
  ```
* **Target Skill:** `writing-plans`
* **What to verify:**
  * Did the agent announce using the `writing-plans` skill?
  * Did it save the plan to `docs/superpowers/plans/`?
  * Are the plan steps detailed with exact paths, commands, code targets, and verification assertions?

---

### Step 6: Workspace Isolation (Git Worktrees)
* **Prompt to send:**
  ```text
  Let's set up an isolated workspace for this implementation branch. Please run the using-git-worktrees skill to ensure the workspace is ready.
  ```
* **Target Skill:** `using-git-worktrees`
* **What to verify:**
  * Did the agent check the current branch status and set up/recommend an isolated git branch or worktree?

---

### Step 7: Test-Driven Development (TDD)
* **Prompt to send:**
  ```text
  Let's start the implementation. Let's implement the core Todo storage model. First, write the failing test for task creation, run it to verify it fails, and then implement the minimal code to pass it using the test-driven-development skill.
  ```
* **Target Skill:** `test-driven-development`
* **What to verify:**
  * Did the agent write the test *before* writing the implementation?
  * Did the agent run the test suite and verify it failed for the expected reason?
  * Did it then implement the code and verify the test passes?

---

### Step 8: Simulating a Bug & Debugging (Systematic Debugging)
* **Prompt to send:**
  ```text
  I've added some mock code that seems to break or throw unexpected errors on empty task lists. Let's use the systematic-debugging skill to find the root cause, write a regression test, and fix it.
  ```
* **Target Skill:** `systematic-debugging`
* **What to verify:**
  * Did the agent gather facts (errors, logs, reproduce case) *before* proposing a fix?
  * Did it write a regression test?
  * Did it explain the root cause clearly?

---

### Step 9: Verification Before Completion
* **Prompt to send:**
  ```text
  The implementation is now complete. Before declaring success, please use the verification-before-completion skill to gather evidence that all acceptance criteria are met, tests pass, and no regressions exist.
  ```
* **Target Skill:** `verification-before-completion`
* **What to verify:**
  * Did the agent execute the tests and compile clear execution evidence?
  * Did it check the code against the acceptance criteria from Step 3?

---

### Step 10: Code Quality Review (Thermo-Nuclear)
* **Prompt to send:**
  ```text
  Let's run a strict code quality audit on what we just built. Use the thermo-nuclear-code-quality-review skill to check for deep modules, file size, readability, and nesting.
  ```
* **Target Skill:** `thermo-nuclear-code-quality-review`
* **What to verify:**
  * Did the agent audit file cohesion, nesting depth, and structural complexity?
  * Were specific, actionable refactoring tasks suggested?

---

### Step 11: Requesting & Receiving Code Review
* **Prompt to send:**
  ```text
  Let's request a formal code review using the requesting-code-review skill. (Wait for agent to respond, then reply with): "Here is feedback from review: 'The TodoItem serializer needs to validate that the title is not empty or pure whitespace.' Please address this using the receiving-code-review skill."
  ```
* **Target Skills:** `requesting-code-review`, `receiving-code-review`
* **What to verify:**
  * Did the agent structure the review request cleanly?
  * When receiving feedback, did the agent write tests for the feedback, fix it, and verify?

---

### Step 12: Creating the PR
* **Prompt to send:**
  ```text
  Let's create the pull request. Run the create-pr skill to generate a high-quality PR description summarizing our changes, architecture, and verification results.
  ```
* **Target Skill:** [create-pr](file:///Users/luiz1361/gh_jae-labs/skills/skills/create-pr/SKILL.md)
* **What to verify:**
  * Did the agent read the git diff?
  * Did the agent generate a structured pull request description?

---

### Step 13: Finishing the Branch
* **Prompt to send:**
  ```text
  The PR is merged! Let's clean up our workspace and decide how to integrate the completed branch work using the finishing-a-development-branch skill.
  ```
* **Target Skill:** `finishing-a-development-branch`
* **What to verify:**
  * Did the agent present options for cleanup (worktree delete, branch delete, local cleanup)?

---

### Step 14: Retrospective & Handoff
* **Prompt to send:**
  ```text
  Let's wrap up this development loop. Please summarize the retrospective of this test run and draft a session handoff document using the handoff skill.
  ```
* **Target Skill:** `handoff`
* **What to verify:**
  * Did the agent create a compact `.md` handoff summarizing accomplishments, next steps, and lessons learned?

---

## Evaluation Grid

During this walkthrough, track any deficiencies in the framework/skills using this format:

| Step | Skill / Node | Expected Behavior | Observed Behavior | Deficiency / Gap | Suggested Adjustment |
| --- | --- | --- | --- | --- | --- |
| 1 | brainstorming | Clear feature outline | | | |
| 2 | grill-me | Challenging questions | | | |
| 3 | triage | Structured issue with AC | | | |
| 4 | ADR | Written storage design decision | | | |
| 5 | writing-plans | Complete plan in `docs/` | | | |
| 6 | using-git-worktrees | Setup git worktree/branch | | | |
| 7 | TDD | Red-green-refactor loop | | | |
| 8 | systematic-debugging | Root cause analysis first | | | |
| 9 | verification-before-completion | Evidence-based completion | | | |
| 10 | thermo-nuclear-review | Strict maintainability audit | | | |
| 11 | code-review (req/rec) | Structured review & feedback loop | | | |
| 12 | create-pr | Diff-based description | | | |
| 13 | finishing-branch | Branch/worktree cleanup | | | |
| 14 | handoff | Session summary & handoff doc | | | |
