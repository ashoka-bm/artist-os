# Artist OS 1.0 rehearsal evidence

`manifest.json` is the tracked index for the six release rehearsals required by
`docs/release-1.0.md`. `rehearsal-run.json` records the exact focused command,
environment, observed result, and digest of the 45 unique records exercised by
that run. A second digest binds the result to the release source surface outside
this evidence directory, avoiding a self-referential hash.

The manifest points at committed, share-safe fixtures and contract tests. It
does not create new artist approvals, waive findings, or claim provider calls.
All rehearsals are dry runs. Generated Works are deliberately not committed;
where a route represents an artifact, its share-safe Output Record carries the
artifact metadata. The Cross-Medium package references only accepted Output
Records.

Run:

```bash
python3 -m unittest tests.test_release_evidence
```

The test validates every listed JSON record against its schema, verifies the
record-set digest and executed supporting-test command, checks the six required
journey names and minimum record chain, validates Album lineage through its
Beat authority, and checks package-to-output integrity.
