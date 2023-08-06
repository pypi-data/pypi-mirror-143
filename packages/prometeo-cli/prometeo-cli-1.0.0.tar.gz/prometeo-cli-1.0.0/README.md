# prometeo-cli

CLI Tool for communicating to bankings institutions through Prometeo Open Banking API.


# Setup

The CLI allows you to configure multiple institutions accounts and environments depending if you are working with `production`, `testing` or `sandbox`.

- First of all set the environment variable `PROMETEO_ENVIRONMENT` with your working environment
- Run it with `python -m pmo COMMAND [ARGS]`

When running it the script will check if the directory `~/.prometeo/` and the file `~/.prometeorc` exists.
The `~/.prometeorc` file stores the api session key.

In the `~/.prometeo/` directory stores two configurations files:

- `configuration.ini` stores the different environments configuration
- `credentials.ini` stores the credentials of the institutions (The passwords are encrypted  :stuck_out_tongue_winking_eye:)

# Available commands

### `config [OPTIONS]`
There are two options `--credential` for configuring a new set of credentials, and the `--environment` for a new env.

### `login [OPTIONS]`
Used for starting a new session

Options:

- `--provider` specifies the set of credentials to user (You can set a default provider with the `PROMETEO_PROVIDER` environment variable)
- `--interactive` to login interactively :smiley:

**logout**
Terminates the current session

**accounts**
Lists your banking accounts details

**cards**
List your credit cars details

**movements [OPTIONS]**
Lists your movements

Options
*All the options are required*
- `(-a, --account) or (-c --card)` sets the origin of the movements
- `(-cu, --currency)` As the credit cards movements might be in different currency you must specify one in ISO 4217
- `--start-date` sets the start of the range of the movements to get in  `%Y-%m-%d` format
- `--end-date` sets the end of the range of the movements to get in  `%Y-%m-%d` format

**providers**
List the available providers and their information (id, country and name)

