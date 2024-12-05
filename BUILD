load("@rules_python//python:defs.bzl", "py_binary")
load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "run",
    srcs = ["run.py"],
    main = "run.py",
    deps = [
        "//app:app_lib",
        requirement("numpy"),
        requirement("scikit-learn"),
        requirement("sentence-transformers"),
        requirement("flask"),
        requirement("flask-cors"),
        requirement("python-dotenv"),
        requirement("PyPDF2"),
        requirement("langchain"),
        requirement("python-magic"),
        requirement("openai"),
        requirement("huggingface-hub"),
        requirement("werkzeug"),
    ],
)
