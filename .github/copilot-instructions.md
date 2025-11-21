# Copilot / AI assistant guidance for compmethods-yw2247

Quick orientation
- This repository is a collection of course problem sets organized under top-level directories `problem_set_0` .. `problem_set_4`.
- Most work is in Jupyter notebooks (e.g., `problem_set_0/exercise1.ipynb`) and small Python scripts (notably `problem_set_3/*.py` and `problem_set_4/exercise1.py` + notebooks).
- Data files live under each problem set's `data/` subfolder; plots are under `plots/` or `figs/`.

What to modify and what to avoid
- Primary edits: exercises' notebooks and the small supporting `.py` files in `problem_set_3` and `problem_set_4`.
- Avoid changing raw data files in `data/` unless the task explicitly requires data preprocessing; do not modify `plots/` images.

Build / run / test workflows
- There is no central build system (no `package.json`, `setup.py`, or Makefile). Typical workflows are:
  - Open the relevant `exerciseX.ipynb` in Jupyter and run cells.
  - For Python scripts, run `python3 problem_set_3/exercise1.py` (or the specific script path).
- When adding dependencies, prefer a minimal `requirements.txt` at the repo root and put import examples in the notebook header cells.

Project-specific conventions
- Use relative paths to data inside each `problem_set_*` directory (e.g., `data/pset0-population.db`). Notebooks expect local relative paths.
- Plots are saved into the `plots/` or `figs/` directory under each problem set—follow existing filename patterns when generating new figures.
- Random seeds: code often sets seeds for reproducibility (see `problem_set_4/exercise1.ipynb` where `random.seed(123)` is used). Preserve or expose seeds when writing tests or examples.

Patterns and examples from the codebase
- Finite-difference gradient examples: `problem_set_4/exercise1.ipynb` implements `err(a,b)` calling an external error function (HTTP), `grad_forward` using forward finite difference, `GDConfig` dataclass, `gradient_descent` and a multi-start driver `run_multistart()`.
  - When editing optimization code, keep the projection to [0,1] and the finite-difference h-handling at boundaries.
- Notebook style: mix of explanatory markdown and runnable cells; keep markdown explanations when adding or changing algorithms.

Integration points and external dependencies
- Some notebooks call external HTTP endpoints (example: `http://ramcdougal.com/cgi-bin/error_function.py?a=...` in `problem_set_4/exercise1.ipynb`). Be mindful that these calls may fail offline or be rate-limited. Provide local fallback stubs or mocks for offline testing.
- No declared dependency manager is present. If you add network or third-party packages, include them in `requirements.txt`.

Editing and PR guidance
- Keep changes per problem set small and self-contained.
- When updating a notebook, run the key cells to ensure no runtime errors; include a short note in the notebook header about any new dependencies.

Notes for AI agents
- Prefer small, deterministic edits: update function implementations, add tests or helper scripts, or improve docstrings and markdown explanations.
- If making network-related changes, add a short offline mock in the same directory (e.g., a local `error_function_stub.py`) and update the notebook to use it behind a simple `if` flag.
- When refactoring across multiple files, search for uses of a function before changing its signature. Notebooks may call scripts by relative import or by running as scripts.

If anything here looks incomplete or you want more detail (tests, a requirements file, or example run commands for a specific notebook), tell me which problem set or file to prioritize and I'll expand this guidance.