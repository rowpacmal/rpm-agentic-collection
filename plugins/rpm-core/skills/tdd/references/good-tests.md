# Good and bad tests

## A good test

- Names a behavior a caller cares about: `rejects an expired coupon`, not `calls validateDate`.
- Uses only the public interface, so it survives refactors.
- Checks one behavior. Several assertions are fine if they describe the same outcome.
- Sets up what it needs close to the test, so a reader doesn't hunt through shared setup.
- Fails with a message that says what broke.

```ts
// Good: observable behavior through the interface
test("an expired coupon is rejected", () => {
  const cart = cartWith({ coupon: coupon({ expires: "2026-01-01" }), today: "2026-02-01" });
  expect(applyCoupon(cart).error).toBe("coupon_expired");
});
```

## Bad tests, and the tell

| Kind | Example | Tell |
|---|---|---|
| Implementation-coupled | Asserts `paymentService.process` was called with `total` | Breaks on a refactor that keeps behavior |
| Side channel | Checks a DB row after `createUser()` instead of calling `getUser()` | Knows about storage the caller never sees |
| Tautological | `expect(add(a, b)).toBe(a + b)` | Can never disagree with the code |
| Snapshot of everything | Huge snapshot nobody reads | Gets re-recorded whenever it fails |
| Order or time dependent | Passes alone, fails in the suite or after midnight | Flaky |
| Over-mocked | Every collaborator is a mock | Tests the mocks, not the code |

## Mocking

Mock at the edge of the system only:
- External APIs (payments, email, third-party services)
- Time and randomness
- Sometimes the file system or database, when a real or in-memory one is impractical

Don't mock your own modules or internal collaborators. If something is hard to test without that, make the dependency injectable:

```ts
// Easy to test: the client is passed in
export function chargeOrder(order: Order, payments: PaymentsClient) {
  return payments.charge(order.total);
}
```

Prefer a small fake with real behavior (an in-memory repository) over a mock that only records calls.

## Where tests go

Follow the project's layout. If it has none:
- Unit tests for pure logic next to the code or under `tests/unit/`.
- Integration tests that cross modules or hit a real database under `tests/integration/`.
- End-to-end tests that drive the running app (browser or HTTP) under `e2e/` or `tests/e2e/`.

## Bug fixes

1. Write a test that reproduces the bug through the interface. Run it and watch it fail on the reported symptom.
2. Fix the code.
3. The test passes, and stays as the regression test.
