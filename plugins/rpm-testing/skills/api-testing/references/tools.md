# API testing tools

## Request-level tests in code (preferred for anything lasting)

Node with supertest:

```ts
import request from "supertest";
import { app } from "../src/app";

test("rejects an order without a sku", async () => {
  const res = await request(app).post("/api/orders").send({ qty: 2 });
  expect(res.status).toBe(400);
  expect(res.body.error).toBe("sku_required");
});
```

Python with FastAPI's `TestClient` (or `httpx` against a running server):

```python
def test_rejects_order_without_sku(client):
    res = client.post("/api/orders", json={"qty": 2})
    assert res.status_code == 400
```

These run in CI with the rest of the suite, need no extra tool, and fail the build when the API breaks.

## Hurl

Plain-text requests with assertions, run by a single binary. Good for smoke tests against a running server.

```hurl
POST {{host}}/api/orders
content-type: application/json
{"sku": "A1", "qty": 2}
HTTP 201
[Asserts]
jsonpath "$.id" exists
```

`hurl --test --variable host=http://localhost:3000 api/*.hurl`

## Bruno

A local-first API client whose collections are plain files in the repo. The desktop app and CLI read the same files.

- `bru run` runs the whole collection from its folder, `bru run users` runs one folder.
- `--env Local` picks an environment, `--env-var KEY=value` overrides one variable.
- Variables marked secret in the app aren't available to the CLI. Pass them with `--env-var` from an environment variable.

## Postman

- **Newman** runs exported collections (v2.1 JSON) offline with no account: `npx newman run collection.json -e env.json --reporters cli`.
- **Postman CLI** (`postman collection run`) is Postman's recommended runner and supports newer collections, but needs a login with a Postman API key, and sends run results to Postman by default.
- The Postman MCP server needs a Postman account and API key too. It isn't part of this plugin. Add it yourself if the team works in Postman's cloud.

## curl and jq

```bash
curl -sS http://localhost:3000/api/orders/42 | jq '.status'
curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:3000/api/orders/999   # expect 404
```
