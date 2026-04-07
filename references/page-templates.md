# Page Templates

Reference templates for each wiki page type. The LLM should follow these structures when creating new pages.

---

## Source Summary Page

```markdown
---
title: "Source Title"
type: source
created: YYYY-MM-DD
updated: YYYY-MM-DD
original_url: "https://..."
author: "Author Name"
published: YYYY-MM-DD
sources: []
tags: [tag1, tag2]
---

# Source Title

> **Author**: Author Name | **Published**: YYYY-MM-DD | **Source**: [link](url)

## Summary

2-3 paragraph summary of the key content.

## Key Takeaways

- Takeaway 1
- Takeaway 2
- Takeaway 3

## Entities Mentioned

- [[Entity 1]] — role/relevance in this source
- [[Entity 2]] — role/relevance in this source

## Concepts Covered

- [[Concept 1]] — how it's discussed
- [[Concept 2]] — how it's discussed

## Notable Claims

> "Direct quote or key claim" (p.X / section Y)

Assessment: supported / contested / novel

## Connections

- Supports [[other-page]] on point X
- Contradicts [[other-page]] regarding Y
- Extends [[other-page]] by adding Z
```

---

## Entity Page

```markdown
---
title: "Entity Name"
type: entity
entity_type: person | organization | product | dataset | model
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [source1, source2]
tags: [tag1, tag2]
---

# Entity Name

> One-line description of what/who this entity is.

## Overview

2-3 paragraph overview synthesizing all known information.

## Key Facts

| Attribute | Value |
|-----------|-------|
| Type | person/org/product |
| Founded/Born | date |
| Affiliation | org |
| Website | url |

## Role in Knowledge Base

How this entity connects to the main research topics.

## Timeline

- **YYYY-MM-DD**: Event 1
- **YYYY-MM-DD**: Event 2

## Related

- [[Related Entity 1]]
- [[Related Concept 1]]

## Sources

- [[source-summary-1]] — what this source says about the entity
- [[source-summary-2]] — what this source says
```

---

## Concept Page

```markdown
---
title: "Concept Name"
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [source1, source2]
tags: [tag1, tag2]
---

# Concept Name

> One-line definition.

## Definition

Clear, precise definition of the concept.

## Context

Why this concept matters in the context of this knowledge base.

## Key Aspects

### Aspect 1
Detail...

### Aspect 2
Detail...

## Examples

- Example 1 from [[source-x]]
- Example 2 from [[source-y]]

## Tradeoffs / Debates

- Proponents argue X ([[source-a]])
- Critics argue Y ([[source-b]])

## Related Concepts

- [[Related Concept 1]] — relationship
- [[Related Concept 2]] — relationship

## Sources

- [[source-1]] — coverage
- [[source-2]] — coverage
```

---

## Comparison Page

```markdown
---
title: "X vs Y"
type: comparison
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [source1, source2]
tags: [comparison, tag1, tag2]
---

# X vs Y

> Comparing [[X]] and [[Y]] across key dimensions.

## Summary

Which is better for what, and why.

## Comparison Table

| Dimension | X | Y |
|-----------|---|---|
| Dimension 1 | X's approach | Y's approach |
| Dimension 2 | X's value | Y's value |
| Dimension 3 | X's strength | Y's strength |

## Analysis

### Where X wins
...

### Where Y wins
...

### Key tradeoffs
...

## When to choose X
...

## When to choose Y
...

## Sources
- [[source-1]]
- [[source-2]]
```

---

## Synthesis Page

```markdown
---
title: "Synthesis Title"
type: synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [source1, source2, source3]
tags: [synthesis, tag1]
---

# Synthesis Title

> Cross-cutting analysis synthesizing insights across multiple sources and concepts.

## Thesis

The main argument or insight.

## Evidence

### Supporting Evidence
- From [[source-1]]: ...
- From [[concept-x]]: ...

### Counter-evidence
- From [[source-2]]: ...

## Implications

What this synthesis means for the broader research.

## Open Questions

- Question 1 — needs further investigation
- Question 2 — depends on [[concept-y]]

## Sources
- [[source-1]] — role in synthesis
- [[source-2]] — role in synthesis
```
