# devsetup
a tool for managing consistent setup for your development environment.

## Development

This project uses `poetry` and `direnv`

```bash

# install direnv (macos) - https://formulae.brew.sh/formula/direnv#default
# other OSs - https://direnv.net/docs/installation.html
brew install direnv
# if bash rc exists, add the shell hook
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
# if zsh rc exists, add the shell hook
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

# clone the repo
git clone https://github.com/nsheaps/devsetup.git
direnv allow ./devsetup
cd devsetup # activates direnv

# install poetry
poetry install

# run things
cd ~/src/devsetup
devsetup <command> # alias to poetry run python ./src/main.py <command>
```

### Linting

`npx mega-linter-runner --flavor cupcake`


## The `devsetup` command

Uses `$HOME/.config/devsetup/` for any needed configuration files.

| command                                                | description                                                                                                                                                                                                                                      |
|--------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `devsetup set-tap <tap>`                               | sets the tap to use for installing software. This is the tap that will be used when running `devsetup install <formula>`.                                                                                                                        |
| `devsetup get-tap`                                     | prints the current tap. eg `nsheaps/devsetup`                                                                                                                                                                                                    |
| `devsetup install <formula>`<br>`devsetup i <formula>` | installs a formula from this tap, an alias for `brew install $(devsetup get-tap)/<formula>`. This is to avoid trying to pin this tap ([deprecated](https://github.com/Homebrew/brew/pull/5925)) when installing your locked versions of software |
| `devsetup upgrade-all` | updates the local clone of this tap (`devsetup update`), then upgrades all software installed from it (list, filter by `$(devsetup get-tap)/.*, run`brew upgrade <formula..>`), also updates devsetup from it's origin tap. |
| `devsetup upgrade devsetup`<br>`devsetup u devsetup` | Updates devsetup from it's origin tap. |
| `devsetup upgrade <formula>`<br>`devsetup u <formula>` | alias for `brew upgrade $(devsetup get-tap)/<formula>`, always upgrades `devsetup` even if from another tap. |
| `devsetup update` | Alias for `$(cd $(brew --repository $(devsetup get-tap)) && git pull)`. This is to avoid updating other taps. **Note:** doesn't change a branch if checked out to a non-default branch. |
| `devsetup outdated` | Alias for `brew outdated $(devsetup get-tap)/.*` |
| `devsetup list` | Lists all kegs/packages installed from the tapped homebrew tap |
| `devsetup info <formula>` | Gets the info for a formula |
| `devsetup search <str>` | Searches for a formula |
| `devsetup add <formula>`<br>`devsetup add <owner>/<tap>/<formula>` | makes a clone of the upstream formula in this tap to lock it's definition, checks that the current working directory or provided dir matches the result of get tap, or makes it in the brew tap and creates a PR, and goes back to the default branch. Overwrites any formula that already exists. |
| `devsetup alias <formula> <alias>`<br>`devsetup remove <owner>/<tap>/<formula> <alias>` | creates a new formula that has the upstream formula as a direct dependency<br>**Note:**versioning ls less controllable here and updates **only** propagate when the created formula changes. |
| `devsetup doctor` | checks for common issues with the machine and produces a diagnostic report for the owner to help diagnose<br><b>Note:</b> The functionality of this command is provided by you |
| `devsetup -h` | prints the help message |
| `devsetup version` | prints the version of the devsetup command |
| `devsetup tap-info [--prefix]` | alias for `brew tap-info $(devsetup get-tap)`. `--prefix` just returns the location of the tap (alias for `$(brew --repository $(devsetup get-tap)`) |
| `devsetup configure <topic> [--reconfigure]` | Alias for `brew update && brew install $(devsetup get-tap)/devsetup-configure-<topic>`. If `--reconfigure` is passed, then the formula is removed first, which removes any configuration it set up prior. |

### `devsetup doctor`

Use this as a way to gather information about a user's machine to diagnose issues. The default functionality runs `brew config && brew doctor`

### `devsetup configure` topics

These are examples but some setup scripts come out of the box for you to customize and use. These boil down into additional devsetup formulas (like `devsetup-configure-git`), which then runs the script with the arguments passed through, but doesn't clutter `$PATH`.

When installed, the formula should check to see if conflicting configurations exist and warn accordingly.
Passing `--preserve` will make it non-interactive and assume that the configuration is correct and the formula will adopt it as it's own if possible. The configuration may not complete non-interactively if the configuration is not considered complete.

When upgraded, the formula should only configure new or additional things, and warn if it is going to change something that already exists (such as the default ssh key). This is an alias to installing with the `--preserve` flag.

When removed, the uninstall scripts should remove any configuration they had set up interactively. Passing `--preserve` will make it non-interactive and not remove any configuration.
Passing `--force` will remove the configuration without warning.

If you want any of these configurations to happen automatically on `devsetup install`, add the formula as a depdendency to the `devsetup` formula.

| topic          | description                                                                                                                                                                                                                                                       |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `git`          | sets up git with a global user and email. Also globally sets `pull.rebase` to false (merge when diverge)                                                                                                                                                          |
| `github-token` | sets up a GITHUB_TOKEN and adds it to your `~/.profile`                                                                                                                                                                                                           |
| `github-ssh`   | sets up github to prefer ssh via `git config --global url.ssh://git@github.com/.insteadOf https://github.com/`, and then runs `gh ssh-key add $(devsetup-configure-ssh --keyfile)`.<br><b>Note:</b> depends on `gh` and `nsheaps/devsetup/devsetup-configure-ssh` |
| `ssh`          | sets up ssh with a key and config. Also provides a `--keyfile [keytype]` to return the location of the requested keyfile                                                                                                                                          |
| `gpg`          | sets up gpg with a key and config                                                                                                                                                                                                                                 |
| `aws`          | sets up aws with a profile and config                                                                                                                                                                                                                             |
