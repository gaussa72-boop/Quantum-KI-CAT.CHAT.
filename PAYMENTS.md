# Quantum Payments & Credits

Shared prepaid-credit contract for paid AI services. Grant credits only after verified idempotent payment events. Stripe and crypto must use provider adapters/webhooks; no private keys or custody. Persist balances, events and ledger entries transactionally in production. Reserve credits before paid jobs and release them on failure. Keep secrets outside Git.
