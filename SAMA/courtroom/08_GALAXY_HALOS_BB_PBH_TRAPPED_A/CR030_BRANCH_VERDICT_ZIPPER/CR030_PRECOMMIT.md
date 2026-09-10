# CR030_BRANCH_VERDICT_ZIPPER Precommit

        ## Test Type

        ```text
        Fresh Courtroom branch test.
        Not a confirmation audit, retest, or double-check of a previous CR result.
        Source G/QP artifacts are treated as hashed inputs, not as automatic verdict promotion.
        ```

        ## Question

        ```text
        Do the fresh 08 Courtroom tests support a scoped branch PASS while preserving the native radial-law boundary?
        ```

        ## Frozen Sources

        - `cr022_summary`: `C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION\CR022_summary.json` (many-nonzero A root summary)
- `cr023_summary`: `C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR023_BB_PBH_TRAPPED_A_INVENTORY\CR023_summary.json` (BB-PBH inventory summary)
- `cr024_summary`: `C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION\CR024_summary.json` (SPARC residual summary)
- `cr025_summary`: `C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT\CR025_summary.json` (clustered profile summary)
- `cr026_summary`: `C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR026_SEED_FIRST_CLUSTERING_SELECTOR\CR026_summary.json` (seed-first summary)
- `cr027_summary`: `C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD\CR027_summary.json` (hydrogen catchup summary)
- `cr028_summary`: `C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR028_QP042_BARYON_SCAFFOLD_SUPPORT\CR028_summary.json` (QP042 support summary)
- `cr029_summary`: `C:\VS\The_Courtroom\08_GALAXY_HALOS_BB_PBH_TRAPPED_A\CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER\CR029_summary.json` (native radial-law debt summary)

        ## Expected Success Verdict

        ```text
        CR030_PASS_SCOPED_GALAXY_HALO_BB_PBH_TRAPPED_A_BRANCH__RADIAL_LAW_OPEN
        scientific_verdict = PASS
        claim_tier = PASS_SCOPED_BRANCH_WITH_NATIVE_RADIAL_SELECTOR_OPEN
        ```

        ## Boundary Discipline

        ```text
        CR030 is the branch zipper. It gives a scoped PASS for the supported halo chain and explicitly keeps the full native radial law open.
        ```

        ## Pass Discipline

        ```text
        free_parameters_introduced = 0
        wrong controls must not pass as the full packet
        execution_status must be CLEAN
        ```

        ## Rule-9 Line

        ```text
        This test could have falsified: the claim that the fresh 08 branch supports PBH-first/hydrogen-catchup/many-nonzero halo contact while preserving the native radial-law debt.
        ```
