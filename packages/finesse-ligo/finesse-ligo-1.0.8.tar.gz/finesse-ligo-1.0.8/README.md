# finesse-ligo

Finesse 3.0 LIGO models, tools, and data.

## Installation
TBA

## Usage and Contributing
This package includes top-level tools and models for simulating LIGO in Finesse 3. Individal simulations that you perform should be stored elsewhere, such as the `finesse_playground` reposistory. Your scripts should just import this package.

If you want to contribute any changes or code to this project then it must be done via a merge request. Merge requests must pass all tests before being merged.

## Support
Please post an issue if you are experiencing any bugs, problems, or feature requests. `https://chat.ligo.org/ligo/channels/finesse` can also be used for broader discussion on Finesse and modelling LIGO with it.

## License
All code here is distributed under GPL v3.

## Packaging

The `finesse-ligo` is automatically uploaded to pypi when new tags are pushed to `main`. Tags must be annotated and be in the semantic versioning form `MAJOR.MINOR.PATCH`:

- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwards compatible manner, and
- PATCH version when you make backwards compatible bug fixes.

Only maintainers can push tags to the main branch.