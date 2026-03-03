# Evidence-First vs Detection-Only Security: The Gap in Current Tooling

*Checkov tells you what's wrong. But can you prove it was fixed? Here's why detection-only security fails compliance audits — and how evidence-first architecture solves it.*

---

Imagine this: Your Vanta dashboard shows "Terraform scanning enabled." The auditor asks: "Prove this scan actually blocked a risky S3 bucket last month."

You provide... a screenshot. The auditor nods, makes a note, moves on.

But here's what neither of you can prove: **whether that control actually ran, or whether the screenshot was fabricated after the fact.**

This is the gap between detection-only security and evidence-first security. One tells you what's wrong. The other proves you fixed it.

## Detection-Only Tools: What They Do Well

Let's start with credit where it's due. Checkov, Terrascan, tfsec, and similar tools are excellent at what they do:

**Policy scanning works:** Scans infrastructure-as-code for violations, identifies misconfigurations before deployment, integrates with CI/CD pipelines, provides clear remediation guidance, and costs $0 for most use cases.

**GitHub Actions can block PRs:** Runs checks on every pull request, prevents risky code from merging, and automates enforcement without manual review.

**Dashboards show compliance status:** Vanta and Drata aggregate evidence from 100+ SaaS integrations, track which controls are enabled, and generate compliance reports for auditors.

**But there's a critical limitation:** None of this provides cryptographic proof that controls actually ran.

## The Auditor's Dilemma

SOC 2, FedRAMP, and PCI DSS all require "evidence that controls are effective." Current evidence includes:

**What auditors accept today:**
- Screenshots of dashboards
- Manually exported logs
- Human attestations in spreadsheets
- Configuration file snapshots
- Point-in-time compliance reviews

**The problems:**
- **Time-consuming**: 54% of firms spend 5+ hours/week on manual evidence collection (Swimlane study)
- **Forgeable**: Screenshots can be doctored, logs can be altered
- **Point-in-time only**: Proves controls were enabled once, not that they run continuously
- **Not tamper-evident**: No way to verify evidence hasn't been modified

The gap exists because we're using detection-only tools for a compliance job that requires proof-of-prevention.

## Evidence-First Architecture: What It Means

**Evidence** in security context means: cryptographically signed, tamper-evident proof that a control ran with a specific result.

Not "we enabled Terraform scanning." But "here's cryptographic proof that Terraform scanning ran on commit abc123 at timestamp T, found violation X, and blocked deployment."

### The Technical Standards Already Exist

**SLSA (Supply chain Levels for Software Artifacts):** Framework for supply chain attestations, defines what evidence should contain, Levels 1–4 for increasing assurance. Developed by Google, implemented by GitHub and Red Hat. ([slsa.dev](https://slsa.dev))

**DSSE (Dead Simple Signing Envelope):** Standard format for signed attestations, used by in-toto and Sigstore. Wraps payload + signature + metadata. ([github.com/secure-systems-lab/dsse](https://github.com/secure-systems-lab/dsse))

**Hash Chains (Merkle trees):** Each attestation references parent hash, creates tamper-evident audit trail. Used by Git, blockchain, certificate transparency logs. Any modification breaks the chain.

**The pieces exist. What's missing is integration into policy-as-code workflows.**

## Technical Deep-Dive: How Mondrian Implemented It

I spent 4 hours building an evidence-first Zero Trust CLI to validate this approach. Here's what the implementation looks like:

### The Policy Engine

Three hard-coded rules for validation:

**S3 Public Bucket Detection:**

```go
func checkS3PublicBuckets(content string) []CheckResult {
    violations := []CheckResult{}
    publicPatterns := []string{
        "public_read",
        "public-read",
        "public_read_write",
    }
    for _, pattern := range publicPatterns {
        if strings.Contains(content, pattern) {
            violations = append(violations, CheckResult{
                RuleID:      "s3-no-public-buckets",
                Severity:    "HIGH",
                Message:     fmt.Sprintf("Public S3 bucket detected: %s", pattern),
                Remediation: "Remove public ACL, use IAM policies instead",
            })
        }
    }
    return violations
}
```

This is intentionally simple — the complexity isn't in the policy logic, it's in the evidence generation.

### Evidence Generation (SLSA-Compatible)

The `internal/evidence/` package creates attestations:

```go
type Attestation struct {
    PredicateType string                `json:"predicateType"`
    Subject       []Subject             `json:"subject"`
    Predicate     PolicyCheckPredicate  `json:"predicate"`
    Timestamp     time.Time             `json:"timestamp"`
    RunID         string                `json:"runId"`
    ParentHash    string                `json:"parentHash,omitempty"`
    Hash          string                `json:"hash"`
}

type PolicyCheckPredicate struct {
    Results       []policy.CheckResult `json:"results"`
    Environment   map[string]string    `json:"environment"`
    Command       string               `json:"command"`
    ExitCode      int                  `json:"exitCode"`
}
```

**Key insight:** The attestation contains not just "what violations were found" but "what command ran, in what environment, with what result" — provable facts, not claims.

### DSSE Signature Generation

```go
type Signer struct {
    keyID      string
    privateKey *ecdsa.PrivateKey
    publicKey  *ecdsa.PublicKey
}

func (s *Signer) SignAttestation(attestation *Attestation) (*SignedAttestation, error) {
    payload, err := json.Marshal(attestation)
    if err != nil {
        return nil, err
    }
    envelope, err := dsse.CreateEnvelope(
        "application/vnd.mondrian.policy-check+json",
        payload,
        s,
    )
    return &SignedAttestation{
        Envelope: *envelope,
        Metadata: SigningMetadata{
            KeyID:     s.keyID,
            Timestamp: time.Now(),
        },
    }, nil
}
```

**What this gives you:** Tamper-evident proof that can be verified later. Anyone with the public key can verify the attestation was signed by Mondrian's key, the payload hasn't been modified, and the signature was created at a specific time.

### Hash Chain for Audit Trail

```go
func (a *Attestation) GenerateHash() string {
    h := sha256.New()
    h.Write([]byte(a.PredicateType))
    h.Write([]byte(a.Timestamp.String()))
    h.Write([]byte(a.ParentHash)) // Links to previous
    return hex.EncodeToString(h.Sum(nil))
}
```

A chain where each attestation proves the previous one existed. You can't insert fake attestations retroactively because the hashes won't match.

### GitHub Actions Integration

```yaml
name: Mondrian Policy Check
on: [pull_request]
jobs:
  security-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Mondrian Check
        run: mondrian check --rules iac,deploy
      - name: Generate Attestation
        if: success()
        run: mondrian attest --output .mondrian/attestation.json
      - name: Upload Evidence
        uses: actions/upload-artifact@v3
        with:
          name: compliance-evidence
          path: .mondrian/
```

This blocks risky PRs (like Checkov) PLUS generates signed proof that the check ran.

## The Implementation Gap: Why This Isn't a Product Yet

The technical pieces work. So why isn't this the standard approach?

### Vanta/Drata Already Solve 80%

Current GRC platforms automated evidence collection with 100+ SaaS integrations, continuous monitoring, dashboards, and audit report generation. **Cost reduction: $400K traditional process to $200K with automation.**

Adding cryptographic signatures would be technically straightforward. The question isn't "Can it be done?" — it's **"Do auditors care?"**

### The Auditor Acceptance Question

Cryptographic signatures work in other domains: DocuSign for legal contracts, GitHub for signed commits, AWS CloudTrail for infrastructure audits, Stripe and QuickBooks for financial audit trails.

**So why not compliance?** Cultural lag, not technical limitation. Auditors are trained to review screenshots and logs. The industry needs to shift from "human review of evidence" to "automated verification of signatures."

## When You Need Evidence vs Detection

**Detection-Only is Sufficient For:** Development/staging environments, pre-production testing, low-risk applications.

**Evidence-First is Required For:** SOC 2 / ISO 27001 / FedRAMP compliance, incident response investigations, regulatory audits (HIPAA, PCI DSS, GDPR), supply chain attestation (SLSA Level 3).

**Hybrid Approach (Most Realistic):** Run detection checks continuously for fast feedback. Generate signed attestations periodically for compliance checkpoints. Keep attestations for the audit retention period. Verify signature chains during audits.

## The Path Forward

Evidence-first security isn't hypothetical — it's implemented and working in supply chain security (SLSA), code signing (Sigstore), and infrastructure logging (CloudTrail).

**What's missing:** Integration into compliance workflows.

**For GRC Platforms:** Add DSSE signing to evidence collection. Offer "cryptographically verified" badges. Educate auditors on signature verification.

**For Policy-as-Code Tools:** Generate SLSA attestations as output. Support DSSE envelope format. Provide reference implementations.

**For CISOs and Security Leaders:** Ask vendors "Do you generate signed attestations?" Pilot evidence-first approaches in non-critical systems. Advocate for cryptographic evidence in audit negotiations.

## Conclusion

Checkov tells you what's wrong. Evidence-first security proves you fixed it.

The technical standards exist (SLSA, DSSE, hash chains). The cryptographic precedents work (DocuSign, GitHub, CloudTrail). The academic research confirms feasibility (73.3% effort reduction).

**What's missing is adoption.** Auditors need training. Platforms need integration. Standards bodies need endorsement.

The next time an auditor asks "Can you prove this control ran?" — you'll have a cryptographic signature instead of a screenshot.

---

**Related reading from Humaine Studio:**
- [Why I Built and Shelved a Zero Trust Tool](https://humaine.studio/posts/2026/03/02/experiments-building-grc-tool-weekend/) — The decision framework behind Mondrian's archive
- [The Security Poverty Line](https://humaine.studio/posts/2026/03/02/security-poverty-line/) — Economic analysis of compliance costs

**Technical Resources:** [SLSA Framework](https://slsa.dev) | [in-toto Project](https://in-toto.io) | [Sigstore](https://www.sigstore.dev) | [Mondrian GitHub](https://github.com/miqcie/mondrian) | [arXiv:2502.16344](https://arxiv.org/abs/2502.16344)

*Originally published at [humaine.studio](https://humaine.studio/posts/2026/03/02/evidence-first-vs-detection-only-security/)*

---

> **Canonical URL:** https://humaine.studio/posts/2026/03/02/evidence-first-vs-detection-only-security/
> Set this in Substack post settings under "This post was originally published elsewhere"
