load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "routes_lib",
    srcs = [
        "files.py",
        "query.py",
        "upload.py",
        "main.py",
    ],
    deps = [
        "//app/config:config_lib",
        "//app/services:services_lib",
        requirement("flask"),
        requirement("werkzeug"),
        requirement("openai"),
    ],
    visibility = ["//visibility:public"],
)
