# Evidence-First vs Detection-Only Security: The Gap in Current Tooling

## Checkov tells you what's wrong. But can you prove it was fixed?

Vanta dashboard shows "Terraform scanning enabled."

Auditor asks: "Prove this scan actually blocked a risky S3 bucket last month."

You provide... a screenshot. The auditor nods, makes a note, moves on.

But here's what neither of you can prove: **whether that control actually ran, or whether the screenshot was fabricated after the fact.**

This is the gap between detection-only security and evidence-first security. One tells you what's wrong. The other proves you fixed it.

---

## Detection-Only Tools: What They Do Well

Credit where it's due. Checkov, Terrascan, tfsec, and similar tools are excellent at what they do:

- Scans infrastructure-as-code for violations (Terraform, CloudFormation, Kubernetes)
- Identifies security misconfigurations before deployment
- Integrates with CI/CD pipelines
- Provides clear remediation guidance
- Costs $0 for most use cases

GitHub Actions can block PRs. Dashboards (Vanta, Drata) aggregate evidence from 100+ SaaS integrations. Reports get generated for auditors.

**But there's a critical limitation:** None of this provides cryptographic proof that controls actually ran.

## The Auditor's Dilemma

SOC 2, FedRAMP, and PCI DSS all require "evidence that controls are effective." Current evidence includes screenshots of dashboards, manually exported logs, human attestations in spreadsheets, and point-in-time compliance reviews.

The problems are clear:

- **Time-consuming**: 54% of firms spend 5+ hours/week on manual evidence collection (Swimlane study)
- **Forgeable**: Screenshots can be doctored, logs can be altered
- **Point-in-time only**: Proves controls were enabled once, not that they run continuously
- **Not tamper-evident**: No way to verify evidence hasn't been modified

The gap exists because we're using detection-only tools for a compliance job that requires proof-of-prevention.

## Evidence-First Architecture: What It Means

**Evidence** in security context means: cryptographically signed, tamper-evident proof that a control ran with a specific result.

Not "we enabled Terraform scanning." But "here's cryptographic proof that Terraform scanning ran on commit abc123 at timestamp T, found violation X, and blocked deployment."

### The Technical Standards Already Exist

**SLSA (Supply chain Levels for Software Artifacts):** Framework for supply chain attestations with Levels 1–4 for increasing assurance. Developed by Google, implemented by GitHub and Red Hat.

**DSSE (Dead Simple Signing Envelope):** Standard format for signed attestations used by in-toto and Sigstore. Wraps payload + signature + metadata.

**Hash Chains (Merkle trees):** Each attestation references parent hash. Creates tamper-evident audit trail. Used by Git, blockchain, certificate transparency logs.

The pieces exist. What's missing is integration into policy-as-code workflows.

## Technical Deep-Dive: How Mondrian Implemented It

I spent 4 hours building an evidence-first Zero Trust CLI to validate this approach.

### The Policy Engine

Three hard-coded rules for validation. Here's S3 Public Bucket Detection:

```go
func checkS3PublicBuckets(content string) []CheckResult {
    violations := []CheckResult{}
    publicPatterns := []string{
        "public_read", "public-read", "public_read_write",
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

Intentionally simple — the complexity isn't in the policy logic, it's in the evidence generation.

### Evidence Generation (SLSA-Compatible)

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
```

The attestation contains not just "what violations were found" but "what command ran, in what environment, with what result" — provable facts, not claims.

### DSSE Signature Generation

```go
func (s *Signer) SignAttestation(attestation *Attestation) (*SignedAttestation, error) {
    payload, _ := json.Marshal(attestation)
    envelope, _ := dsse.CreateEnvelope(
        "application/vnd.mondrian.policy-check+json",
        payload, s,
    )
    return &SignedAttestation{
        Envelope: *envelope,
        Metadata: SigningMetadata{KeyID: s.keyID, Timestamp: time.Now()},
    }, nil
}
```

Tamper-evident proof that can be verified later. Anyone with the public key can verify the attestation was signed, the payload hasn't been modified, and when the signature was created.

### Hash Chain for Audit Trail

Each attestation references its parent. A chain where each attestation proves the previous one existed. You can't insert fake attestations retroactively because the hashes won't match.

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

Blocks risky PRs (like Checkov) **plus** generates signed proof that the check ran.

---

## The Implementation Gap

### Vanta/Drata Already Solve 80%

Current GRC platforms automated evidence collection: 100+ SaaS integrations, continuous monitoring, dashboards, and audit report generation. Cost reduction from $400K to $200K.

Adding cryptographic signatures would be technically straightforward. The question is: **"Do auditors care?"**

### The Auditor Acceptance Question

Cryptographic signatures work in other domains — DocuSign for legal contracts, GitHub for code provenance, AWS CloudTrail for infrastructure audits, Stripe for financial audit trails.

So why not compliance? Cultural lag, not technical limitation.

## When You Need Evidence vs Detection

**Detection-Only is Sufficient For:** Development/staging environments, pre-production testing, low-risk applications.

**Evidence-First is Required For:** SOC 2 / ISO 27001 / FedRAMP compliance, incident response investigations, regulatory audits (HIPAA, PCI DSS, GDPR), supply chain attestation (SLSA Level 3).

**Hybrid Approach (Most Realistic):** Run detection checks continuously. Generate signed attestations periodically. Keep attestations for audit retention. Verify signature chains during audits.

## The Path Forward

Evidence-first security isn't hypothetical — it's implemented and working in supply chain security (SLSA), code signing (Sigstore), and infrastructure logging (CloudTrail).

What's missing: Integration into compliance workflows.

**For GRC Platforms:** Add DSSE signing to evidence collection. Educate auditors on signature verification.

**For Policy-as-Code Tools:** Generate SLSA attestations as output. Support DSSE envelope format.

**For CISOs:** Ask vendors "Do you generate signed attestations?" Pilot evidence-first approaches. Advocate for cryptographic evidence in audit negotiations.

## Conclusion

Checkov tells you what's wrong. Evidence-first security proves you fixed it.

The technical standards exist. The cryptographic precedents work. The academic research confirms feasibility (73.3% effort reduction per arXiv:2502.16344).

What's missing is adoption. The gap between detection-only and evidence-first security is closing — because compliance requirements are finally demanding proof instead of screenshots.

And the next time an auditor asks "Can you prove this control ran?" — you'll have a cryptographic signature instead of a screenshot.

---

*Originally published at [humaine.studio](https://humaine.studio/posts/2026/03/02/evidence-first-vs-detection-only-security/)*

**Technical Resources:** [SLSA Framework](https://slsa.dev) | [in-toto Project](https://in-toto.io) | [Sigstore](https://www.sigstore.dev) | [Mondrian GitHub](https://github.com/miqcie/mondrian)

---

> **Medium Import Instructions:**
> 1. Use Medium's "Import a story" feature with the canonical URL: https://humaine.studio/posts/2026/03/02/evidence-first-vs-detection-only-security/
> 2. Or paste this content manually and set the canonical link in Story Settings
> 3. **Suggested tags:** Cybersecurity, DevSecOps, Compliance, Infrastructure as Code, Zero Trust
> 4. **Suggested publications:** Better Programming, InfoSec Write-ups, The Startup
