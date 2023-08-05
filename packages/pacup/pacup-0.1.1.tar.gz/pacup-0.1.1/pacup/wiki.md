## A word of advice

First go and read [how Pacup
works](https://github.com/pacstall/pacup#how-does-it-work) to have a general
understanding of Pacup. Understanding that isn't necessary to use `repology`
variable in your pacscripts, but it helps.

This wiki uses `pacup --show-repology <pacscript>` command to show the parsed
repology response.

## Filters and the Filtrate

Let's look at an example of the `repology` var for
`brave-browser-bin.pacscript`

```bash
repology=("project: brave")
```


Pacup uses the [Repology API](https://repology.org/api) to get the latest
versions of your pacscript. Here's how an API response from the API looks like
(truncated) for the `brave` project.

```json
[
    {
        "repo": "chaotic-aur",
        "srcname": "brave-nightly-bin",
        "binname": "brave-nightly-bin",
        "visiblename": "brave-nightly-bin",
        "version": "1.38.53",
        "licenses": [
            "MPL2"
        ],
        "summary": "Web browser that blocks ads and trackers by default (nightly binary release).",
        "status": "ignored",
        "origversion": "1.38.53-1"
    },
    {
        "repo": "aur",
        "srcname": "brave",
        "binname": "brave",
        "visiblename": "brave",
        "version": "1.29.79",
        "maintainers": [
            "alerque@aur"
        ],
        "licenses": [
            "custom"
        ],
        "summary": "A web browser that stops ads and trackers by default",
        "status": "outdated",
        "origversion": "1.29.79-1"
    },
    ...
    ...
    ...
    {
        "repo": "sabayon_for_gentoo",
        "srcname": "www-client/brave-bin",
        "visiblename": "www-client/brave-bin",
        "version": "1.3.114",
        "maintainers": [
            "fallback-mnt-sabayon@repology"
        ],
        "categories": [
            "www-client"
        ],
        "status": "legacy",
        "origversion": null
    },
    {
        "repo": "sabayon_for_gentoo",
        "srcname": "www-client/brave-bin",
        "visiblename": "www-client/brave-bin",
        "version": "1.15.75",
        "maintainers": [
            "fallback-mnt-sabayon@repology"
        ],
        "categories": [
            "www-client"
        ],
        "status": "outdated",
        "origversion": null
    }
]
```

Do look here for a [rendered
version](https://repology.org/project/brave/versions) of the API response.

So how will Pacup know which version to consider to be the latest from this
response? The answer is through filtering the response. In fact the above
response itself is a filtrate of the `project` filter.

### Basic Filters

#### Project Filter

```bash
repology=("project: brave")
```

The `project` filter is the most basic filter and is a must for your pacscript
to work with Pacup.

The `project` filter just queries repology with it's value (i.e. `brave`) in
the above code example, which results in the above JSON response being sent
back to Pacup.

When executing `pacup --show-repology <pacscript>` this filter would be absent
from the `Filters` panel.


#### Status Filter

The status filter is an implicit filter that you don't have to specify in the
`repology` array. It's default value is `newest`.

<details>
    <summary>Parsed Repology Data</summary>

    ╭────────────────────────────────────── Repology for brave ──────────────────────────────────────╮
    │ ╭───────────────────────────────────────── Filters ──────────────────────────────────────────╮ │
    │ │ {'status': 'newest'}                                                                       │ │
    │ ╰────────────────────────────────────────────────────────────────────────────────────────────╯ │
    │ ╭───────────────────────────────────────── Filtrate ─────────────────────────────────────────╮ │
    │ │ [                                                                                          │ │
    │ │ │   {                                                                                      │ │
    │ │ │   │   'repo': 'aur',                                                                     │ │
    │ │ │   │   'srcname': 'brave-bin',                                                            │ │
    │ │ │   │   'binname': 'brave-bin',                                                            │ │
    │ │ │   │   'visiblename': 'brave-bin',                                                        │ │
    │ │ │   │   'version': '1.36.116',                                                             │ │
    │ │ │   │   'maintainers': ['alerque@aur'],                                                    │ │
    │ │ │   │   'licenses': ['BSD', 'custom:chromium', 'MPL2'],                                    │ │
    │ │ │   │   'summary': 'Web browser that blocks ads and trackers by default (binary release)', │ │
    │ │ │   │   'status': 'newest',                                                                │ │
    │ │ │   │   'origversion': '1:1.36.116-1'                                                      │ │
    │ │ │   },                                                                                     │ │
    │ │ │   {                                                                                      │ │
    │ │ │   │   'repo': 'chaotic-aur',                                                             │ │
    │ │ │   │   'srcname': 'brave-bin',                                                            │ │
    │ │ │   │   'binname': 'brave-bin',                                                            │ │
    │ │ │   │   'visiblename': 'brave-bin',                                                        │ │
    │ │ │   │   'version': '1.36.116',                                                             │ │
    │ │ │   │   'licenses': ['MPL2', 'BSD', 'custom:chromium'],                                    │ │
    │ │ │   │   'summary': 'Web browser that blocks ads and trackers by default (binary release)', │ │
    │ │ │   │   'status': 'newest',                                                                │ │
    │ │ │   │   'origversion': '1:1.36.116-1'                                                      │ │
    │ │ │   },                                                                                     │ │
    │ │ │   {                                                                                      │ │
    │ │ │   │   'repo': 'nix_stable_21_11',                                                        │ │
    │ │ │   │   'name': 'brave',                                                                   │ │
    │ │ │   │   'visiblename': 'brave',                                                            │ │
    │ │ │   │   'version': '1.36.116',                                                             │ │
    │ │ │   │   'maintainers': [                                                                   │ │
    │ │ │   │   │   'urban.skudnik@gmail.com',                                                     │ │
    │ │ │   │   │   'rhtbot@protonmail.com',                                                       │ │
    │ │ │   │   │   'grimsleepless@protonmail.com',                                                │ │
    │ │ │   │   │   'nasirhussainm14@gmail.com'                                                    │ │
    │ │ │   │   ],                                                                                 │ │
    │ │ │   │   'licenses': ['MPL-2.0'],                                                           │ │
    │ │ │   │   'summary': 'Privacy-oriented browser for Desktop and Laptop computers',            │ │
    │ │ │   │   'status': 'newest',                                                                │ │
    │ │ │   │   'origversion': None                                                                │ │
    │ │ │   },                                                                                     │ │
    │ │ │   {                                                                                      │ │
    │ │ │   │   'repo': 'pclinuxos',                                                               │ │
    │ │ │   │   'srcname': 'brave',                                                                │ │
    │ │ │   │   'visiblename': 'brave',                                                            │ │
    │ │ │   │   'version': '1.36.116',                                                             │ │
    │ │ │   │   'summary': 'Brave Web Browser',                                                    │ │
    │ │ │   │   'categories': ['Networking/WWW'],                                                  │ │
    │ │ │   │   'status': 'newest',                                                                │ │
    │ │ │   │   'origversion': '1.36.116-1pclos2022'                                               │ │
    │ │ │   },                                                                                     │ │
    │ │ │   {                                                                                      │ │
    │ │ │   │   'repo': 'solus',                                                                   │ │
    │ │ │   │   'srcname': 'brave',                                                                │ │
    │ │ │   │   'binname': 'brave',                                                                │ │
    │ │ │   │   'visiblename': 'brave',                                                            │ │
    │ │ │   │   'version': '1.36.116',                                                             │ │
    │ │ │   │   'maintainers': ['algent@protonmail.com'],                                          │ │
    │ │ │   │   'licenses': ['GPL-2.0-or-later', 'GPL-3.0-or-later', 'MPL-2.0'],                   │ │
    │ │ │   │   'summary': 'A browser focused on privacy that blocks ads and trackers by default', │ │
    │ │ │   │   'categories': ['network.web.browser'],                                             │ │
    │ │ │   │   'status': 'newest',                                                                │ │
    │ │ │   │   'origversion': None                                                                │ │
    │ │ │   },                                                                                     │ │
    │ │ │   {                                                                                      │ │
    │ │ │   │   'repo': 'solus',                                                                   │ │
    │ │ │   │   'srcname': 'brave',                                                                │ │
    │ │ │   │   'binname': 'brave-dbginfo',                                                        │ │
    │ │ │   │   'visiblename': 'brave-dbginfo',                                                    │ │
    │ │ │   │   'version': '1.36.116',                                                             │ │
    │ │ │   │   'maintainers': ['algent@protonmail.com'],                                          │ │
    │ │ │   │   'licenses': ['GPL-2.0-or-later', 'GPL-3.0-or-later', 'MPL-2.0'],                   │ │
    │ │ │   │   'summary': 'Debug symbols for brave',                                              │ │
    │ │ │   │   'categories': ['debug'],                                                           │ │
    │ │ │   │   'status': 'newest',                                                                │ │
    │ │ │   │   'origversion': None                                                                │ │
    │ │ │   }                                                                                      │ │
    │ │ ]                                                                                          │ │
    │ ╰────────────────────────────────────────────────────────────────────────────────────────────╯ │
    │ ╭────────────────────────────── Selected version (most common) ──────────────────────────────╮ │
    │ │ 1.36.116                                                                                   │ │
    │ ╰────────────────────────────────────────────────────────────────────────────────────────────╯ │
    ╰────────────────────────────────────────────────────────────────────────────────────────────────╯
</details>


For most of your pacscripts only using the `project` filter would be
sufficient, but for more complicated pacscripts you would have to delve into
the advanced filters.

### Advanced Filters

### Repo Filter

```bash
repology=("project: brave" "repo: aur")
```

The `repo` filter's value is  the name of the repository you want to filter, so
applying the above filter would result in the filtrate only containing the
packages from `aur`.

<details>
    <summary>Parsed Repology Data</summary>

    ╭────────────────────────────────────── Repology for brave ──────────────────────────────────────╮
    │ ╭───────────────────────────────────────── Filters ──────────────────────────────────────────╮ │
    │ │ {'repo': 'aur', 'status': 'newest'}                                                        │ │
    │ ╰────────────────────────────────────────────────────────────────────────────────────────────╯ │
    │ ╭───────────────────────────────────────── Filtrate ─────────────────────────────────────────╮ │
    │ │ [                                                                                          │ │
    │ │ │   {                                                                                      │ │
    │ │ │   │   'repo': 'aur',                                                                     │ │
    │ │ │   │   'srcname': 'brave-bin',                                                            │ │
    │ │ │   │   'binname': 'brave-bin',                                                            │ │
    │ │ │   │   'visiblename': 'brave-bin',                                                        │ │
    │ │ │   │   'version': '1.36.116',                                                             │ │
    │ │ │   │   'maintainers': ['alerque@aur'],                                                    │ │
    │ │ │   │   'licenses': ['BSD', 'custom:chromium', 'MPL2'],                                    │ │
    │ │ │   │   'summary': 'Web browser that blocks ads and trackers by default (binary release)', │ │
    │ │ │   │   'status': 'newest',                                                                │ │
    │ │ │   │   'origversion': '1:1.36.116-1'                                                      │ │
    │ │ │   }                                                                                      │ │
    │ │ ]                                                                                          │ │
    │ ╰────────────────────────────────────────────────────────────────────────────────────────────╯ │
    │ ╭────────────────────────────── Selected version (most common) ──────────────────────────────╮ │
    │ │ 1.36.116                                                                                   │ │
    │ ╰────────────────────────────────────────────────────────────────────────────────────────────╯ │
    ╰────────────────────────────────────────────────────────────────────────────────────────────────╯
</details>

### Subrepo Filter

```bash
repology=("project: brave" "subrepo: hasufell" "status: outdated")
```

NOTE: I've used `status: outdated` filter here as the packages from the
`newest` filtrate didn't have a `subrepo` property to filter.
