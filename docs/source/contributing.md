# Contributing to CPL

We would love for you to contribute to CPL and help make it even better than it is today! As a contributor, here are the guidelines we would like you to follow:

- [Issuses and Bugs](#found-a-bug)
- [Feature Request](#feature-request)
- [Submission Guidelines](#submission-guidelines)
- [Coding Rules](#coding-rules)
- [License](#license)

## Found a Bug?

If you find a bug in the source code, you can help us by [submitting an issue](#submitting-an-issue) to our [Gitea Repository][gitea-repo]. Even better, you can [submit a Pull Request](#submitting-a-pull-request) with a fix.

## Feature Request

You can request a new feature by submitting an issue to our [Gitea Repository][gitea-repo]. If you would like to implement a new feature, please consider the size of the change in order to determine the right steps to proceed:

For a Major Feature, first open an issue and outline your proposal so that it can be discussed. This process allows us to better coordinate our efforts, prevent duplication of work, and help you to craft the change so that it is successfully accepted into the project.

Note: Adding a new topic to the documentation, or significantly re-writing a topic, counts as a major feature.

Small Features can be crafted and directly submitted as a [Pull Request](#submit-pr).

## Submission Guidelines

### Submitting an Issue

Before you submit an issue, please search the issue tracker, maybe an issue for your problem already exists and the discussion might inform you of workarounds readily available.

We want to fix all the issues as soon as possible, but before fixing a bug we need to reproduce and confirm it. In order to reproduce bugs, we require that you provide a minimal reproduction. Having a minimal reproducible scenario gives us a wealth of important information without going back and forth to you with additional questions.

A minimal reproduction allows us to quickly confirm a bug (or point out a coding problem) as well as confirm that we are fixing the right problem.

We require a minimal reproduction to save maintainers' time and ultimately be able to fix more bugs. Often, developers find coding problems themselves while preparing a minimal reproduction. We understand that sometimes it might be hard to extract essential bits of code from a larger codebase but we really need to isolate the problem before we can fix it.

Unfortunately, we are not able to investigate / fix bugs without a minimal reproduction, so if we don't hear back from you, we are going to close an issue that doesn't have enough info to be reproduced.

### Submitting a Pull Request

Before you submit your Pull Request (PR) consider the following guidelines:

1. Search the [repository][gitea-repo] for an open or closed PR that relates to your submission. You don't want to duplicate existing efforts.

2. Be sure that an issue describes the problem you're fixing, or documents the design for the feature you'd like to add. Discussing the design upfront helps to ensure that we're ready to accept your work.

3. Fork the sh-edraft.de/sh_cpl repo.

4. In your forked repository, make your changes in a new git branch:

    ```sh
    git checkout -b my-fix-branch master
    ```

5. Create your patch, including appropriate test cases.

<!-- 6. Follow our [Coding Rules](coding-rules). -->

6. Commit your changes.

    ```sh
    git commit --all
    ```

    Note: the optional commit ```-a``` command line option will automatically "add" and "rm" edited files.

7. Push your branch to the [repository][gitea-repo]:

    ```sh
    git push origin my-fix-branch
    ```

8. In Gitea, send a pull request to sh_cpl:master

### Reviewing a Pull Request

The sh-edraft.de team reserves the right not to accept pull requests from community members who haven't been good citizens of the community. Such behavior includes not following the CPL [coding rules](#coding-rules) and applies within or outside of CPL managed channels.

#### Addressing review feedback

If we ask for changes via code reviews then:

1. Make the required updates to the code.

2. Create a fixup commit and push to your repository (this will update your Pull Request):

    ```sh
    git commit --all --fixup HEAD
    git push
    ```

That's it! Thank you for your contribution!

## Coding Rules

To ensure consistency throughout the source code, keep these rules in mind as you are working:

- All features or bug fixes must be tested by one or more unit-tests.

- All public API methods must be documented.

- We follow [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
See [LICENSE](https://git.sh-edraft.de/sh-edraft.de/sh_cpl/src/branch/master/LICENSE)

<!-- LINKS -->
[gitea-repo]: https://git.sh-edraft.de/sh-edraft.de/sh_cpl/
[coding-rules]: /
