# Sprints and boards

On many instances, **sprints are not versions**. `/api/v3/versions` can be empty while sprints exist.
Don't conclude from an empty versions list that there are no sprints.

A sprint board is a grid (`/api/v3/grids`) whose grid-level `options.filters` contains an entry like:

```json
{"sprint_id": {"operator": "=", "values": ["17"]}}
```

`sprint` is also a valid work-package filter.

## The trap

A board's columns are ordinary saved queries that filter on **status only**. The sprint filter lives on the grid, not on the column queries.
Reading a column query directly returns every matching work package in the project, not only the sprint's. The numbers look plausible but are wrong.

## Do this

1. `openproject.sh boards` maps board names to sprint ids.
2. `openproject.sh sprint <id> [status-id]` lists the sprint's work packages, with the sprint filter applied.

For custom queries, always add the `sprint` filter yourself:

```bash
filters='[{"sprint":{"operator":"=","values":["17"]}},{"status":{"operator":"=","values":["7"]}}]'
openproject.sh get "/api/v3/work_packages?pageSize=200&filters=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$filters")"
```

If an instance has no sprint grids and `versions` isn't empty, it uses versions as sprints. Filter on `version` instead.
