# Code smell baseline

Each smell is a heuristic. Report it as "possible <smell>", never as a hard violation.
A documented project standard that endorses the pattern overrides it.

| Smell | Looks like | Usual fix |
|---|---|---|
| Mysterious name | A name that doesn't say what the thing does or holds | Rename it. If no honest name comes, the design is unclear |
| Duplicated code | The same logic shape in several hunks or files | Extract the shared shape once |
| Feature envy | A function that uses another object's data more than its own | Move it next to that data |
| Data clumps | The same few fields or params always travel together | Bundle them into one type |
| Primitive obsession | A string or number standing in for a domain concept | Give the concept a small type |
| Repeated switches | The same switch/if-chain on one type in several places | One map or polymorphism shared by all sites |
| Shotgun surgery | One logical change needs scattered edits | Gather what changes together |
| Divergent change | One module edited for several unrelated reasons | Split by reason to change |
| Speculative generality | Hooks, params, or layers for needs nobody has | Delete. Inline until a real need appears |
| Message chains | `a.b().c().d()` walks the caller shouldn't depend on | One method on the first object |
| Middle man | A wrapper that only delegates | Call the real target |
| Refused bequest | A subclass ignoring most of what it inherits | Composition instead of inheritance |
