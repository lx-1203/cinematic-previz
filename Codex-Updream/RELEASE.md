Codex-native Updream plugin 0.3.3 source maintenance build with automatic Windows installation.

- Separates native Codex browser diagnostics from the independent Edge/Chrome Bridge. Bridge status is never a native-browser connection test.
- Reports a missing browser in the current chat without taking over another chat or automatically requesting extension pairing.
- Uses the documented direct tab/WebMCP route when a wrapper's automatic UI snapshot times out, with a bounded host-call budget.
- The previously published Windows release remains 0.3.2; a local 0.3.3 build is not proof of a published GitHub release.

- Extract the Windows ZIP and double-click install.bat.
- The official Codex CLI registers the local marketplace, installs the plugin, and verifies installed/enabled/version state automatically.
- No Edge developer mode, extension-folder picker, pairing JSON, desktop input or extra Bridge daemon is required.
- Uses the host's supported built-in browser and current site tools; it does not add browser permissions or authentication credentials.
- A successful plugin installation is distinct from a successful live website connection. This chat initially had no browser; after activation, the native WebMCP catalog and current-project read succeeded. UI snapshot binding timed out, so the documented direct tab handle was used. Writes and paid generation were not tested.
- Real Codex CLI installation and reinstallation are tested with isolated configuration, without operating the user's desktop.

Use the Windows x64 ZIP, not the automatically generated source archive. Codex desktop must already be installed; normal website login and host browser permissions still apply.
