---
description: A pasted diff should get a two-axis, severity-labelled review.
tags: [trigger, core2]
max_turns: 8
allowed_tools: [Skill, Read, Glob, Grep]
---

Review this change before I merge it. The ticket said: "Users can delete their own comments."

```diff
+app.delete("/comments/:id", async (req, res) => {
+  await db.query(`DELETE FROM comments WHERE id = ${req.params.id}`);
+  res.sendStatus(204);
+});
```
