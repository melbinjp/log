---
title: When an MCP result loses its error flag
description: A missing error flag made an unknown tool result look successful. The rigout repair rejects that result and shows what arrived.
date: 2026-11-22
slug: mcp-missing-error-flag
---
A tool call can fail while its wrapper reports success. In rigout, one cause was a result without a recognised error flag.

[rigout](https://github.com/melbinjp/rigout) gives authorised AI agents access to a machine through MCP.
It supports command execution, processes and files. A false success result can send the next step in the wrong direction.

The defect was in the result adapter. MCP used `isError` in one supported version and `is_error` in another.
The adapter checked both names. If neither existed, its fallback returned `None`. Python converts `None` to `False`.
The wrapper therefore treated an unknown result as a successful call.

The [merged repair](https://github.com/melbinjp/rigout/pull/66) gives an absent field its own value.
The adapter reads either known field. If both fields are absent, it raises `UnknownResultShapeError` and includes a preview of the result.

A field that exists with a value of `None` remains distinct from an absent field.
This preserves the supported result behaviour while rejecting an unknown format.

The [implementation](https://github.com/melbinjp/rigout/blob/6bc40fc/src/rigout/results.py) and
[regression tests](https://github.com/melbinjp/rigout/blob/6bc40fc/tests/unit/test_result_shape.py) show the exact cases.
The tests cover both field names, true and false values, an explicit `None`, and an object with neither field.

For a tool adapter, the useful question is simple: what happens when the response changes shape?
Test that case directly. A familiar success response cannot prove how an unfamiliar response will behave.

This repair shipped in [rigout 0.4.1 on PyPI](https://pypi.org/project/rigout/0.4.1/).

If your team needs help with an agent integration or an existing automation, send the workflow, the observed failure and the required result to
[melbinjpaulose@gmail.com](mailto:melbinjpaulose@gmail.com?subject=Agent%20integration%20or%20automation).
For a role, include the scope, location and assessment format. I am based in Kozhikode, India.
