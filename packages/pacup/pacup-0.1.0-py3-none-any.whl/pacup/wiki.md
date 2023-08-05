## A word of advice

First go and read [how Pacup
works](https://github.com/pacstall/pacup#how-does-it-work) to have a general
understanding of Pacup. Understanding that isn't necessary to use `repology`
variable in your pacscripts, but it helps.

This wiki uses `pacup --show-repology <pacscript>` command to show the repology
response.

## Filters and the Filtrate

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

So how will Pacup know which version to consider to be the latest from this
response? The answer is through filtering the response. In fact the above
response itself is a filtrate of the `project` filter.

## Basic Filters

### Project Filter

```bash
repology=("project: brave")
```

The `project` filter is the most basic filter and is a must for your pacscript
to work with Pacup.

The `project` filter just queries repology with it's value (i.e. `brave`) in
the above code example, which results in the above JSON response being sent
back to Pacup. Simple.

### Status Filter

The status filter is an implicit filter that you don't have to specify in the
`repology` array. It's default value is `newest`

Note
