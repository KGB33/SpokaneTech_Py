CI/CD is handled by [Dagger](https://docs.dagger.io/zenith/), specifically version `v0.9.8`.

# Running CI/CD

To run the CI, you'll need the [`dagger`
cli](https://docs.dagger.io/zenith/user/install) and
[Docker](https://docs.docker.com/) installed. 


Once both are installed, you can list the available functions 
by running `dagger -m ci functions` in the root of this repo.

```
❯ dagger -m ci functions
✔ dagger functions [0.00s]
   Name     Description
   bandit   Runs bandit on the provided directory.
   debug    Builds a container without starting the web server for debugging.
   lint     Checks that the directory passes various linters,
   local    Used to run the website in a production **like** environment.
   prod     Builds a production-ready container.
⧗ 3.00s ✔ 161 ∅ 31
```

Then, to run a function - like `bandit` - use `dagger call`.

```
❯ dagger -m ci call bandit --dir .
...
```

The required flags for a function (in this case `--dir .`), can be viewed using
`dagger -m ci call bandit --help`.

Lastly, by default `dagger` only shows the currently running step, to show all the steps, 
use `--focus=false`; i.e. `dagger -m ci --focus=false call lint --dir .`.


## Advanced Usage

Dagger provides two methods to debug your containers - `up` and `shell`.

`up` is used to run a service. For example, `dagger -m ci call local --dir ./ up --native`, runs the website
in a container, and tunnels the exposed ports. 

`shell` opens an interactive terminal in the container. `dagger -m ci call debug --dir ./ shell`. 

# Contributing to CI/CD

First, create and activate your Python virtual environment as described in the README. 
Then, move into the `ci` directory - almost all commands should be run this directory. 

Documentation can be found [here](https://docs.dagger.io/zenith/developer/python/419481/quickstart),
and the Python reference is [here](https://dagger-io.readthedocs.io/en/sdk-python-v0.9.8/)

## IDE Autocomplete

Optionally, for autocomplete, run `dagger mod sync` to generate the SDK code,
then `pip install -e sdk/`.
