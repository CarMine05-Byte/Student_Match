from django.db import migrations
from django.db.models import Count, F, Q


MAX_TUTOR_PER_GRUPPO = 4
MAX_ADMIN_PER_GRUPPO = 2


def validate_existing_values(apps, schema_editor):
    if MAX_TUTOR_PER_GRUPPO < 1 or MAX_ADMIN_PER_GRUPPO < 1:
        raise ValueError("I limiti massimi di tutor e admin devono essere maggiori di zero.")

    Gruppo = apps.get_model("studymatch", "Gruppo")
    Partecipazione = apps.get_model("studymatch", "Partecipazione")
    Supporto = apps.get_model("studymatch", "Supporto")
    Gestione = apps.get_model("studymatch", "Gestione")
    Studente = apps.get_model("studymatch", "Studente")
    Tutor = apps.get_model("studymatch", "Tutor")
    Admin = apps.get_model("studymatch", "Admin")

    errors = []

    invalid_capienze = list(
        Gruppo.objects.filter(max_partecipanti__lt=0)
        .order_by("id_gruppo")
        .values("id_gruppo", "max_partecipanti")
    )
    if invalid_capienze:
        errors.append(
            "capienze negative: "
            + ", ".join(
                f"gruppo {row['id_gruppo']}={row['max_partecipanti']}"
                for row in invalid_capienze
            )
        )

    groups_over_capacity = list(
        Gruppo.objects.annotate(
            accepted_count=Count(
                "gruppo_utente",
                filter=Q(gruppo_utente__stato=True),
            )
        )
        .filter(accepted_count__gt=F("max_partecipanti"))
        .order_by("id_gruppo")
        .values("id_gruppo", "max_partecipanti", "accepted_count")
    )
    if groups_over_capacity:
        errors.append(
            "gruppi oltre capienza: "
            + ", ".join(
                "gruppo {id_gruppo}: {accepted_count}/{max_partecipanti}".format(**row)
                for row in groups_over_capacity
            )
        )

    supporto_over_limit = list(
        Supporto.objects.values("id_gruppo_id")
        .annotate(tutor_count=Count("id"))
        .filter(tutor_count__gt=MAX_TUTOR_PER_GRUPPO)
        .order_by("id_gruppo_id")
    )
    if supporto_over_limit:
        errors.append(
            "troppi tutor: "
            + ", ".join(
                f"gruppo {row['id_gruppo_id']}: {row['tutor_count']}"
                for row in supporto_over_limit
            )
        )

    gestione_over_limit = list(
        Gestione.objects.values("id_gruppo_id")
        .annotate(admin_count=Count("id"))
        .filter(admin_count__gt=MAX_ADMIN_PER_GRUPPO)
        .order_by("id_gruppo_id")
    )
    if gestione_over_limit:
        errors.append(
            "troppi admin: "
            + ", ".join(
                f"gruppo {row['id_gruppo_id']}: {row['admin_count']}"
                for row in gestione_over_limit
            )
        )

    invalid_students = list(
        Studente.objects.exclude(studente__ruolo="studente")
        .order_by("id")
        .values("id", "studente_id", "studente__ruolo")
    )
    if invalid_students:
        errors.append(
            "studenti con ruolo non coerente: "
            + ", ".join(
                f"{row['studente_id']}={row['studente__ruolo']}"
                for row in invalid_students
            )
        )

    invalid_tutors = list(
        Tutor.objects.exclude(tutor__ruolo="tutor")
        .order_by("id")
        .values("id", "tutor_id", "tutor__ruolo")
    )
    if invalid_tutors:
        errors.append(
            "tutor con ruolo non coerente: "
            + ", ".join(
                f"{row['tutor_id']}={row['tutor__ruolo']}"
                for row in invalid_tutors
            )
        )

    invalid_admins = list(
        Admin.objects.exclude(admin__ruolo="admin")
        .order_by("id")
        .values("id", "admin_id", "admin__ruolo")
    )
    if invalid_admins:
        errors.append(
            "admin con ruolo non coerente: "
            + ", ".join(
                f"{row['admin_id']}={row['admin__ruolo']}"
                for row in invalid_admins
            )
        )

    student_ids = set(Studente.objects.values_list("studente_id", flat=True))
    tutor_ids = set(Tutor.objects.values_list("tutor_id", flat=True))
    admin_ids = set(Admin.objects.values_list("admin_id", flat=True))
    duplicate_specializations = sorted(
        (student_ids & tutor_ids)
        | (student_ids & admin_ids)
        | (tutor_ids & admin_ids)
    )
    if duplicate_specializations:
        errors.append(
            "utenti in piu' specializzazioni: "
            + ", ".join(duplicate_specializations)
        )

    if errors:
        raise ValueError(
            "Impossibile applicare la migration. Valori non validi: "
            + "; ".join(errors)
            + "."
        )


class Migration(migrations.Migration):

    dependencies = [
        ("studymatch", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            validate_existing_values,
            reverse_code=migrations.RunPython.noop,
        ),

        # =====================================================
        # 1. CONTROLLO DELLA CAPIENZA MASSIMA
        # Inserimento di una partecipazione già accettata
        # =====================================================
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS
                trg_partecipazione_capienza_insert
                BEFORE INSERT ON studymatch_partecipazione
                FOR EACH ROW

                WHEN NEW.stato = 1
                AND (
                    SELECT COUNT(*)
                    FROM studymatch_partecipazione
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                    AND stato = 1
                ) >= (
                    SELECT max_partecipanti
                    FROM studymatch_gruppo
                    WHERE id_gruppo = NEW.id_gruppo_id
                )

                BEGIN
                SELECT RAISE(
                               ABORT,
                               'Capienza massima del gruppo raggiunta'
                       );
                END;
                """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_partecipazione_capienza_insert;
            """,
        ),

        # =====================================================
        # 1. CONTROLLO DELLA CAPIENZA MASSIMA
        # Modifica dello stato in accettato
        # =====================================================
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS
                trg_partecipazione_capienza_update
                BEFORE UPDATE OF stato, id_gruppo_id
                ON studymatch_partecipazione
                FOR EACH ROW

                WHEN NEW.stato = 1
                AND (
                    OLD.stato != 1
                    OR NEW.id_gruppo_id != OLD.id_gruppo_id
                )
                AND (
                    SELECT COUNT(*)
                    FROM studymatch_partecipazione
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                    AND stato = 1
                ) >= (
                    SELECT max_partecipanti
                    FROM studymatch_gruppo
                    WHERE id_gruppo = NEW.id_gruppo_id
                )

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Capienza massima del gruppo raggiunta'
                    );
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_partecipazione_capienza_update;
            """,
        ),

        # =====================================================
        # 2. CONTROLLO DELLA MODIFICA DELLA CAPIENZA
        # =====================================================
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS
                trg_gruppo_modifica_capienza
                BEFORE UPDATE OF max_partecipanti
                ON studymatch_gruppo
                FOR EACH ROW

                WHEN NEW.max_partecipanti < (
                    SELECT COUNT(*)
                    FROM studymatch_partecipazione
                    WHERE id_gruppo_id = NEW.id_gruppo
                    AND stato = 1
                )

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Capienza inferiore agli studenti accettati'
                    );
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_gruppo_modifica_capienza;
            """,
        ),

        # =====================================================
        # 3. COERENZA TRA RUOLO E SPECIALIZZAZIONE
        # 4. DISGIUNZIONE DELLA SPECIALIZZAZIONE
        # Controllo per STUDENTE
        # =====================================================
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS
                trg_studente_specializzazione
                BEFORE INSERT ON studymatch_studente
                FOR EACH ROW

                BEGIN
                    SELECT CASE
                        WHEN COALESCE(
                            (
                                SELECT ruolo
                                FROM studymatch_utente
                                WHERE utente = NEW.studente_id
                            ),
                            ''
                        ) != 'studente'

                        THEN RAISE(
                            ABORT,
                            'Ruolo non coerente con STUDENTE'
                        )
                    END;

                    SELECT CASE
                        WHEN EXISTS (
                            SELECT 1
                            FROM studymatch_tutor
                            WHERE tutor_id = NEW.studente_id
                        )
                        OR EXISTS (
                            SELECT 1
                            FROM studymatch_admin
                            WHERE admin_id = NEW.studente_id
                        )

                        THEN RAISE(
                            ABORT,
                            'Utente già presente in un altra specializzazione'
                        )
                    END;
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_studente_specializzazione;
            """,
        ),

        # =====================================================
        # 3. COERENZA TRA RUOLO E SPECIALIZZAZIONE
        # 4. DISGIUNZIONE DELLA SPECIALIZZAZIONE
        # Controllo per TUTOR
        # =====================================================
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS
                trg_tutor_specializzazione
                BEFORE INSERT ON studymatch_tutor
                FOR EACH ROW

                BEGIN
                    SELECT CASE
                        WHEN COALESCE(
                            (
                                SELECT ruolo
                                FROM studymatch_utente
                                WHERE utente = NEW.tutor_id
                            ),
                            ''
                        ) != 'tutor'

                        THEN RAISE(
                            ABORT,
                            'Ruolo non coerente con TUTOR'
                        )
                    END;

                    SELECT CASE
                        WHEN EXISTS (
                            SELECT 1
                            FROM studymatch_studente
                            WHERE studente_id = NEW.tutor_id
                        )
                        OR EXISTS (
                            SELECT 1
                            FROM studymatch_admin
                            WHERE admin_id = NEW.tutor_id
                        )

                        THEN RAISE(
                            ABORT,
                            'Utente già presente in un altra specializzazione'
                        )
                    END;
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_tutor_specializzazione;
            """,
        ),

        # =====================================================
        # 3. COERENZA TRA RUOLO E SPECIALIZZAZIONE
        # 4. DISGIUNZIONE DELLA SPECIALIZZAZIONE
        # Controllo per ADMIN
        # =====================================================
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS
                trg_admin_specializzazione
                BEFORE INSERT ON studymatch_admin
                FOR EACH ROW

                BEGIN
                    SELECT CASE
                        WHEN COALESCE(
                            (
                                SELECT ruolo
                                FROM studymatch_utente
                                WHERE utente = NEW.admin_id
                            ),
                            ''
                        ) != 'admin'

                        THEN RAISE(
                            ABORT,
                            'Ruolo non coerente con ADMIN'
                        )
                    END;

                    SELECT CASE
                        WHEN EXISTS (
                            SELECT 1
                            FROM studymatch_studente
                            WHERE studente_id = NEW.admin_id
                        )
                        OR EXISTS (
                            SELECT 1
                            FROM studymatch_tutor
                            WHERE tutor_id = NEW.admin_id
                        )

                        THEN RAISE(
                            ABORT,
                            'Utente già presente in un altra specializzazione'
                        )
                    END;
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_admin_specializzazione;
            """,
        ),

        migrations.RunSQL(
            sql="""
                CREATE TRIGGER IF NOT EXISTS
                trg_utente_ruolo_specializzazione_update
                BEFORE UPDATE OF ruolo
                ON studymatch_utente
                FOR EACH ROW

                WHEN (
                    NEW.ruolo != 'studente'
                    AND EXISTS (
                        SELECT 1
                        FROM studymatch_studente
                        WHERE studente_id = NEW.utente
                    )
                )
                OR (
                    NEW.ruolo != 'tutor'
                    AND EXISTS (
                        SELECT 1
                        FROM studymatch_tutor
                        WHERE tutor_id = NEW.utente
                    )
                )
                OR (
                    NEW.ruolo != 'admin'
                    AND EXISTS (
                        SELECT 1
                        FROM studymatch_admin
                        WHERE admin_id = NEW.utente
                    )
                )

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Ruolo non coerente con la specializzazione esistente'
                    );
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_utente_ruolo_specializzazione_update;
            """,
        ),

        # =====================================================
        # 5. LIMITE MASSIMO DI TUTOR PER GRUPPO
        # Massimo 4 tutor
        # =====================================================
        migrations.RunSQL(
            sql=f"""
                CREATE TRIGGER IF NOT EXISTS
                trg_supporto_limite_tutor_insert
                BEFORE INSERT ON studymatch_supporto
                FOR EACH ROW

                WHEN (
                    SELECT COUNT(*)
                    FROM studymatch_supporto
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                ) >= {MAX_TUTOR_PER_GRUPPO}

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Un gruppo non può avere più di 4 tutor'
                    );
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_supporto_limite_tutor_insert;
            """,
        ),

        migrations.RunSQL(
            sql=f"""
                CREATE TRIGGER IF NOT EXISTS
                trg_supporto_limite_tutor_update
                BEFORE UPDATE OF id_gruppo_id
                ON studymatch_supporto
                FOR EACH ROW

                WHEN NEW.id_gruppo_id != OLD.id_gruppo_id
                AND (
                    SELECT COUNT(*)
                    FROM studymatch_supporto
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                ) >= {MAX_TUTOR_PER_GRUPPO}

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Un gruppo non può avere più di 4 tutor'
                    );
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_supporto_limite_tutor_update;
            """,
        ),

        # =====================================================
        # 5. LIMITE MASSIMO DI ADMIN PER GRUPPO
        # Massimo 2 amministratori
        # =====================================================
        migrations.RunSQL(
            sql=f"""
                CREATE TRIGGER IF NOT EXISTS
                trg_gestione_limite_admin_insert
                BEFORE INSERT ON studymatch_gestione
                FOR EACH ROW

                WHEN (
                    SELECT COUNT(*)
                    FROM studymatch_gestione
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                ) >= {MAX_ADMIN_PER_GRUPPO}

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Un gruppo non può avere più di 2 amministratori'
                    );
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_gestione_limite_admin_insert;
            """,
        ),

        migrations.RunSQL(
            sql=f"""
                CREATE TRIGGER IF NOT EXISTS
                trg_gestione_limite_admin_update
                BEFORE UPDATE OF id_gruppo_id
                ON studymatch_gestione
                FOR EACH ROW

                WHEN NEW.id_gruppo_id != OLD.id_gruppo_id
                AND (
                    SELECT COUNT(*)
                    FROM studymatch_gestione
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                ) >= {MAX_ADMIN_PER_GRUPPO}

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Un gruppo non può avere più di 2 amministratori'
                    );
                END;
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS
                trg_gestione_limite_admin_update;
            """,
        ),
    ]
