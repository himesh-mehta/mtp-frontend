# Local Toolkits

MTP includes local/no-key toolkits inspired by common agent toolkit patterns:
- calculator
- file
- python
- shell

Use them with:

```python
from mtp import ToolRegistry, register_local_toolkits

registry = ToolRegistry()
register_local_toolkits(registry, base_dir=".")
```

## Discovery + lazy loading

- Tool names are discoverable through loader spec preview.
- Handlers load only when a matching tool is called.

## Toolkit summary

## `calculator.*`
- `calculator.add`
- `calculator.subtract`
- `calculator.multiply`
- `calculator.divide`
- `calculator.sqrt`

## `file.*`
- `file.list_files`
- `file.read_file`
- `file.write_file`
- `file.search_in_files`

Paths are constrained to the configured `base_dir`.

## `python.*`
- `python.run_code`
- `python.run_file`

Execution uses constrained builtins and local scope.

## `shell.*`
- `shell.run_command`

Runs commands in `base_dir` with timeout.

## Risk and policy

Default policy:
- read-only tools: allow
- write tools: allow
- destructive tools: ask

Customize with `RiskPolicy` when creating `ToolRegistry`.
