# License Headers for Vendored Templates

When vendoring, put a license/attribution block at the top of `template/<pkg>.typ`. The exact wording depends on the upstream license — most require retention of the copyright notice and (sometimes) the full license text.

## Quick decision

| Upstream license | Minimum required in the vendored file |
|---|---|
| MIT | Copyright line + one-line license name. Keep the upstream `LICENSE` file if you want a belt-and-suspenders copy. |
| BSD-2-Clause / BSD-3-Clause | Copyright line + full clauses. Usually worth copying the upstream `LICENSE` verbatim. |
| Apache-2.0 | Copyright line + "Licensed under Apache-2.0" + NOTICE file contents if upstream ships one. |
| MPL-2.0 | Copyright line + MPL header block (3 lines). |
| CC-BY-4.0 | Attribution to author + link to the license. |
| Unlicensed / no LICENSE file | **Do not vendor.** Ask the author or don't use it. |

## Templates

Pick the block matching upstream. Keep it as a top-of-file comment in `template/<pkg>.typ`.

### MIT (most common)

```typ
// Vendored from https://github.com/<owner>/<pkg> @ tag <tag>.
// MIT License — Copyright (c) <year> <author>.
// Trimmed: <sections removed>. Fixed: <version-drift changes>.
```

If you want to be extra safe, duplicate the full MIT text as a comment block. Not strictly required since MIT's "copyright notice and this permission notice" clause is short, but it silences any ambiguity.

### BSD-3-Clause

```typ
// Vendored from https://github.com/<owner>/<pkg> @ tag <tag>.
// BSD 3-Clause License — Copyright (c) <year> <author>. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice,
//    this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright notice,
//    this list of conditions and the following disclaimer in the documentation
//    and/or other materials provided with the distribution.
// 3. Neither the name of the copyright holder nor the names of its contributors
//    may be used to endorse or promote products derived from this software
//    without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED. [...]
```

BSD-2-Clause is the same minus clause 3.

### Apache-2.0

```typ
// Vendored from https://github.com/<owner>/<pkg> @ tag <tag>.
// Copyright <year> <author>.
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//     http://www.apache.org/licenses/LICENSE-2.0
// Trimmed: <sections removed>. Fixed: <version-drift changes>.
```

If the upstream ships a `NOTICE` file, copy its contents verbatim into a second comment block below — Apache-2.0 requires downstream redistribution to carry the NOTICE.

### MPL-2.0

```typ
// This Source Code Form is subject to the terms of the Mozilla Public License,
// v. 2.0. If a copy of the MPL was not distributed with this file, You can
// obtain one at http://mozilla.org/MPL/2.0/.
//
// Vendored from https://github.com/<owner>/<pkg> @ tag <tag>.
// Copyright <year> <author>.
// Trimmed: <sections removed>.
```

MPL-2.0 is **file-level copyleft**: if you modify this file (which vendoring does), your modifications must stay MPL-2.0. Your resume source doesn't have to be MPL, but the vendored template file does.

### CC-BY-4.0 (rare, usually on documentation or style templates)

```typ
// Vendored from https://github.com/<owner>/<pkg> @ tag <tag>.
// Based on work by <author>, licensed under CC BY 4.0.
// https://creativecommons.org/licenses/by/4.0/
// Modifications by <your name>, <year>.
```

## Anti-patterns

- **"Adapted from" without names.** Attribution has to name the upstream author. "Based on a Typst template" is not attribution.
- **Stripping the license comment in a later refactor.** The header is load-bearing; do not delete it when trimming. The skill's guardrails say so for a reason.
- **Relicensing upstream code.** You can't. Your modifications to a BSD-3 file are yours, but the composite file has to retain BSD-3 terms.
- **Vendoring from a repo with no LICENSE file.** "Probably MIT because it's on GitHub" is not a legal basis. Open an issue asking the author to clarify, or don't vendor.

## Concrete example (as shipped)

See `template/modern-cv.typ` at this repo's root — its header is:

```typ
// Vendored from https://github.com/ptsouchlos/modern-cv @ tag 0.8.0.
// MIT License — Copyright (c) 2024 Paul Tsouchlos.
// Trimmed: cover-letter templates removed; linguify dropped (English inlined);
// `type(x) == "string"` updated to `type(x) == str` for typst 0.13+.
```

That format is the canonical MIT pattern. Copy it for the next MIT vendor.
