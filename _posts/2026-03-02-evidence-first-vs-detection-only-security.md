---
layout: post
title: "Evidence-First vs Detection-Only Security: The Gap in Current Tooling"
date: 2026-03-02
categories: [security, compliance]
tags: [evidence-first-security, SLSA, DSSE, attestation, tamper-evident, Checkov]
excerpt: "Checkov tells you what's wrong. But can you prove it was fixed? Here's why detection-only security fails compliance audits — and how evidence-first architecture solves it."
---

Vanta dashboard shows ✅ "Terraform scanning enabled."

Auditor asks: "Prove this scan actually blocked a risky S3 bucket last month."

You provide... a screenshot. The auditor nods, makes a note, moves on.

But here's what neither of you can prove: **whether that control actually ran, or whether the screenshot was fabricated after the fact.**

This is the gap between detection-only security and evidence-first security. One tells you what's wrong. The other proves you fixed it.

## Detection-Only Tools: What They Do Well

Let's start with credit where it's due. Checkov, Terrascan, tfsec, and similar tools are excellent at what they do:

**Policy scanning works:**
- Scans infrastructure-as-code for violations (Terraform, CloudFormation, Kubernetes)
- Identifies security misconfigurations before deployment
- Integrates with CI/CD pipelines
- Provides clear remediation guidance
- Costs $0 for most use cases

**GitHub Actions can block PRs:**
- Runs checks on every pull request
- Prevents risky code from merging
- Shows results inline with code review
- Automates enforcement without manual review

**Dashboards show compliance status:**
- Vanta and Drata aggregate evidence from 100+ SaaS integrations
- Track which controls are enabled
- Monitor policy enforcement trends
- Generate compliance reports for auditors

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

**What auditors want** (but don't always get):
- Tamper-evident proof that can't be forged
- Continuous monitoring instead of periodic snapshots
- Automated evidence generation without human intervention
- Cryptographic verification of authenticity

The gap exists because we're using detection-only tools for a compliance job that requires proof-of-prevention.

## Evidence-First Architecture: What It Means

**Evidence** in security context means: cryptographically signed, tamper-evident proof that a control ran with a specific result.

Not "we enabled Terraform scanning." But "here's cryptographic proof that Terraform scanning ran on commit abc123 at timestamp T, found violation X, and blocked deployment."

### The Technical Standards Already Exist

**SLSA (Supply chain Levels for Software Artifacts):**
- Framework for supply chain attestations
- Defines what evidence should contain
- Levels 1-4 for increasing assurance
- Developed by Google, implemented by GitHub and Red Hat
- Spec: [slsa.dev](https://slsa.dev)

**DSSE (Dead Simple Signing Envelope):**
- Standard format for signed attestations
- Used by in-toto and Sigstore (GitHub's code signing uses Sigstore, which implements DSSE)
- Wraps payload + signature + metadata
- Spec: [github.com/secure-systems-lab/dsse](https://github.com/secure-systems-lab/dsse)

**Hash Chains (Merkle trees):**
- Each attestation references parent hash
- Creates tamper-evident audit trail
- Used by Git, blockchain, certificate transparency logs
- Any modification breaks the chain

**The pieces exist. What's missing is integration into policy-as-code workflows.**

## Technical Deep-Dive: How Mondrian Implemented It

I spent 4 hours building an evidence-first Zero Trust CLI to validate this approach. Here's what the implementation looks like:

### The Policy Engine

Three hard-coded rules for validation:

**1. S3 Public Bucket Detection**
```go
func checkS3PublicBuckets(content string) []CheckResult {
    violations := []CheckResult{}

    // Scan for public ACL patterns
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

This is intentionally simple - the complexity isn't in the policy logic, it's in the evidence generation.

### Evidence Generation (SLSA-Compatible)

The `internal/evidence/` package creates attestations:

```go
// Attestation structure (simplified)
type Attestation struct {
    // SLSA/in-toto compatible fields
    PredicateType string                `json:"predicateType"`
    Subject       []Subject             `json:"subject"`
    Predicate     PolicyCheckPredicate  `json:"predicate"`

    // Mondrian-specific metadata
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

**Key insight:** The attestation contains not just "what violations were found" but "what command ran, in what environment, with what result" - provable facts, not claims.

### DSSE Signature Generation

The `signer.go` implementation uses ECDSA keys:

```go
// Signer handles DSSE signing
type Signer struct {
    keyID      string
    privateKey *ecdsa.PrivateKey
    publicKey  *ecdsa.PublicKey
}

// SignAttestation creates a DSSE-signed envelope
func (s *Signer) SignAttestation(attestation *Attestation) (*SignedAttestation, error) {
    // Serialize attestation to JSON
    payload, err := json.Marshal(attestation)
    if err != nil {
        return nil, err
    }

    // Create DSSE envelope
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

**What this gives you:** Tamper-evident proof that can be verified later. Anyone with the public key can verify:
1. This attestation was signed by Mondrian's key
2. The payload hasn't been modified
3. The signature was created at a specific time

### Hash Chain for Audit Trail

Each attestation references its parent:

```go
// Generate hash for this attestation
func (a *Attestation) GenerateHash() string {
    h := sha256.New()
    h.Write([]byte(a.PredicateType))
    h.Write([]byte(a.Timestamp.String()))
    h.Write([]byte(a.ParentHash)) // Links to previous
    // ... write all fields ...
    return hex.EncodeToString(h.Sum(nil))
}
```

**The result:** A chain where each attestation proves the previous one existed. You can't insert fake attestations retroactively because the hashes won't match.

### GitHub Actions Integration

The practical workflow:

```yaml
name: Mondrian Policy Check

on: [pull_request]

jobs:
  security-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Mondrian Check
        run: |
          mondrian check --rules iac,deploy

      - name: Generate Attestation
        if: success()
        run: |
          mondrian attest --output .mondrian/attestation.json

      - name: Upload Evidence
        uses: actions/upload-artifact@v3
        with:
          name: compliance-evidence
          path: .mondrian/
```

**What this produces:**
- Blocks risky PRs (like Checkov)
- PLUS: Generates signed proof that the check ran
- Stored as artifact for auditor review

## The Implementation Gap: Why This Isn't a Product Yet

The technical pieces work. So why isn't this the standard approach?

### Vanta/Drata Already Solve 80%

Current GRC platforms automated evidence collection:
- 100+ SaaS integrations (GitHub, AWS, Okta, etc.)
- Continuous monitoring instead of point-in-time
- Dashboard showing compliance status
- Audit report generation

**Cost reduction: $400K traditional process → $200K with automation.**

Adding cryptographic signatures to these platforms would be technically straightforward. The question isn't "Can it be done?" - it's **"Do auditors care?"**

### The Auditor Acceptance Question

**Cryptographic signatures work in other domains:**
- **DocuSign:** Courts accept electronic signatures for legal contracts (DocuSign's Qualified Electronic Signature tier meets the highest legal standards; standard e-signatures have faced some court challenges)
- **GitHub:** Signed commits prove code provenance
- **AWS CloudTrail:** Crypto-verified logs for infrastructure audits
- **Financial SaaS:** Stripe, QuickBooks use crypto audit trails

**So why not compliance?** Cultural lag, not technical limitation.

Auditors are trained to review screenshots and logs. Cryptographic verification requires different skills. The industry needs to shift from "human review of evidence" to "automated verification of signatures."

### What It Would Take to Productionize

**1. Auditor Education:**
- Training on cryptographic verification
- Standards bodies endorsing SLSA/DSSE for compliance
- Example audit reports using signed attestations

**2. Integration with Existing Platforms:**
- Vanta/Drata adding DSSE signing to their evidence collection
- Policy-as-code tools (Checkov, OPA) generating attestations
- GitHub/GitLab/Azure DevOps native attestation support

**3. Standards Adoption:**
- SLSA Level 3+ becoming requirement for enterprise sales
- SOC 2 auditors accepting signed attestations as primary evidence
- Industry consortiums (Cloud Security Alliance, CNCF) promoting standards

**4. Key Management Infrastructure:**
- Where do signing keys live? (HSM, cloud KMS, Sigstore?)
- How do auditors verify signatures? (Public key infrastructure)
- What's the key rotation process?

## When You Need Evidence vs Detection

Not every environment needs evidence-first security:

### Detection-Only is Sufficient For:
- **Development/staging environments** - Fast feedback matters more than proof
- **Pre-production testing** - Catching issues early, not proving they were caught
- **Low-risk applications** - Internal tools, prototypes, non-production systems

### Evidence-First is Required For:
- **SOC 2 / ISO 27001 / FedRAMP compliance** - Auditors need tamper-evident proof
- **Incident response investigations** - "What controls were actually running when breach occurred?"
- **Regulatory audits** - HIPAA, PCI DSS, GDPR require documented evidence
- **Supply chain attestation** - SLSA Level 3 requires cryptographic build provenance

### Hybrid Approach (Most Realistic):
- Run detection checks continuously (fast feedback)
- Generate signed attestations periodically (compliance checkpoints)
- Keep attestations for audit retention period (varies by framework; SOX requires 7 years, SOC 2 has no fixed retention requirement)
- Verify signature chains during audits

## Academic Support: This Approach Works

ML-based compliance automation research (arXiv:2502.16344) shows:
- **73.3% reduction** in manual compliance effort
- **Process duration: 7 days → 1.5 days**
- Automated evidence generation is feasible at scale

The technology isn't the bottleneck. **Market adoption is.**

## Example: Full Evidence Chain

Here's what a complete evidence artifact looks like:

```json
{
  "envelope": {
    "payloadType": "application/vnd.mondrian.policy-check+json",
    "payload": "<base64-encoded attestation>",
    "signatures": [{
      "keyid": "mondrian-prod-key-2025",
      "sig": "<base64-encoded ECDSA signature>"
    }]
  },
  "metadata": {
    "keyId": "mondrian-prod-key-2025",
    "timestamp": "2025-09-14T18:30:45Z",
    "publicKey": "<PEM-encoded public key>"
  }
}
```

**To verify this evidence, an auditor:**
1. Decodes the base64 payload
2. Verifies the ECDSA signature using the public key
3. Checks the timestamp is within acceptable range
4. Validates the hash chain (this attestation → parent → grandparent)
5. Confirms no attestations are missing from the chain

**What they CAN'T do:** Forge this evidence. The cryptography makes it mathematically infeasible.

## The Path Forward

Evidence-first security isn't hypothetical - it's implemented and working in supply chain security (SLSA), code signing (Sigstore), and infrastructure logging (CloudTrail).

**What's missing:** Integration into compliance workflows.

**Specific next steps for the industry:**

**For GRC Platforms (Vanta, Drata):**
- Add DSSE signing to evidence collection
- Offer "cryptographically verified" badge for controls
- Educate auditors on signature verification

**For Policy-as-Code Tools (Checkov, OPA):**
- Generate SLSA attestations as output
- Support DSSE envelope format
- Provide reference implementations

**For Cloud Providers (AWS, Azure, GCP):**
- Native attestation support in CI/CD (GitHub Actions, GitLab, Azure Pipelines)
- Managed signing keys in cloud KMS
- Verification APIs for auditors

**For Standards Bodies (CSA, CNCF, ISO):**
- Endorse SLSA/DSSE for compliance evidence
- Update audit frameworks to accept cryptographic verification
- Train auditors on signature verification processes

**For CISOs and Security Leaders:**
- Ask vendors: "Do you generate signed attestations?"
- Pilot evidence-first approaches in non-critical systems
- Advocate for cryptographic evidence in audit negotiations

## Conclusion

Checkov tells you what's wrong. Evidence-first security proves you fixed it.

The technical standards exist (SLSA, DSSE, hash chains). The cryptographic precedents work (DocuSign, GitHub, CloudTrail). The academic research confirms feasibility (73.3% effort reduction).

**What's missing is adoption.** Auditors need training. Platforms need integration. Standards bodies need endorsement.

The gap between detection-only and evidence-first security is closing. Not because the technology is new - but because compliance requirements are finally demanding proof instead of screenshots.

Consider evidence requirements early in your security architecture. The cost to retrofit is high. The cost to build it in from day one is negligible.

And the next time an auditor asks "Can you prove this control ran?" - you'll have a cryptographic signature instead of a screenshot.

---

**Related Reading:**
- [Why I Built and Shelved a Zero Trust Tool](/posts/2026/03/02/experiments-building-grc-tool-weekend/) - The decision framework behind Mondrian's archive
- [The Security Poverty Line](/posts/2026/03/02/security-poverty-line/) - Economic analysis of compliance costs

**Technical Resources:**
- [SLSA Framework](https://slsa.dev) - Supply chain attestation standards
- [in-toto Project](https://in-toto.io) - Attestation format and tools
- [Sigstore](https://www.sigstore.dev) - Free signing service for open source
- [Mondrian GitHub](https://github.com/miqcie/mondrian) - Archived reference implementation
- [arXiv:2502.16344](https://arxiv.org/abs/2502.16344) - ML-based compliance automation research

**For advisory/consulting inquiries:** [Eagle Ridge Advisory](https://eagleridge.io) | [Humaine Studio](https://humaine.studio)
