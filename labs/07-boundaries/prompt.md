Implement the typed router in `router.py`. Do not parse or block arbitrary shell
strings. Accept only the declared tool names and argument shapes, resolve paths
under the supplied workspace, and reject calls at or above the attempt ceiling.
Reject malformed calls, negative attempt counts, symlink escapes, and paths
outside the workspace. The router only returns an admission decision; it does
not execute a tool. Run the fixture checks.
