---
name: api-testing
description: Checks HTTP APIs by sending real requests to the running app and asserting on the responses, instead of guessing from the code. Covers quick curl checks, lasting request-level tests in the project's test framework, and running existing Bruno, Hurl, or Postman collections locally. Use when building, changing, or debugging an API endpoint, verifying a backend change, testing webhooks, or when the user mentions curl, Postman, Newman, Bruno, Hurl, or API tests.
argument-hint: "[endpoint or collection]"
license: MIT
metadata:
  sources: "Postman and Newman docs, Bruno CLI docs, Hurl docs, supertest and httpx docs"
---

# API testing

Send the request and read the response. Don't assume an endpoint works because the handler looks right.

## Pick the tool

| Need | Tool |
|---|---|
| A test that guards the behavior from now on | The project's test framework, at the HTTP layer (supertest, `httpx`/`TestClient`, `net/http/httptest`, …) through the `tdd` loop |
| A quick check of a change or a bug | `curl` against the running dev server |
| The team already keeps a collection | Run it with its own CLI (below) |

Use what the project already has first. Look for `*.http`, `*.hurl`, a `bruno.json` collection folder, `*.postman_collection.json`, or API tests under `tests/`.

## Quick check with curl

```bash
curl -sS -i http://localhost:3000/api/health
curl -sS -i -X POST http://localhost:3000/api/orders \
  -H 'content-type: application/json' \
  -H "authorization: Bearer $DEV_API_TOKEN" \
  -d '{"sku":"A1","qty":2}'
```

Check the status code, the key headers, and the body shape (`| jq` helps). Then try what usually breaks: missing or invalid fields, wrong types, no auth, someone else's resource (expect 403 or 404), duplicates, and very large input.

## Running collections locally

| Collection | Command | Account needed |
|---|---|---|
| Bruno (`bruno.json` folder) | `bru run --env <name>` from the collection folder (`npm i -g @usebruno/cli`) | No |
| Hurl (`*.hurl`) | `hurl --test --variable host=http://localhost:3000 api/*.hurl` | No |
| Postman (exported v2.1 JSON) | `npx newman run collection.json -e env.json` | No |
| Postman (current format, cloud workspaces) | `postman collection run <collection>` (Postman CLI) | Yes, logs in with an API key |

Newman can't run collections saved in Postman's newer v3 format. Export as v2.1, or use the Postman CLI if the user has a Postman account.
For a new collection that lives in git, Bruno and Hurl keep everything local, as plain files. Details and examples: [references/tools.md](references/tools.md).

## Safety

- Local and staging only by default. Writes or deletes against shared or production environments need explicit approval for that run.
- Tokens and passwords come from environment variables or the tool's secret files. Never inline them in commands, collections, or committed environment files, and never print them.
- Don't paste real customer data into requests or fixtures.

## Report

Say which requests you sent and what came back (status, the relevant part of the body), and which cases you didn't cover.
