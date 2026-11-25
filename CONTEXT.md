# Tyxuan AI

A knowledge base for a footwear factory, plus agents that use it to do each department's daily work. The first agent turns a customer's tech pack into a reviewed sample development schedule.

## Language

### Development workflow

**TP**:
The tech pack a customer sends to request a sample: drawings, materials, construction and the dates they want. Mostly PDF, sometimes Excel, and the layout differs per customer.
_Avoid_: spec, sample request, brief

**Tracking list**:
The per-season Excel sheet where the factory tracks every sample through its nodes. One sheet per sampling round, one row per SR#.
_Avoid_: tracker, status sheet

**Sampling round**:
One pass of making and shipping samples for a season, such as 1st Proto, 2nd Proto or EC sample. Round names belong to the customer.
_Avoid_: stage, phase (phase means a road-map phase here)

**SR#**:
The sample request number that identifies one model and colourway within a sampling round.

**Node**:
One dated step a sample passes through, from TP date to sample shipping date (pullover confirm, material ETA, cutting die, jigs, cutting, stitching, assembling, packing).
_Avoid_: milestone, step, task

**Common node**:
The factory's own name for a node, shared across customers. Each customer's node names map onto common nodes.

**Tech level**:
The factory's code for how new a shoe is, and the main driver of how long it takes: TN (totally new), TN+ (totally new with a new last), NU (new upper), NU+ (new upper with a new last), NU- (minor upper change), NG (new graphic), NP (new process), ND (new cutting die), NM (new material), NC (new colour).
_Avoid_: complexity, difficulty

**Pullover**:
A trial upper pulled over the last to confirm pattern and fit before samples are made. It can take several rounds.

**Last**:
The foot-shaped form a shoe is built on (楦頭). A new or revised last adds lead time.

**Sample room**:
The workshop that makes samples (樣品室). Its **loading** is how much work is already queued there.

### Scheduling

**Schedule draft**:
The agent's proposed dates for every node of one TP, with a risk level, reason and buffer source per node. It has no effect until a reviewer signs it off.
_Avoid_: plan, timeline

**Requested date**:
The date the customer asks for in the TP.

**Gap**:
The number of days the forward-computed finish falls after the requested date, with the node that causes it.

**Buffer**:
Days added to a node because of a named risk. Every buffer records the rule or statistic it came from.
_Avoid_: padding, contingency

**Review edit**:
A change a reviewer makes to a schedule draft, recorded with a reason picked from a fixed list.

**Backtest**:
Running the schedule engine on a past TP and comparing its dates with what the tracking list shows actually happened.

### Knowledge base

**Knowledge base**:
The three stores every agent reads: the structured store, the document store and the rule base.

**Structured store**:
Historical projects, node duration statistics, and data synced read-only from the ERP (line schedule, sample room loading, material lead times).

**Document store**:
Customer standards, technical documents and interview notes, retrieved by search.

**Rule base**:
Versioned, human-approved scheduling rules: standard durations per tech level and buffers per risk.

### Agents

**Specialist agent**:
An agent with one job, such as scheduling or knowledge Q&A. Users can talk to it directly.
_Avoid_: bot (in prose), skill

**Orchestrator**:
The agent that splits a cross-department request among specialist agents (總指揮). Not built until there are three or more specialists.
_Avoid_: master bot, coordinator

**Customer A / Customer B**:
Aliases for the first and second customers onboarded. Real customer names never appear in this repo.
