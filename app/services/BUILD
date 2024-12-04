load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "services_lib",
    srcs = [
        "document_processor.py",
        "embedding_service.py",
        "container.py",
    ],
    deps = [
        "//app/config:config_lib",
        requirement("PyPDF2"),
        requirement("langchain"),
        requirement("sentence-transformers"),
        requirement("scikit-learn"),
        requirement("numpy"),
    ],
    visibility = ["//visibility:public"],
)
