workspace(name = "aiknowledgebase")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Python rules
http_archive(
    name = "rules_python",
    sha256 = "d71d2c67e0bce986e1c5a7731b4693226867c45bfe0b7c5e0067228a536fc580",
    strip_prefix = "rules_python-0.29.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.29.0/rules_python-0.29.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")
py_repositories()

# Register the Python toolchain
python_register_toolchains(
    name = "python3_9",
    python_version = "3.9",
)

load("@rules_python//python:pip.bzl", "pip_parse")

# Create a central repo to manage python dependencies
pip_parse(
    name = "pip",
    requirements_lock = "//:requirements.txt",
)

load("@pip//:requirements.bzl", "install_deps")
install_deps()
