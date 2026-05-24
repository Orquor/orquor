# Migration Runbook — ITERAMED → ORQUOR Clinical (Hostinger Edition)

Step-by-step technical migration of the production system from `iteramed.sbs` to `clinical.orquor.com`. Adapted to Fred's actual stack: **Hostinger** for domain registration, DNS, and email; **Hyperstack / Lambda Labs** for GPU-bound API hosting. Designed to execute in a single 6-hour window with a planned 90-minute maintenance pause.

**Pre-conditions**:
- Domains purchased through **Hostinger Domain Registrar** (`orquor.com`, `orquor.ai`, `orquor.health`, `orquor.io`, `orquor.co`, `orquor.app`)
- Hostinger hPanel access active (with 2FA)
- Access to the current Hyperstack A100 VM via SSH key `ITERAMED_OFICIAL_Hyperstack.pem`
- Access to current Google OAuth client console

**Architectural split (do not confuse)**:

| Component | Runs on | Reason |
|---|---|---|
| Marketing site (`orquor.com`) | **Hostinger Web Hosting** (Premium or Business plan, USD 2.99–3.99/mo) | Static HTML, perfect for shared hosting |
| Blog (`blog.orquor.com`) | **Hostinger Web Hosting** (same plan, WordPress or Ghost) | Standard CMS, no GPU |
| Clinical app (`clinical.orquor.com`) | **Hyperstack VM (A100)** unchanged | Requires GPU for ASR + MT |
| API (`api.clinical.orquor.com`) | **Hyperstack VM (A100)** unchanged | Same as clinical app |
| Email (`@orquor.com`) | **Hostinger Email** (free with hosting) or Google Workspace USD 6/user/mo | Standard mail relay |
| Future Hermes platform (`hermes.orquor.com`) | TBD — Vercel for FE, Hyperstack/Lambda for backend | Out of scope this runbook |

---

## Phase 0 — Pre-flight (≤ 30 minutes)

- [ ] **Verify Hostinger plan**: confirm Business or Premium Web Hosting plan (shared hosting Premium minimum recommended for performance). Free SSL is included on all plans.
- [ ] **Hostinger 2FA**: enable hPanel 2FA before doing anything else.
- [ ] **Backup**: snapshot the Hyperstack VM through Hyperstack console. Confirm snapshot ID.
- [ ] **Database backup**: `pg_dump` on the VM, copy off-VM to local + Hostinger File Manager (or any S3 / R2 / B2 bucket).
- [ ] **Notify users**: email all active users 24 hours before with maintenance window (email template at end of this runbook).
- [ ] **Status banner**: deploy a maintenance banner on `iteramed.sbs` indicating start time and duration.

---

## Phase 1 — Hostinger DNS provisioning (45 minutes)

In **hPanel → Domain → DNS / Nameservers**:

### 1.1 Confirm nameservers point to Hostinger
Hostinger nameservers should be (defaults when registered through them):
```
ns1.dns-parking.com
ns2.dns-parking.com
```
If domains were registered elsewhere and transferred in, ensure NS records point to Hostinger before continuing. Propagation takes 4–24 hours.

### 1.2 Open hPanel → Domains → orquor.com → DNS Zone Editor

Add the following records:

| Type | Name | Value | TTL |
|---|---|---|---|
| A | `@` (root) | IP of Hostinger shared hosting | 14400 |
| CNAME | `www` | `orquor.com` | 14400 |
| A | `clinical` | IP of Hyperstack A100 VM | 14400 |
| A | `api.clinical` | IP of Hyperstack A100 VM | 14400 |
| CNAME | `hermes` | (placeholder, e.g. `cname.vercel-dns.com`) | 14400 |
| CNAME | `academy` | Skool/Teachable subdomain target | 14400 |
| CNAME | `blog` | `orquor.com` (host on same Hostinger plan) | 14400 |
| MX | `@` | `mx1.hostinger.com` priority 5 | 14400 |
| MX | `@` | `mx2.hostinger.com` priority 10 | 14400 |
| TXT | `@` | `v=spf1 include:_spf.hostinger.com ~all` | 14400 |
| TXT | `_dmarc` | `v=DMARC1; p=quarantine; rua=mailto:dmarc@orquor.com` | 14400 |

DKIM is auto-generated when you create the first email account in `hPanel → Emails`; copy the DKIM TXT record Hostinger provides into the DNS zone.

Repeat the same exercise on `orquor.ai`, `orquor.health`, `orquor.io`, `orquor.co`, `orquor.app` — but on those domains, set up a redirect to `orquor.com` (see Phase 4).

### 1.3 Hostinger built-in security
- [ ] **hPanel → Security → HTTPS auto-redirect**: ON
- [ ] **hPanel → Security → Web Application Firewall**: ON (basic protection included)
- [ ] **DNSSEC**: enable in **hPanel → Domains → DNS**. Hostinger supports it free.

### 1.4 Verify propagation
- [ ] `nslookup clinical.orquor.com 8.8.8.8` → returns Hyperstack IP
- [ ] `nslookup orquor.com 8.8.8.8` → returns Hostinger IP
- [ ] Use **https://dnschecker.org** to verify A records propagated globally

---

## Phase 2 — SSL certificates (15 minutes)

### 2.1 Hostinger-hosted domains (orquor.com, blog.orquor.com)
- [ ] **hPanel → Security → SSL**: click "Setup" on each domain
- [ ] Hostinger auto-generates free Let's Encrypt with auto-renewal
- [ ] Wait 60 seconds for the green checkmark
- [ ] Test: `curl -I https://orquor.com` returns 200 + valid cert

### 2.2 Hyperstack-hosted subdomains (clinical.orquor.com, api.clinical.orquor.com)
- [ ] SSH into the Hyperstack VM
- [ ] Install certbot if absent: `sudo apt install certbot python3-certbot-nginx`
- [ ] Issue certificate:
  ```
  sudo certbot --nginx \
      -d clinical.orquor.com \
      -d api.clinical.orquor.com \
      --non-interactive --agree-tos -m freddy@orquor.com
  ```
- [ ] Verify nginx config updated. Test: `sudo nginx -t`. Reload: `sudo systemctl reload nginx`.
- [ ] External test: `curl -I https://clinical.orquor.com` returns 200 with valid cert
- [ ] Renewal cron is automatic with certbot — confirm with `sudo systemctl list-timers | findstr certbot` (Linux: `systemctl list-timers | grep certbot`)

---

## Phase 3 — Deploy marketing site to Hostinger (30 minutes)

### 3.1 Method A — File Manager upload (fastest for static HTML)
- [ ] Open **hPanel → Files → File Manager**
- [ ] Navigate to `public_html/`
- [ ] Delete the default `index.html`
- [ ] Upload the entire contents of `04-web/` from this repo (currently just `index.html`)
- [ ] If logo SVG and whitepaper PDF need to be served, upload those to `public_html/assets/` and `public_html/whitepaper-acto.pdf` respectively
- [ ] Test: open `https://orquor.com` in a browser. Should render the landing page.

### 3.2 Method B — Git deployment (better for ongoing iteration)
- [ ] **hPanel → Advanced → Git**
- [ ] Create new repository pointing to `github.com/orquor/orquor-web.git` (after you create the GitHub org)
- [ ] Branch: `main`
- [ ] Build path: `/public_html`
- [ ] Auto-deploy on push: ON
- [ ] Push your `04-web/` contents to the GitHub repo; Hostinger pulls automatically

Recommendation: start with Method A for speed, migrate to Method B after the first week.

### 3.3 Add `.htaccess` for SPA-style routing (if needed for future)
If you decide the marketing site grows into a Next.js or React app, create `public_html/.htaccess`:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
```
For HTML-only static site as currently shipped, no .htaccess needed.

---

## Phase 4 — 301 redirects from iteramed.sbs (30 minutes)

Goal: every URL on `iteramed.sbs` permanently redirects to its `clinical.orquor.com` equivalent.

The current `.sbs` domain is *not* registered through Hostinger. Two paths:

### 4.1 If iteramed.sbs is at your previous registrar
- [ ] Log into the registrar
- [ ] DNS section: add an A record for `iteramed.sbs` pointing to **a tiny redirect VM or a Cloudflare Pages free site**
- [ ] On that endpoint, configure HTTP-level 301 with path preservation:
  - Nginx snippet:
    ```nginx
    server {
        listen 80;
        server_name iteramed.sbs www.iteramed.sbs api.iteramed.sbs;
        return 301 https://clinical.orquor.com$request_uri;
    }
    ```

### 4.2 If you transfer iteramed.sbs to Hostinger
- [ ] Transfer the `.sbs` domain to Hostinger (USD ~3, 7 days)
- [ ] Use **hPanel → Domains → iteramed.sbs → Redirects** to set up forwarding to `https://clinical.orquor.com` with "preserve path" enabled

**Recommended**: option 4.2 for centralized management. The transfer takes a week but Hostinger handles redirects natively after that.

### 4.3 Apex-to-www and other secondary domains
Use the same hPanel redirect feature to point:
- `orquor.ai` → `orquor.com`
- `orquor.health` → `orquor.com` (or to `clinical.orquor.com` for vertical-specific entry)
- `orquor.io` → `orquor.com`
- `orquor.co` → `orquor.com`
- `orquor.app` → reserved for future product

---

## Phase 5 — Email setup with Hostinger Email (45 minutes)

### 5.1 Create email accounts in hPanel → Emails
- [ ] `freddy@orquor.com` (your founder mailbox, full inbox)
- [ ] `hello@orquor.com` (catch-all for inbound contact, forward to freddy@)
- [ ] `noreply@orquor.com` (transactional outbound, no inbox needed)
- [ ] `support@orquor.com` (forward to freddy@ until you have a team)
- [ ] `legal@orquor.com` (forward to freddy@)
- [ ] `privacy@orquor.com` (forward to freddy@, required by privacy policy)
- [ ] `research@orquor.com` (forward to freddy@)
- [ ] `hermes@orquor.com` (used by HERMES sub-agents for system-generated notifications)

### 5.2 Configure DKIM (Hostinger panel)
- [ ] **hPanel → Emails → DKIM Manager** — enable DKIM signing
- [ ] Hostinger adds the DKIM TXT record automatically; verify in DNS Zone Editor

### 5.3 Application transactional email
For the Orquor Clinical API to send transactional email (password resets, BAA reminders), two options:

**Option A — Use Hostinger SMTP (cheapest)**
```
SMTP_HOST=smtp.hostinger.com
SMTP_PORT=465
SMTP_USER=noreply@orquor.com
SMTP_PASS=[generated in hPanel]
SMTP_SECURE=true
```
Limit: 100 emails/hour on shared, 500/hour on Business plan.

**Option B — Resend (better for production volume)**
- [ ] Create free Resend account (3,000 emails/month free tier)
- [ ] Add `orquor.com` to Resend
- [ ] Add the DKIM and Return-Path TXT records that Resend provides to Hostinger DNS Zone Editor
- [ ] Update API env to use `RESEND_API_KEY`

Recommendation: start with Option A for the first 30 days while volume is low, migrate to Option B before you cross 50 emails/day.

### 5.4 Email signature template
Save in your mail client + share with HERMES Content-Bot:
```
Freddy [Apellido]
Founder, Orquor S.A.C.
freddy@orquor.com · orquor.com
Lima, Peru
```

---

## Phase 6 — Application reconfiguration on Hyperstack VM (60 minutes)

### 6.1 Environment variables on the VM
SSH into the Hyperstack VM and edit production `.env`:
```
APP_DOMAIN=clinical.orquor.com
API_BASE_URL=https://api.clinical.orquor.com
FRONTEND_URL=https://clinical.orquor.com
OAUTH_REDIRECT_URI=https://clinical.orquor.com/auth/callback
BRAND_NAME=Orquor Clinical
SMTP_HOST=smtp.hostinger.com
SMTP_PORT=465
SMTP_USER=noreply@orquor.com
SMTP_PASS=[paste from Hostinger]
```
Restart the service: `sudo systemctl restart orquor-api`

### 6.2 Google OAuth client update
In Google Cloud Console → APIs & Services → Credentials:
- [ ] Add `https://clinical.orquor.com` to Authorized JavaScript Origins
- [ ] Add `https://clinical.orquor.com/auth/callback` to Authorized redirect URIs
- [ ] Keep the old `iteramed.sbs` redirect URI active for 14 days as grace period
- [ ] Optional: create a new OAuth client labeled "Orquor Clinical Production"

### 6.3 Frontend rebrand on the app
- [ ] Replace all UI strings "ITERAMED" → "Orquor Clinical"
- [ ] Replace logo asset with the SVG from `02-brand/logo-concepts.svg` (Concept A — Loop doble)
- [ ] Apply theme tokens from `02-brand/BRAND_IDENTITY.md`
- [ ] Update favicon and Open Graph meta tags
- [ ] Rebuild and deploy the frontend bundle (the static assets live on the Hyperstack VM unless you split them off to Hostinger)

### 6.4 Backend updates
- [ ] Update CORS allowlist to include `https://clinical.orquor.com` and `https://orquor.com`
- [ ] Update email templates (transactional, BAA reminders, password reset) with new brand
- [ ] Re-issue API keys to active customers (notify in advance)

---

## Phase 7 — Migration communication (immediately after cutover)

Send the email below to all active users from `noreply@orquor.com` via Hostinger SMTP:

> **Subject**: We've renamed. ITERAMED is now Orquor Clinical.
>
> Hello,
>
> Today we completed the rebrand of ITERAMED to **Orquor Clinical**. Same team, same product, more ambitious mission.
>
> What this means for you:
> - The platform is now at **clinical.orquor.com** (old links continue to redirect automatically)
> - Your account, your sessions, your audit logs are unchanged
> - You may need to sign in again — your previous session was preserved but the cookie domain changed
>
> If anything is not working as expected, reply to this email and we will fix it within the hour.
>
> Why the change?
>
> Orquor is the parent company for our next products: Orquor Hermes (agent orchestration), Orquor Academy (AI evaluation training), and several adjacent verticals coming this year. Orquor Clinical is the first and remains the most important product in the family.
>
> Thank you for being part of this from the beginning.
>
> Freddy
> Founder, Orquor
> freddy@orquor.com

---

## Phase 8 — Post-cutover verification + lift banner (30 minutes)

- [ ] Smoke tests: login flow on `clinical.orquor.com`, start a session, complete a translation, verify audit log entry, sign out
- [ ] Verify cryptographic timestamping still functional (test session log has valid OpenTimestamps proof)
- [ ] Verify Google OAuth callback works with new redirect_uri
- [ ] Verify a password-reset email arrives in Gmail inbox (not spam) — confirms SPF/DKIM/DMARC are correct
- [ ] Visit `iteramed.sbs/some-path` in browser → confirm transparent redirect to `clinical.orquor.com/some-path`
- [ ] Check error monitoring (Sentry, etc.) for unusual errors in the first hour
- [ ] Check Hostinger Analytics + Cloudflare/Plausible for landing-page traffic
- [ ] Remove maintenance banner from clinical.orquor.com

---

## Rollback plan

Within the first 4 hours of cutover, rollback is straightforward:

1. Restore the VM from the Phase 0 snapshot
2. Revert Google OAuth client to the old config
3. In Hostinger DNS Zone Editor, point `clinical.orquor.com` A record back to a temporary "down for maintenance" page
4. Remove the 301 redirects from iteramed.sbs
5. Email users about the rollback

After 4 hours and the first new sessions on clinical.orquor.com, rollback requires database merge — plan accordingly.

---

## Hostinger-specific gotchas (lessons learned)

| Issue | Workaround |
|---|---|
| Hostinger shared hosting has a 100 email/hour limit | Move transactional email to Resend before scaling outreach |
| Hostinger Premium plan limits to 100 GB storage and 25k visits/month | Upgrade to Business plan (USD 3.99/mo) before first traffic spike |
| WordPress staging slot doesn't exist on Premium | Build staging manually in a subdomain like `staging.orquor.com` |
| Hostinger SSL renewal can fail silently | Set up a monthly calendar reminder to check certificate expiry in hPanel |
| Hostinger's File Manager has a 100 MB single-file upload limit | Use SFTP for larger files (credentials in hPanel → Files → FTP Accounts) |
| Hostinger backups are once-daily on Premium | Take manual backups before any major migration |

---

## Total time estimate

| Phase | Time |
|---|---|
| 0 — Pre-flight | 30 min |
| 1 — DNS (Hostinger) | 45 min |
| 2 — SSL (Hostinger free + certbot on VM) | 15 min |
| 3 — Deploy marketing site to Hostinger | 30 min |
| 4 — 301 redirects from iteramed.sbs | 30 min |
| 5 — Email setup (Hostinger Email) | 45 min |
| 6 — Application reconfiguration on Hyperstack | 60 min |
| 7 — Communication | 15 min |
| 8 — Verification + lift banner | 30 min |
| **Total** | **~5 hours** |

Plan a 6-hour window. Best time slot: Sunday 02:00–08:00 UTC-5 (lowest traffic on the platform).
