# Writes

Every write goes through `post` or `patch`, and fails when `OPEN_PROJECT_READONLY=true`.
Confirm with the user before creating anything or editing a subject or description.

## Optimistic locking

A PATCH to a work package must include its current `lockVersion`, or the API returns `409 Conflict`.
`status` handles this for you. For a raw `patch`, read the work package first:

```bash
lock=$(openproject.sh wp 363 | python3 -c 'import json,sys;print(json.load(sys.stdin)["lockVersion"])')
openproject.sh patch /api/v3/work_packages/363 "{\"lockVersion\":$lock,\"subject\":\"New subject\"}"
```

## Update the description

```bash
python3 -c 'import json,sys;print(json.dumps({"lockVersion":int(sys.argv[1]),"description":{"format":"markdown","raw":open(sys.argv[2]).read()}}))' "$lock" desc.md \
  | openproject.sh patch /api/v3/work_packages/363 -
```

## Create a work package

Find the project id (`projects`) and the type id (`get /api/v3/types`) first.

```bash
cat > /tmp/wp.json <<'JSON'
{
  "subject": "Short imperative title",
  "description": {"format": "markdown", "raw": "What and why, acceptance criteria."},
  "_links": {
    "type": {"href": "/api/v3/types/1"},
    "parent": {"href": "/api/v3/work_packages/363"}
  }
}
JSON
openproject.sh post /api/v3/projects/<project-id>/work_packages @/tmp/wp.json
```

Omit `parent` for a top-level item. Report the new id and URL: `$OPEN_PROJECT_BASE_URL/work_packages/<id>`.
