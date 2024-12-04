load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "app_lib",
    srcs = [
        "__init__.py",
    ],
    deps = [
        "//app/config:config_lib",
        "//app/routes:routes_lib",
        "//app/services:services_lib",
        requirement("flask"),
        requirement("flask-cors"),
    ],
    visibility = ["//visibility:public"],
)
