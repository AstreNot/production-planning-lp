# Production planning under material scarcity: data model summary (synthetic exercise)

Choose production quantities that maximise margin when materials are scarce and batches must be whole multiples. A fictional manufacturer: 20 products, 5 materials, a bill of materials.

## Status
- Runs end to end in under a second. Self-checks pass (material-feasible, within demand, whole batches, fill-rate ordering).
- Single period only.

## 1. Problem and process
1. **LP relaxation:** continuous quantities. An upper bound on what is achievable.
2. **MPQ rounding:** floor to minimum-production-quantity multiples. Stays feasible, loses fill rate.
3. **Recovery:** spend leftover material on whole batches, best margin per material first.

## 2. Data flow
```mermaid
flowchart LR
    D[Seeded data] --> LP[LP relaxation] --> R[MPQ rounding] --> V[Recovery pass] --> O[Fill rate + margin]
```

## 3. Model
- Variables: quantity per product. Objective: maximise margin.
- Constraints: material use <= availability (BOM), quantity <= demand.

## 4. Tests
Material feasibility, demand cap, multiples of MPQ, and `fill(LP) >= fill(recovered) >= fill(rounded)`.

## 5. Known issues and next steps
- Rounding gap depends on how tight materials are. Next: multi-period balances, substitution, a MILP with make/no-make binaries.

## 6. How to run
```
python run.py     # prints fill and margin per stage, saves fill_rate.png
```
Needs numpy and scipy; matplotlib optional.

---
Part of the portfolio at https://astrenot.github.io/Arkananta-Website/. Synthetic data only.
