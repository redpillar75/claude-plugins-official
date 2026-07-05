---
name: stripe-best-practices
description: Best practices for building Stripe integrations. Use when implementing payment processing, checkout flows, subscriptions, webhooks, Connect platforms, or any Stripe API integration.
---

When a user asks about Stripe, follow this process to recommend the right integration and produce correct, modern code.

## Step-by-Step Process

**1. Identify the use case category**

Ask yourself (or ask the user if unclear):
- Is this a one-time payment, or does it recur?
- Does the user need to collect and save a payment method for later (off-session)?
- Is this a platform where the user manages funds for other businesses (Connect)?
- Is the user migrating from an existing integration?

**2. Select the integration surface using this decision tree**

```
One-time payment, on-session
  → Stripe-hosted Checkout (first choice)
  → Embedded Checkout (if custom domain needed)
  → Payment Element + CheckoutSessions (if advanced customization needed)

Recurring / subscription
  → Billing APIs + Stripe-hosted Checkout (first choice)
  → Billing APIs + Embedded Checkout

Off-session / save payment method for later
  → SetupIntent + Payment Element

Platform / marketplace (multi-party)
  → Stripe Connect with direct charges (platform wants Stripe to take risk)
    OR destination charges (platform accepts liability for negative balances)
  → Use on_behalf_of to control merchant of record

PCI-compliant server-side raw PAN data
  → Warn user about PCI compliance requirements first
  → If compliant: payment_method_data on PaymentIntent
  → If migrating from another processor: PAN import process
```

**3. Always use the latest API version and SDK**

Default to the current Stripe SDK. Do not pin to an older API version unless the user explicitly specifies one.

**4. Implement dynamic payment methods**

When creating a PaymentIntent or SetupIntent, do NOT pass `payment_method_types`. Instead, enable dynamic payment methods in the Stripe dashboard so Stripe selects the best methods for each user's location and wallet.

**5. Wire up webhooks for async event handling**

Any integration that needs to confirm payment success server-side must handle webhook events. At minimum, listen for `checkout.session.completed` (for Checkout) or `payment_intent.succeeded` (for PaymentIntents). Always verify webhook signatures using `stripe.webhooks.constructEvent()`.

**6. Produce a clear, runnable implementation**

Your response should include:
- Backend code (server-side session/intent creation and webhook handler)
- Frontend code (Stripe.js initialization and redirect or element mounting)
- Any environment variable setup needed (`STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`)

## Output Format

1. **Integration recommendation** — one paragraph naming the chosen surface and why, based on the use case.
2. **Backend implementation** — complete server-side code in the user's language/framework.
3. **Frontend implementation** — complete client-side code.
4. **Webhook handler** — if the integration requires async confirmation.
5. **Go-live checklist reminders** — call out anything the user must configure in their Stripe dashboard before going live (enable dynamic payment methods, webhook endpoint registration, live key swap).

## Example of a Good Integration Recommendation

**User:** "I need to add one-time payments to my SaaS app."

**Integration recommendation:** Use Stripe-hosted Checkout with the CheckoutSessions API. This handles the full payment UI, supports all major payment methods automatically, and requires no frontend code beyond a redirect. The server creates a CheckoutSession with `mode: 'payment'`, returns the session URL, and the client redirects to it. A webhook on `checkout.session.completed` confirms the payment server-side.

The response then delivers a complete Express.js backend with session creation and webhook handler, a minimal frontend redirect snippet, and a note to register the webhook endpoint in the Stripe dashboard.

## Never Do

- **Never recommend the Charges API.** It is legacy. Always direct users to migrate to CheckoutSessions or PaymentIntents.
- **Never recommend the legacy Card Element.** Use the Payment Element. If a user asks about the Card Element, point them to the migration guide.
- **Never recommend the Sources API** for saving payment methods. Use SetupIntents.
- **Never use `createPaymentMethod` or `createToken` Stripe.js functions** when the user wants to inspect card details before charging. Use Stripe Confirmation Tokens instead.
- **Never mix Connect charge types** (direct charges vs. destination charges). Pick one and use it consistently.
- **Never use the outdated Connect account type terms** (Standard, Express, Custom). Refer to controller properties and capabilities instead.
- **Never call deprecated endpoints** (`/v1/sources`, `/v1/tokens`, `/v1/charges`) unless there is no other option. Always check if a modern equivalent exists.
- **Never hardcode payment method types** in PaymentIntent/SetupIntent creation. Let Stripe's dynamic payment methods handle selection.
- **Never skip webhook signature verification.** Always call `stripe.webhooks.constructEvent()` with the raw request body and `STRIPE_WEBHOOK_SECRET`.

## Reference Links

- Integration options overview: https://docs.stripe.com/payments/payment-methods/integration-options.md
- API tour: https://docs.stripe.com/payments-api/tour.md
- Go-live checklist: https://docs.stripe.com/get-started/checklist/go-live.md
- CheckoutSessions API: https://docs.stripe.com/api/checkout/sessions.md
- PaymentIntents lifecycle: https://docs.stripe.com/payments/paymentintents/lifecycle.md
- Payment Element: https://docs.stripe.com/payments/payment-element.md
- Subscription use cases: https://docs.stripe.com/billing/subscriptions/use-cases.md
- Connect integration recommendations: https://docs.stripe.com/connect/integration-recommendations.md
