import json
import os
import pytest
import tempfile

# ---------------------------------------------------------------------------
# We import the module under test by pointing at it directly so the test file
# can live anywhere relative to the source tree.
# ---------------------------------------------------------------------------
import importlib.util, pathlib

# Locate & load the module dynamically so we don't rely on a fixed package structure
_SRC = pathlib.Path(__file__).parent / "data_utils.py"   # adjust if needed
_spec = importlib.util.spec_from_file_location("data_utils", _SRC)
data_utils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(data_utils)

# Pull the public helpers into the local namespace for convenience
append_data       = data_utils.append_data
read_data         = data_utils.read_data
save_user         = data_utils.save_user
get_user          = data_utils.get_user
user_exists       = data_utils.user_exists
add_transaction   = data_utils.add_transaction
get_transactions  = data_utils.get_transactions
delete_transaction= data_utils.delete_transaction


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tmp_file(suffix=".json"):
    """Return a path to a fresh temporary file that is removed after each test."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return path


# ===========================================================================
# append_data
# ===========================================================================

class TestAppendData:
    def test_creates_file_when_missing(self):
        path = _tmp_file()
        os.remove(path)                          # ensure it does not exist
        append_data({"key": "value"}, filepath=path)
        with open(path) as f:
            data = json.load(f)
        assert data == [{"key": "value"}]
        os.remove(path)

    def test_appends_to_existing_list(self):
        path = _tmp_file()
        with open(path, "w") as f:
            json.dump([{"a": 1}], f)
        append_data({"b": 2}, filepath=path)
        with open(path) as f:
            data = json.load(f)
        assert data == [{"a": 1}, {"b": 2}]
        os.remove(path)

    def test_handles_corrupt_file_gracefully(self):
        path = _tmp_file()
        with open(path, "w") as f:
            f.write("NOT VALID JSON!!!")
        append_data({"x": 99}, filepath=path)
        with open(path) as f:
            data = json.load(f)
        assert data == [{"x": 99}]
        os.remove(path)


# ===========================================================================
# read_data
# ===========================================================================

class TestReadData:
    def test_returns_empty_structure_when_file_missing(self):
        result = read_data(filepath="/nonexistent/path/users.json")
        assert result == {"user_list": []}

    def test_wraps_bare_list_in_user_list(self):
        path = _tmp_file()
        with open(path, "w") as f:
            json.dump([{"user_alice": {}}], f)
        result = read_data(filepath=path)
        assert "user_list" in result
        assert isinstance(result["user_list"], list)
        os.remove(path)

    def test_adds_user_list_key_when_missing_from_dict(self):
        path = _tmp_file()
        with open(path, "w") as f:
            json.dump({"other_key": 123}, f)
        result = read_data(filepath=path)
        assert "user_list" in result
        assert result["user_list"] == []
        os.remove(path)

    def test_returns_dict_intact_when_well_formed(self):
        path = _tmp_file()
        payload = {"user_list": [{"user_bob": {"password_hash": "abc"}}]}
        with open(path, "w") as f:
            json.dump(payload, f)
        result = read_data(filepath=path)
        assert result == payload
        os.remove(path)


# ===========================================================================
# save_user / get_user / user_exists
# ===========================================================================

class TestUserPersistence:
    def setup_method(self):
        self.path = _tmp_file()

    def teardown_method(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def _make_user(self, username="alice", password_hash="hashed_pw"):
        return {
            "username": username,
            "password_hash": password_hash,
            "session": {},
            "transactions": [],
            "income": [],
            "expense": [],
        }

    def test_save_and_retrieve_user(self):
        user = self._make_user("alice")
        save_user(user, filepath=self.path)
        result = get_user("alice", filepath=self.path)
        assert result is not None
        assert result["password_hash"] == "hashed_pw"

    def test_get_user_returns_none_for_unknown(self):
        assert get_user("ghost", filepath=self.path) is None

    def test_multiple_users_stored_independently(self):
        save_user(self._make_user("alice", "pw_alice"), filepath=self.path)
        save_user(self._make_user("bob",   "pw_bob"),   filepath=self.path)
        alice = get_user("alice", filepath=self.path)
        bob   = get_user("bob",   filepath=self.path)
        assert alice["password_hash"] == "pw_alice"
        assert bob["password_hash"]   == "pw_bob"

    def test_user_fields_default_to_empty_collections(self):
        save_user({"username": "charlie", "password_hash": "x"}, filepath=self.path)
        result = get_user("charlie", filepath=self.path)
        assert result["transactions"] == []
        assert result["income"]       == []
        assert result["expense"]      == []
        assert result["session"]      == {}

    def test_user_exists_true_after_save(self):
        # Patch the module-level file path so user_exists uses our tmp file
        original = data_utils.file_path
        data_utils.file_path = self.path
        try:
            save_user(self._make_user("dave"), filepath=self.path)
            assert user_exists("dave") is True
        finally:
            data_utils.file_path = original

    def test_user_exists_false_when_absent(self):
        original = data_utils.file_path
        data_utils.file_path = self.path
        try:
            assert user_exists("nobody") is False
        finally:
            data_utils.file_path = original


# ===========================================================================
# add_transaction / get_transactions / delete_transaction
# ===========================================================================

class TestTransactions:
    def setup_method(self):
        self.path = _tmp_file()

    def teardown_method(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add_and_retrieve_single_transaction(self):
        txn = {"amount": 50.0, "category": "food", "type": "expense"}
        add_transaction("alice", txn, filepath=self.path)
        results = get_transactions("alice", filepath=self.path)
        assert len(results) == 1
        assert results[0]["amount"] == 50.0
        assert results[0]["username"] == "alice"

    def test_transactions_are_scoped_per_user(self):
        add_transaction("alice", {"amount": 10}, filepath=self.path)
        add_transaction("bob",   {"amount": 20}, filepath=self.path)
        alice_txns = get_transactions("alice", filepath=self.path)
        bob_txns   = get_transactions("bob",   filepath=self.path)
        assert len(alice_txns) == 1
        assert len(bob_txns)   == 1
        assert alice_txns[0]["amount"] == 10
        assert bob_txns[0]["amount"]   == 20

    def test_get_transactions_returns_empty_for_unknown_user(self):
        assert get_transactions("nobody", filepath=self.path) == []

    def test_multiple_transactions_accumulate(self):
        for i in range(5):
            add_transaction("alice", {"amount": i}, filepath=self.path)
        assert len(get_transactions("alice", filepath=self.path)) == 5

    def test_delete_transaction_by_index(self):
        add_transaction("alice", {"amount": 1}, filepath=self.path)
        add_transaction("alice", {"amount": 2}, filepath=self.path)
        add_transaction("alice", {"amount": 3}, filepath=self.path)
        success = delete_transaction("alice", 1, filepath=self.path)   # remove middle
        assert success is True
        remaining = get_transactions("alice", filepath=self.path)
        assert len(remaining) == 2
        assert remaining[0]["amount"] == 1
        assert remaining[1]["amount"] == 3

    def test_delete_first_transaction(self):
        add_transaction("alice", {"amount": 100}, filepath=self.path)
        add_transaction("alice", {"amount": 200}, filepath=self.path)
        delete_transaction("alice", 0, filepath=self.path)
        remaining = get_transactions("alice", filepath=self.path)
        assert len(remaining) == 1
        assert remaining[0]["amount"] == 200

    def test_delete_invalid_index_returns_false(self):
        add_transaction("alice", {"amount": 99}, filepath=self.path)
        assert delete_transaction("alice", 99,  filepath=self.path) is False
        assert delete_transaction("alice", -1,  filepath=self.path) is False

    def test_delete_does_not_affect_other_users(self):
        add_transaction("alice", {"amount": 5},  filepath=self.path)
        add_transaction("bob",   {"amount": 10}, filepath=self.path)
        delete_transaction("alice", 0, filepath=self.path)
        assert get_transactions("alice", filepath=self.path) == []
        assert len(get_transactions("bob", filepath=self.path)) == 1

    def test_get_transactions_handles_corrupt_file(self):
        with open(self.path, "w") as f:
            f.write("INVALID")
        assert get_transactions("alice", filepath=self.path) == []
