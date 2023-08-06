# from types import NoneType
from setup_tests import path_to_uri, run_request, test_dir, write_rpc_request

from fortls.json_templates import uri_json


def imp_request(file, line, char):
    return write_rpc_request(
        1,
        "textDocument/implementation",
        {
            "textDocument": {"uri": path_to_uri(str(file))},
            "position": {"line": line, "character": char},
        },
    )


def check_imp_request(response: dict, references: dict):
    for uri, changes in response.items():
        refs = references[uri]
        # Loop over all the changes in the current URI, instances of object
        for c, r in zip(changes, refs):
            assert c["range"] == r["range"]


def create(file, line, schar, echar):
    return uri_json(path_to_uri(str(file)), line, schar, line, echar)


def test_implementation_type_bound():
    """Go to implementation of type-bound procedures"""
    string = write_rpc_request(1, "initialize", {"rootPath": str(test_dir)})
    file_path = test_dir / "test.f90"
    string += imp_request(file_path, 3, 17)
    errcode, results = run_request(string, ["-n", "1"])
    assert errcode == 0
    assert results[1] == create(test_dir / "subdir" / "test_free.f90", 49, 11, 28)
