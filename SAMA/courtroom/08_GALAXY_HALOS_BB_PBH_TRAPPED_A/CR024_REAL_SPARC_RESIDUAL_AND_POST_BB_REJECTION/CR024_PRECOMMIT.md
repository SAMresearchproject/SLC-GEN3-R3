# CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION Precommit

        ## Test Type

        ```text
        Fresh Courtroom branch test.
        Not a confirmation audit, retest, or double-check of a previous CR result.
        Source G/QP artifacts are treated as hashed inputs, not as automatic verdict promotion.
        ```

        ## Question

        ```text
        Does real SPARC data show a large outer halo residual while the post-BB-only PBH envelope remains far too small to be the full halo source?
        ```

        ## Frozen Sources

        - `g392_summary`: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G392_REAL_SPARC_PBH_HALO_INVENTORY_TEST\G392_summary.json` (real SPARC residual summary)
- `g393_summary`: `C:\VS\Stam_model-A-v1.0\tests\Substrate\G393_PBH_HALO_FORWARD_STACK_SELECTOR\G393_summary.json` (forward stack and post-BB-only budget summary)

        ## Expected Success Verdict

        ```text
        CR024_PASS_REAL_SPARC_RESIDUAL_POST_BB_ONLY_REJECTED
        scientific_verdict = PASS
        claim_tier = PASS_REAL_DATA_HALO_RESIDUAL_AND_CONTROL_REJECTION
        ```

        ## Boundary Discipline

        ```text
        CR024 is a real-data contact test. It does not close the full radial halo law; it locks the SPARC residual and rejects the post-BB-only control as a full-halo explanation.
        ```

        ## Pass Discipline

        ```text
        free_parameters_introduced = 0
        wrong controls must not pass as the full packet
        execution_status must be CLEAN
        ```

        ## Rule-9 Line

        ```text
        This test could have falsified: the claim that SPARC rotation data leaves a large halo residual and that the bounded post-BB/window PBH envelope is insufficient as the complete source.
        ```
