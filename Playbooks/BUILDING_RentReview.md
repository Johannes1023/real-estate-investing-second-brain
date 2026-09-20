---
object: BUILDING
as_of: 2026-09-20
status: current
source: Synthetic example
---
# Rent-review playbook

## Summary

A staged review keeps calculations separate from legal validation and an effective rent change.

## Steps

1. Read the current lease and prior rent history.
2. Calculate a candidate adjustment using verified source data.
3. Check the actual contract, current law, notice requirements, and timing outside this demo.
4. Record a decision: reject, defer, or proceed. A proposal does not change the lease note.
5. Only after a valid effective change, update the current lease amount and add a dated rent-history row.
6. Run `Update` to check consistency.

[U03 proposed index review](../RentReviews/U03_IndexReview.md) illustrates a calculation that has **not** changed the current rent.
