from __future__ import annotations

import importlib.util
import sqlite3
import tempfile
import unittest
from contextlib import closing
from importlib.machinery import SourceFileLoader
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIST_OS_DB_PATH = REPO_ROOT / "bin" / "artist-os-db"


def load_artist_os_db():
    # The script has no .py extension, so it is not importable as a module.
    # Load it via SourceFileLoader exactly like the storage tests do so the
    # production registry/functions under test are the real ones.
    loader = SourceFileLoader("artist_os_db", str(ARTIST_OS_DB_PATH))
    spec = importlib.util.spec_from_loader("artist_os_db", loader)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


artist_os_db = load_artist_os_db()

# Throwaway probe schema deltas. These touch only `migration_probe`, never any
# production table, so the real schema is left untouched no matter what runs.
PROBE_V3 = artist_os_db.Migration(
    version=3,
    name="probe_create_table",
    statements=["CREATE TABLE migration_probe (id INTEGER PRIMARY KEY)"],
)
PROBE_V4 = artist_os_db.Migration(
    version=4,
    name="probe_add_column",
    statements=["ALTER TABLE migration_probe ADD COLUMN label TEXT"],
)


def fresh_db(tmpdir: str) -> Path:
    # A real on-disk DB exercised through the same connect/apply_schema path as
    # production, so persistence (commit) behaviour is what we actually test.
    return artist_os_db.connect(Path(tmpdir) / "artist-os.sqlite")


def applied_versions(conn: sqlite3.Connection) -> set[int]:
    return {row[0] for row in conn.execute("SELECT version FROM schema_migrations")}


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (name,),
    ).fetchone()
    return row is not None


class ApplyMigrationsContractTests(unittest.TestCase):
    def test_fresh_db_records_exactly_baseline_versions_one_and_two(self) -> None:
        # Baseline guard: the frozen-baseline model says a fresh DB after
        # apply_schema sits at exactly {1, 2}. If this drifts (e.g. a migration's
        # effect got baked into the DDL, or a new seed appeared), the whole
        # incremental model is unsound, so we pin it explicitly.
        with tempfile.TemporaryDirectory() as tmpdir:
            with closing(fresh_db(tmpdir)) as conn, conn:
                newly = artist_os_db.apply_schema(conn)
                self.assertEqual(applied_versions(conn), {1, 2})
            # With the empty production registry, apply_schema applies nothing.
            self.assertEqual(newly, [])

    def test_idempotent_when_everything_already_applied(self) -> None:
        # Contract #1: re-running with nothing pending must be a silent no-op
        # that returns [] and raises nothing. This is what makes apply_schema
        # safe to call from the ~7 setup/refresh sites on every invocation.
        with tempfile.TemporaryDirectory() as tmpdir:
            with closing(fresh_db(tmpdir)) as conn, conn:
                artist_os_db.apply_schema(conn)
                first = artist_os_db.apply_migrations(conn, [PROBE_V3])
                second = artist_os_db.apply_migrations(conn, [PROBE_V3])
                self.assertEqual(first, [3])
                self.assertEqual(second, [])

    def test_incremental_applies_new_version_and_records_it(self) -> None:
        # Contract #2: from {1, 2}, a registry with a v3 migration applies v3,
        # records it in schema_migrations, and the v3 effect (a new table) is
        # actually present afterward.
        with tempfile.TemporaryDirectory() as tmpdir:
            with closing(fresh_db(tmpdir)) as conn, conn:
                artist_os_db.apply_schema(conn)
                self.assertFalse(table_exists(conn, "migration_probe"))
                newly = artist_os_db.apply_migrations(conn, [PROBE_V3])
                self.assertEqual(newly, [3])
                self.assertIn(3, applied_versions(conn))
                self.assertTrue(table_exists(conn, "migration_probe"))

    def test_applies_in_ascending_version_order_regardless_of_list_order(self) -> None:
        # Contract #3: v4 ALTERs the table v3 creates. If the runner honoured
        # list order instead of version order, passing [v4, v3] would try to
        # ALTER a table that does not yet exist and fail. Success here proves the
        # sort by version.
        with tempfile.TemporaryDirectory() as tmpdir:
            with closing(fresh_db(tmpdir)) as conn, conn:
                artist_os_db.apply_schema(conn)
                newly = artist_os_db.apply_migrations(conn, [PROBE_V4, PROBE_V3])
                self.assertEqual(newly, [3, 4])
                columns = {
                    row[1]
                    for row in conn.execute("PRAGMA table_info(migration_probe)")
                }
                self.assertIn("label", columns)

    def test_failed_migration_rolls_back_partial_effects_and_is_not_recorded(self) -> None:
        # Contract #4 (the hard one): Python's sqlite3 does not reliably wrap DDL
        # in the implicit DML transaction, so a partial migration could leave a
        # half-created table behind. The SAVEPOINT in apply_migrations must undo
        # the valid CREATE that ran before the invalid statement. We prove this
        # EMPIRICALLY: after the failure, the probe table must NOT exist and v3
        # must NOT be recorded. Then a corrected re-run applies cleanly.
        broken_v3 = artist_os_db.Migration(
            version=3,
            name="probe_broken",
            statements=[
                "CREATE TABLE migration_probe (id INTEGER PRIMARY KEY)",
                "THIS IS NOT VALID SQL",
            ],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            with closing(fresh_db(tmpdir)) as conn, conn:
                artist_os_db.apply_schema(conn)

                with self.assertRaises(sqlite3.OperationalError):
                    artist_os_db.apply_migrations(conn, [broken_v3])

                # The exact assertions proving rollback: the table the migration
                # tried to create is gone, and its version was never recorded.
                self.assertFalse(table_exists(conn, "migration_probe"))
                self.assertNotIn(3, applied_versions(conn))

                # A corrected re-run then applies cleanly with no leftover state.
                newly = artist_os_db.apply_migrations(conn, [PROBE_V3])
                self.assertEqual(newly, [3])
                self.assertTrue(table_exists(conn, "migration_probe"))
                self.assertIn(3, applied_versions(conn))

    def test_skips_already_applied_versions_without_error(self) -> None:
        # Contract #5: with the DB already at {1, 2, 3}, a registry of [v3, v4]
        # must apply only v4 and must not error on re-encountering v3.
        with tempfile.TemporaryDirectory() as tmpdir:
            with closing(fresh_db(tmpdir)) as conn, conn:
                artist_os_db.apply_schema(conn)
                self.assertEqual(artist_os_db.apply_migrations(conn, [PROBE_V3]), [3])
                self.assertEqual(applied_versions(conn), {1, 2, 3})

                newly = artist_os_db.apply_migrations(conn, [PROBE_V3, PROBE_V4])
                self.assertEqual(newly, [4])
                self.assertEqual(applied_versions(conn), {1, 2, 3, 4})

    def test_persists_across_connections_through_context_manager_commit(self) -> None:
        # Confirms migrations are committed (not just visible in-transaction):
        # we apply through the production `with closing(connect(...)) as conn, conn`
        # pattern, then reopen the file in a brand-new connection and assert the
        # effect survived.
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "artist-os.sqlite"
            with closing(artist_os_db.connect(db_path)) as conn, conn:
                artist_os_db.apply_schema(conn)
                artist_os_db.apply_migrations(conn, [PROBE_V3])
            with closing(sqlite3.connect(db_path)) as reopened:
                self.assertIn(3, applied_versions(reopened))
                self.assertTrue(table_exists(reopened, "migration_probe"))

    def test_apply_schema_folds_in_registered_migrations_on_every_setup_path(self) -> None:
        # Fold-in wiring proof: patch the module-level MIGRATIONS registry to
        # contain a throwaway v3, then run apply_schema on a fresh connection.
        # apply_schema calls apply_migrations() with no explicit argument, so it
        # must pick up the patched registry. Because every setup/init/refresh
        # site funnels through apply_schema, this proves they all migrate.
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(artist_os_db, "MIGRATIONS", [PROBE_V3]):
                with closing(fresh_db(tmpdir)) as conn, conn:
                    newly = artist_os_db.apply_schema(conn)
                    self.assertEqual(newly, [3])
                    self.assertIn(3, applied_versions(conn))
                    self.assertTrue(table_exists(conn, "migration_probe"))


class RegistryValidityTests(unittest.TestCase):
    def test_duplicate_versions_raise_and_write_nothing(self) -> None:
        # The new STATIC guard: two registered migrations sharing a version is a
        # registry bug, not an idempotent re-run. It must fail loud, and because
        # the raise happens BEFORE any DB mutation, schema_migrations must be
        # untouched (the colliding version must not appear).
        dup_a = artist_os_db.Migration(
            version=3, name="probe_dup_a", statements=["CREATE TABLE migration_probe (id INTEGER PRIMARY KEY)"]
        )
        dup_b = artist_os_db.Migration(
            version=3, name="probe_dup_b", statements=["CREATE TABLE migration_probe_b (id INTEGER PRIMARY KEY)"]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            with closing(fresh_db(tmpdir)) as conn, conn:
                artist_os_db.apply_schema(conn)
                with self.assertRaises(ValueError):
                    artist_os_db.apply_migrations(conn, [dup_a, dup_b])
                # Nothing was written: still exactly the baseline, v3 absent.
                self.assertEqual(applied_versions(conn), {1, 2})
                self.assertNotIn(3, applied_versions(conn))
                self.assertFalse(table_exists(conn, "migration_probe"))

    def test_version_below_baseline_raises_and_applies_nothing(self) -> None:
        # A version < MIN_MIGRATION_VERSION collides with / sits below the seeded
        # baseline (versions 1 and 2). It must raise before any DB mutation and
        # apply nothing.
        collides_with_baseline = artist_os_db.Migration(
            version=2, name="probe_collides_baseline", statements=["CREATE TABLE migration_probe (id INTEGER PRIMARY KEY)"]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            with closing(fresh_db(tmpdir)) as conn, conn:
                artist_os_db.apply_schema(conn)
                with self.assertRaises(ValueError):
                    artist_os_db.apply_migrations(conn, [collides_with_baseline])
                # Applied nothing: still exactly the baseline {1, 2}.
                self.assertEqual(applied_versions(conn), {1, 2})
                self.assertFalse(table_exists(conn, "migration_probe"))

    def test_valid_registry_remains_idempotent_after_guard(self) -> None:
        # REGRESSION guard: the new STATIC registry validation must NOT have
        # turned an already-applied version into an error. A valid single-v3
        # registry applied twice still returns [3] then [] with no raise --
        # proving the guard validates registry well-formedness only and leaves
        # the idempotent "skip already-applied" runtime behaviour intact.
        # (See also test_idempotent_when_everything_already_applied; this one
        # explicitly pins that the guard did not regress re-run safety.)
        with tempfile.TemporaryDirectory() as tmpdir:
            with closing(fresh_db(tmpdir)) as conn, conn:
                artist_os_db.apply_schema(conn)
                self.assertEqual(artist_os_db.apply_migrations(conn, [PROBE_V3]), [3])
                self.assertEqual(artist_os_db.apply_migrations(conn, [PROBE_V3]), [])
                self.assertEqual(applied_versions(conn), {1, 2, 3})


if __name__ == "__main__":
    unittest.main()
