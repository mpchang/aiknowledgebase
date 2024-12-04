load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "config_lib",
    srcs = ["config.py"],
    deps = [
        requirement("python-dotenv"),
    ],
    visibility = ["//visibility:public"],
)
