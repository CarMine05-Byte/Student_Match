PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
INSERT INTO django_migrations VALUES(1,'contenttypes','0001_initial','2026-06-24 13:56:09.204654');
INSERT INTO django_migrations VALUES(2,'contenttypes','0002_remove_content_type_name','2026-06-24 13:56:09.209308');
INSERT INTO django_migrations VALUES(3,'auth','0001_initial','2026-06-24 13:56:09.219560');
INSERT INTO django_migrations VALUES(4,'auth','0002_alter_permission_name_max_length','2026-06-24 13:56:09.224390');
INSERT INTO django_migrations VALUES(5,'auth','0003_alter_user_email_max_length','2026-06-24 13:56:09.229286');
INSERT INTO django_migrations VALUES(6,'auth','0004_alter_user_username_opts','2026-06-24 13:56:09.233710');
INSERT INTO django_migrations VALUES(7,'auth','0005_alter_user_last_login_null','2026-06-24 13:56:09.239394');
INSERT INTO django_migrations VALUES(8,'auth','0006_require_contenttypes_0002','2026-06-24 13:56:09.250599');
INSERT INTO django_migrations VALUES(9,'auth','0007_alter_validators_add_error_messages','2026-06-24 13:56:09.254634');
INSERT INTO django_migrations VALUES(10,'auth','0008_alter_user_username_max_length','2026-06-24 13:56:09.259998');
INSERT INTO django_migrations VALUES(11,'auth','0009_alter_user_last_name_max_length','2026-06-24 13:56:09.264287');
INSERT INTO django_migrations VALUES(12,'auth','0010_alter_group_name_max_length','2026-06-24 13:56:09.268598');
INSERT INTO django_migrations VALUES(13,'auth','0011_update_proxy_permissions','2026-06-24 13:56:09.271756');
INSERT INTO django_migrations VALUES(14,'auth','0012_alter_user_first_name_max_length','2026-06-24 13:56:09.276801');
INSERT INTO django_migrations VALUES(15,'sessions','0001_initial','2026-06-24 13:56:09.281232');
INSERT INTO django_migrations VALUES(16,'studymatch','0001_initial','2026-06-24 13:56:09.323724');
INSERT INTO django_migrations VALUES(31,'studymatch','0002_create_trigger','2026-07-13 13:12:36.361438');
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO django_content_type VALUES(1,'auth','group');
INSERT INTO django_content_type VALUES(2,'auth','permission');
INSERT INTO django_content_type VALUES(3,'auth','user');
INSERT INTO django_content_type VALUES(4,'contenttypes','contenttype');
INSERT INTO django_content_type VALUES(5,'sessions','session');
INSERT INTO django_content_type VALUES(6,'studymatch','admin');
INSERT INTO django_content_type VALUES(7,'studymatch','assegnazione');
INSERT INTO django_content_type VALUES(8,'studymatch','condivisione');
INSERT INTO django_content_type VALUES(9,'studymatch','esame');
INSERT INTO django_content_type VALUES(10,'studymatch','gestione');
INSERT INTO django_content_type VALUES(11,'studymatch','gruppo');
INSERT INTO django_content_type VALUES(12,'studymatch','materiale');
INSERT INTO django_content_type VALUES(13,'studymatch','partecipazione');
INSERT INTO django_content_type VALUES(14,'studymatch','studente');
INSERT INTO django_content_type VALUES(15,'studymatch','supporto');
INSERT INTO django_content_type VALUES(16,'studymatch','svolgimento');
INSERT INTO django_content_type VALUES(17,'studymatch','tutor');
INSERT INTO django_content_type VALUES(18,'studymatch','utente');
INSERT INTO django_content_type VALUES(19,'studymatch','invio');
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
INSERT INTO auth_permission VALUES(1,2,'add_permission','Can add permission');
INSERT INTO auth_permission VALUES(2,2,'change_permission','Can change permission');
INSERT INTO auth_permission VALUES(3,2,'delete_permission','Can delete permission');
INSERT INTO auth_permission VALUES(4,2,'view_permission','Can view permission');
INSERT INTO auth_permission VALUES(5,1,'add_group','Can add group');
INSERT INTO auth_permission VALUES(6,1,'change_group','Can change group');
INSERT INTO auth_permission VALUES(7,1,'delete_group','Can delete group');
INSERT INTO auth_permission VALUES(8,1,'view_group','Can view group');
INSERT INTO auth_permission VALUES(9,3,'add_user','Can add user');
INSERT INTO auth_permission VALUES(10,3,'change_user','Can change user');
INSERT INTO auth_permission VALUES(11,3,'delete_user','Can delete user');
INSERT INTO auth_permission VALUES(12,3,'view_user','Can view user');
INSERT INTO auth_permission VALUES(13,4,'add_contenttype','Can add content type');
INSERT INTO auth_permission VALUES(14,4,'change_contenttype','Can change content type');
INSERT INTO auth_permission VALUES(15,4,'delete_contenttype','Can delete content type');
INSERT INTO auth_permission VALUES(16,4,'view_contenttype','Can view content type');
INSERT INTO auth_permission VALUES(17,5,'add_session','Can add session');
INSERT INTO auth_permission VALUES(18,5,'change_session','Can change session');
INSERT INTO auth_permission VALUES(19,5,'delete_session','Can delete session');
INSERT INTO auth_permission VALUES(20,5,'view_session','Can view session');
INSERT INTO auth_permission VALUES(21,18,'add_utente','Can add utente');
INSERT INTO auth_permission VALUES(22,18,'change_utente','Can change utente');
INSERT INTO auth_permission VALUES(23,18,'delete_utente','Can delete utente');
INSERT INTO auth_permission VALUES(24,18,'view_utente','Can view utente');
INSERT INTO auth_permission VALUES(25,14,'add_studente','Can add studente');
INSERT INTO auth_permission VALUES(26,14,'change_studente','Can change studente');
INSERT INTO auth_permission VALUES(27,14,'delete_studente','Can delete studente');
INSERT INTO auth_permission VALUES(28,14,'view_studente','Can view studente');
INSERT INTO auth_permission VALUES(29,17,'add_tutor','Can add tutor');
INSERT INTO auth_permission VALUES(30,17,'change_tutor','Can change tutor');
INSERT INTO auth_permission VALUES(31,17,'delete_tutor','Can delete tutor');
INSERT INTO auth_permission VALUES(32,17,'view_tutor','Can view tutor');
INSERT INTO auth_permission VALUES(33,6,'add_admin','Can add admin');
INSERT INTO auth_permission VALUES(34,6,'change_admin','Can change admin');
INSERT INTO auth_permission VALUES(35,6,'delete_admin','Can delete admin');
INSERT INTO auth_permission VALUES(36,6,'view_admin','Can view admin');
INSERT INTO auth_permission VALUES(37,9,'add_esame','Can add esame');
INSERT INTO auth_permission VALUES(38,9,'change_esame','Can change esame');
INSERT INTO auth_permission VALUES(39,9,'delete_esame','Can delete esame');
INSERT INTO auth_permission VALUES(40,9,'view_esame','Can view esame');
INSERT INTO auth_permission VALUES(41,11,'add_gruppo','Can add gruppo');
INSERT INTO auth_permission VALUES(42,11,'change_gruppo','Can change gruppo');
INSERT INTO auth_permission VALUES(43,11,'delete_gruppo','Can delete gruppo');
INSERT INTO auth_permission VALUES(44,11,'view_gruppo','Can view gruppo');
INSERT INTO auth_permission VALUES(45,12,'add_materiale','Can add materiale');
INSERT INTO auth_permission VALUES(46,12,'change_materiale','Can change materiale');
INSERT INTO auth_permission VALUES(47,12,'delete_materiale','Can delete materiale');
INSERT INTO auth_permission VALUES(48,12,'view_materiale','Can view materiale');
INSERT INTO auth_permission VALUES(49,13,'add_partecipazione','Can add partecipazione');
INSERT INTO auth_permission VALUES(50,13,'change_partecipazione','Can change partecipazione');
INSERT INTO auth_permission VALUES(51,13,'delete_partecipazione','Can delete partecipazione');
INSERT INTO auth_permission VALUES(52,13,'view_partecipazione','Can view partecipazione');
INSERT INTO auth_permission VALUES(53,15,'add_supporto','Can add supporto');
INSERT INTO auth_permission VALUES(54,15,'change_supporto','Can change supporto');
INSERT INTO auth_permission VALUES(55,15,'delete_supporto','Can delete supporto');
INSERT INTO auth_permission VALUES(56,15,'view_supporto','Can view supporto');
INSERT INTO auth_permission VALUES(57,10,'add_gestione','Can add gestione');
INSERT INTO auth_permission VALUES(58,10,'change_gestione','Can change gestione');
INSERT INTO auth_permission VALUES(59,10,'delete_gestione','Can delete gestione');
INSERT INTO auth_permission VALUES(60,10,'view_gestione','Can view gestione');
INSERT INTO auth_permission VALUES(61,16,'add_svolgimento','Can add svolgimento');
INSERT INTO auth_permission VALUES(62,16,'change_svolgimento','Can change svolgimento');
INSERT INTO auth_permission VALUES(63,16,'delete_svolgimento','Can delete svolgimento');
INSERT INTO auth_permission VALUES(64,16,'view_svolgimento','Can view svolgimento');
INSERT INTO auth_permission VALUES(65,7,'add_assegnazione','Can add assegnazione');
INSERT INTO auth_permission VALUES(66,7,'change_assegnazione','Can change assegnazione');
INSERT INTO auth_permission VALUES(67,7,'delete_assegnazione','Can delete assegnazione');
INSERT INTO auth_permission VALUES(68,7,'view_assegnazione','Can view assegnazione');
INSERT INTO auth_permission VALUES(69,8,'add_condivisione','Can add condivisione');
INSERT INTO auth_permission VALUES(70,8,'change_condivisione','Can change condivisione');
INSERT INTO auth_permission VALUES(71,8,'delete_condivisione','Can delete condivisione');
INSERT INTO auth_permission VALUES(72,8,'view_condivisione','Can view condivisione');
INSERT INTO auth_permission VALUES(73,19,'add_invio','Can add invio');
INSERT INTO auth_permission VALUES(74,19,'change_invio','Can change invio');
INSERT INTO auth_permission VALUES(75,19,'delete_invio','Can delete invio');
INSERT INTO auth_permission VALUES(76,19,'view_invio','Can view invio');
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "studymatch_partecipazione" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "data_iscrizione" date NOT NULL, "stato" bool NOT NULL, "id_gruppo_id" smallint NOT NULL REFERENCES "studymatch_gruppo" ("id_gruppo") DEFERRABLE INITIALLY DEFERRED, "studente_id" bigint NOT NULL REFERENCES "studymatch_studente" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO studymatch_partecipazione VALUES(6,'2026-07-12',1,5,2);
INSERT INTO studymatch_partecipazione VALUES(7,'2026-07-12',1,6,1);
INSERT INTO studymatch_partecipazione VALUES(8,'2026-07-13',1,5,4);
INSERT INTO studymatch_partecipazione VALUES(9,'2026-07-13',1,5,5);
INSERT INTO studymatch_partecipazione VALUES(10,'2026-07-13',1,5,6);
INSERT INTO studymatch_partecipazione VALUES(11,'2026-07-13',1,9,3);
INSERT INTO studymatch_partecipazione VALUES(12,'2026-07-16',1,7,2);
CREATE TABLE IF NOT EXISTS "studymatch_svolgimento" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "data_svolgimento" date NOT NULL, "id_esame_id" smallint NOT NULL REFERENCES "studymatch_esame" ("id_esame") DEFERRABLE INITIALLY DEFERRED, "studente_id" bigint NOT NULL REFERENCES "studymatch_studente" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "studymatch_admin" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "admin_id" varchar(50) NOT NULL REFERENCES "studymatch_utente" ("utente") DEFERRABLE INITIALLY DEFERRED, "data_nomina" date NOT NULL, "livello" smallint NOT NULL, "notifica_id" varchar(50) NULL REFERENCES "studymatch_utente" ("utente") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO studymatch_admin VALUES(1,'m.rossi_test01','2026-07-09',1,NULL);
INSERT INTO studymatch_admin VALUES(2,'test_user_7z3q','2026-07-09',1,NULL);
INSERT INTO studymatch_admin VALUES(4,'d.romano_admin','2026-07-13',1,NULL);
INSERT INTO studymatch_admin VALUES(5,'s.greco_didattica','2026-07-13',1,NULL);
CREATE TABLE IF NOT EXISTS "studymatch_studente" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "corso_laurea" varchar(100) NOT NULL, "studente_id" varchar(50) NOT NULL REFERENCES "studymatch_utente" ("utente") DEFERRABLE INITIALLY DEFERRED, "anno_corso" smallint NOT NULL);
INSERT INTO studymatch_studente VALUES(1,'Fisica','user_8x92k',1);
INSERT INTO studymatch_studente VALUES(2,'Cybersecurity','studente_dev_x92',2);
INSERT INTO studymatch_studente VALUES(3,'Ingegneria Informatica','Luc.martin023',2);
INSERT INTO studymatch_studente VALUES(4,'Cybersecurity','a.neri_netsec',2);
INSERT INTO studymatch_studente VALUES(5,'Cybersecurity','c.volpi_redteam',2);
INSERT INTO studymatch_studente VALUES(6,'Cybersecurity','s.barbieri_crypto',2);
CREATE TABLE IF NOT EXISTS "studymatch_tutor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "dipartimento" varchar(128) NOT NULL, "area_competenza" varchar(128) NOT NULL, "tutor_id" varchar(50) NOT NULL REFERENCES "studymatch_utente" ("utente") DEFERRABLE INITIALLY DEFERRED, "laurea" varchar(100) NULL);
INSERT INTO studymatch_tutor VALUES(1,'Dipartimento di Ingegneria dell''Informazione','Ingegneria dell''Informazione e Informatica','tutor_demo_user','Cybersecurity');
INSERT INTO studymatch_tutor VALUES(2,'Dipartimento di Matematica','Scienze Matematiche, Fisiche e Naturali','soprano_olong90','Fisica');
INSERT INTO studymatch_tutor VALUES(3,'Dipartimento di Elettronica, Informazione e Bioingegneria','Strutture Dati, Basi di Dati e Ingegneria del Software','g.conti_dev','Ingegneria Informatica');
INSERT INTO studymatch_tutor VALUES(4,' Dipartimento di Elettronica e Telecomunicazioni','Elettronica Analogica e Digitale, Teoria dei Circuiti e Microelettronica','a.ferrari_elec','Ingegneria Elettronica');
INSERT INTO studymatch_tutor VALUES(5,' Dipartimento di Ingegneria Gestionale ','Ricerca Operativa, Economia Aziendale, Gestione della Produzione e Logistica','l.bianchi_mgmt','Ingegneria Gestionale');
CREATE TABLE IF NOT EXISTS "studymatch_utente" ("utente" varchar(50) NOT NULL PRIMARY KEY, "email" varchar(128) NOT NULL, "password" varchar(256) NOT NULL, "ruolo" varchar(20) NOT NULL, "cognome" varchar(50) NULL, "nome" varchar(50) NULL);
INSERT INTO studymatch_utente VALUES('user_8x92k','prova_generica_2026@studenti.uniparthenope.it','09ff5d7bb6bf7df01103b8dbb75cf53b$d7dad32755647826952b3fd3e7472aa5985d721c96062b645789df4171d3a999','studente',NULL,NULL);
INSERT INTO studymatch_utente VALUES('m.rossi_test01','test.admin_@uniparthenope.it','74a4edb0e401aac5531a490247c29f3b$131ba7659717e695c69604977e13b378028889ed1fbedacdceaec2297f9ed0f3','admin',NULL,NULL);
INSERT INTO studymatch_utente VALUES('test_user_7z3q','simulazione.esame_2026@studenti.uniparthenope.it','431e04c42a14675e5693a72989c93179$26e2890eb3bb1bbed7143270ec0d09bb1c569509a88e0f536d7ccf98062e85d8','admin',NULL,NULL);
INSERT INTO studymatch_utente VALUES('studente_dev_x92','progetto.test_2026@universita-demo.it','f829d464f6f0cee22b0e3f5adb0ace19$39e55dd05e96dcd5ffa2af19fe3d44421558dca281c2e1cca2314a513cc5226c','studente',NULL,NULL);
INSERT INTO studymatch_utente VALUES('tutor_demo_user','tutor.demo@test.it','c33beef5207638c06a18ea15f9821571$5e48094610c53943840c2e3fc0dd3792c872c7daf531cbbbbe3ad9f30cbf9433','tutor',NULL,NULL);
INSERT INTO studymatch_utente VALUES('soprano_olong90','soprano_olong90@test.local','c443840c11ea36e8dd10f52f5f644b25$0698a6ee64af6fc371f9388e44fde900851efad167032898fd4124fa3b82060d','tutor','','');
INSERT INTO studymatch_utente VALUES('g.conti_dev','giulia.conti@politecnico-test.it','ca443b2e9ba0d5e37be5d82982645311$b18d9fe451a6f8d1563294c52281ea1b816d42ac6879e349b7616da90b2cde26','tutor','Conti','Giulia');
INSERT INTO studymatch_utente VALUES('a.ferrari_elec','alessandro.ferrari@politecnico-test.it','ad0ff36f01e10a0c52e10ecf5db51409$2123e0c9e3ae01ac46440c661c9371dac804d514420ddb6ae2bf1cb6a2f9de52','tutor','Ferrari','Alessandro');
INSERT INTO studymatch_utente VALUES('l.bianchi_mgmt','laura.bianchi@politecnico-test.it','e2e85000450844ad63091e6584915fc1$c11a92e6335f611dbf254958c400a0d4e50f7c63a076998a8ef6c1c75690734a','tutor','Bianchi','Laura');
INSERT INTO studymatch_utente VALUES('d.romano_admin','davide.romano@politecnico-test.it','90f45d1b20d1defef49a4e0b2c06ea62$748809d3078dba3f3044a09df166a338726d147d717ae43534f6937d2331dc7f','admin','Romano','Davide');
INSERT INTO studymatch_utente VALUES('Luc.martin023','luca.martini@studenti.politecnico-test.it','25c6ee741fbed184a577dab7f478e590$110271508fc43c2648e6cb2c2a340c7edfd3eea5b0137f1d40de5638759c8c3f','studente','Martini','Luca');
INSERT INTO studymatch_utente VALUES('a.neri_netsec','','63550e0cc841dc25cc2b8311b898f850$08a2c83467fec8cc584163953b5ec1f4424fa2752e4a58c6b6b90fa77d232db7','studente','Neri','Andrea');
INSERT INTO studymatch_utente VALUES('c.volpi_redteam','chiara.volpi@studenti.politecnico-test.it','2fd7869b8fb0e67f97b9917e1d4e969e$197b95ff2a545b8dfeb0f0c75c17e1af6fd6b0a3ba8a5698483fa52f74594c91','studente','Volpi','Chiara');
INSERT INTO studymatch_utente VALUES('s.barbieri_crypto','','a79c47d2cbbe10a5ccc406ec76f3a579$a76bc8c4e10e1c3e97965c42a2ec54c818eef23bc0395b2fb57b59829227c372','studente','','');
CREATE TABLE IF NOT EXISTS "studymatch_esame" ("id_esame" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nome_esame" varchar(50) NOT NULL, "corso" varchar(100) NOT NULL, "cfu" smallint NOT NULL, "semestre" smallint NOT NULL, "anno_corso" smallint NOT NULL);
INSERT INTO studymatch_esame VALUES(1,'Fisica Generale','Fisica',6,1,1);
INSERT INTO studymatch_esame VALUES(2,'Crittografia','Cybersecurity',6,1,2);
INSERT INTO studymatch_esame VALUES(3,'Base di Dati','Cybersecurity',6,2,2);
INSERT INTO studymatch_esame VALUES(4,'Base di Dati','Informatica',9,1,2);
INSERT INTO studymatch_esame VALUES(5,'Linguaggi','Ingegneria Informatica',6,1,2);
INSERT INTO studymatch_esame VALUES(6,'Sistemi Operativi','Cybersecurity',9,1,2);
INSERT INTO studymatch_esame VALUES(7,'Sistemi Operativi','Informatica',9,1,2);
INSERT INTO studymatch_esame VALUES(8,'Sistemi Operativi','Ingegneria Informatica',9,1,2);
INSERT INTO studymatch_esame VALUES(9,'Antropologia','Lettere',11,2,1);
CREATE TABLE IF NOT EXISTS "studymatch_gestione" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "admin_id" bigint NOT NULL REFERENCES "studymatch_admin" ("id") DEFERRABLE INITIALLY DEFERRED, "id_gruppo_id" smallint NOT NULL REFERENCES "studymatch_gruppo" ("id_gruppo") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO studymatch_gestione VALUES(5,1,5);
INSERT INTO studymatch_gestione VALUES(6,1,6);
INSERT INTO studymatch_gestione VALUES(7,2,6);
INSERT INTO studymatch_gestione VALUES(8,2,5);
INSERT INTO studymatch_gestione VALUES(9,4,7);
INSERT INTO studymatch_gestione VALUES(10,1,8);
INSERT INTO studymatch_gestione VALUES(11,4,8);
INSERT INTO studymatch_gestione VALUES(12,4,9);
INSERT INTO studymatch_gestione VALUES(13,4,10);
CREATE TABLE IF NOT EXISTS "studymatch_materiale" ("tipo" varchar(5) NOT NULL, "file" varchar(100) NULL, "url" varchar(200) NULL, "data_caricamento" date NOT NULL, "nome_file" varchar(150) NOT NULL PRIMARY KEY);
INSERT INTO studymatch_materiale VALUES('txt','materiali/about-gpu-2026-04-18T16-27-09-294Z.txt',NULL,'2026-07-10','about-gpu-2026-04-18T16-27-09-294Z.txt');
INSERT INTO studymatch_materiale VALUES('pdf','materiali/Advanced_Programming_in_the_UNIX_Environment.pdf',NULL,'2026-07-10','Advanced Programming in the UNIX Environment.pdf');
INSERT INTO studymatch_materiale VALUES('file','materiali/bulma.scss',NULL,'2026-07-12','bulma.scss');
CREATE TABLE IF NOT EXISTS "studymatch_condivisione" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "file_id" varchar(150) NOT NULL REFERENCES "studymatch_materiale" ("nome_file") DEFERRABLE INITIALLY DEFERRED, "id_gruppo_id" smallint NOT NULL REFERENCES "studymatch_gruppo" ("id_gruppo") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO studymatch_condivisione VALUES(3,'bulma.scss',5);
CREATE TABLE IF NOT EXISTS "studymatch_supporto" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "punteggio" integer NULL, "id_gruppo_id" smallint NOT NULL REFERENCES "studymatch_gruppo" ("id_gruppo") DEFERRABLE INITIALLY DEFERRED, "tutor_id" bigint NOT NULL REFERENCES "studymatch_tutor" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO studymatch_supporto VALUES(4,NULL,5,1);
INSERT INTO studymatch_supporto VALUES(5,NULL,5,2);
INSERT INTO studymatch_supporto VALUES(6,NULL,5,3);
INSERT INTO studymatch_supporto VALUES(7,NULL,6,4);
INSERT INTO studymatch_supporto VALUES(8,NULL,5,4);
CREATE TABLE IF NOT EXISTS "studymatch_gruppo" ("id_gruppo" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nome_gruppo" varchar(50) NOT NULL, "max_partecipanti" smallint NOT NULL, "link_chat" text NULL, "descrizione" text NULL);
INSERT INTO studymatch_gruppo VALUES(5,'CIAO',20,'https://teams.cloud.microsoft/l/team/19%3AdsUGVEx32_-v2zhMa-FsTcAQ7wpYyOF_nNm45eHniaI1%40thread.tacv2/conversations?groupId=ffb4ffed-5861-409e-9943-04f31e548e9b&tenantId=017e16ae-f415-4f8d-9af0-a21b57cd448e','');
INSERT INTO studymatch_gruppo VALUES(6,'Fisica Quantisticl',25,'https://teams.cloud.microsoft/l/team/19%3AWU4-gGWEOnpndRP7fZhl9W9J37NTdNuGtLm9NZYhFK81%40thread.tacv2/conversations?groupId=f881db95-394e-4c37-8339-574b61de88ce&tenantId=017e16ae-f415-4f8d-9af0-a21b57cd448e',' gruppi quantistici sono algebre non commutative che generalizzano le strutture dei gruppi di Lie e delle algebre di Hopf.  Formalizzati negli anni ''80 da Vladimir Drinfeld e Michio Jimbo, rappresentano una "deformazione" di algebre classiche dipendenti da un parametro');
INSERT INTO studymatch_gruppo VALUES(7,'SecureOS Lab',5,'https://andreatv123@comc',replace(replace('Gruppo dedicato all''approfondimento dei meccanismi di sicurezza nei sistemi operativi moderni. Le sessioni si concentreranno su:\r\nGestione della sicurezza: Implementazione di policy di controllo accessi (DAC, MAC, RBAC) in ambienti Linux e Windows.\r\nProtezione della memoria: Analisi e prevenzione di vulnerabilità come buffer overflow e race conditions.\r\nVirtualizzazione Sicura: Studio degli isolamenti tramite hypervisor e container (Docker/Kubernetes) in ottica security.\r\nHardening: Tecniche per la messa in sicurezza del kernel e configurazione di sistemi minimali per ambienti critici.\r\nLaboratorio Pratico: Esercitazioni su codice C/Assembly per comprendere le primitive di sincronizzazione e le falle di sicurezza a basso livello.','\r',char(13)),'\n',char(10)));
INSERT INTO studymatch_gruppo VALUES(8,'OS Core Engineering',4,'',replace(replace('Gruppo focalizzato sulla comprensione profonda dell''architettura e della gestione delle risorse nei sistemi operativi moderni (Linux/Unix-based). Le sessioni copriranno:\r\nGestione Processi e Thread: Creazione (fork, exec), sincronizzazione (mutex, semafori) e comunicazione interprocesso (pipe, shared memory).\r\nScheduling della CPU: Analisi comparativa degli algoritmi (Round Robin, SJF, Multilevel Queue) e calcolo dei tempi di attesa/risposta.\r\nGestione Memoria: Paginazione, segmentazione, algoritmi di sostituzione (LRU, FIFO) e simulazione del fenomeno del thrashing.\r\nFile System: Strutture di allocazione (i-node, FAT), gestione dello spazio libero e implementazione di comandi shell per la manipolazione file.\r\nLaboratorio C/Shell: Risoluzione di esercizi pratici di programmazione di sistema e scripting per l''automazione di task amministrativi.','\r',char(13)),'\n',char(10)));
INSERT INTO studymatch_gruppo VALUES(9,'OS Performance & Architecture',8,'',replace(replace('Sistemi Operativi (Ingegneria Informatica/Elettronica)\r\nDescrizione: Gruppo tecnico dedicato all''analisi quantitativa e alla progettazione di meccanismi interni del sistema operativo. Le sessioni si concentrano su:\r\nAnalisi degli Algoritmi di Scheduling: Calcolo manuale e comparativo di tempi di attesa, turnaround e risposta per algoritmi FCFS, SJF, Round Robin e Multilevel Queue. Simulazione di scenari di starvation e ottimizzazione del throughput.\r\nGestione della Memoria e Paging: Risoluzione di esercizi su traduzione indirizzi logici/fisici, calcolo della dimensione delle tabelle delle pagine e simulazione di algoritmi di sostituzione (LRU, FIFO, Optimal) per minimizzare i page fault.\r\nPrevenzione del Thrashing: Analisi del modello Working Set e calcolo del grado di multiprogrammazione ottimale per evitare il degrado delle prestazioni.\r\nScheduling del Disco: Ottimizzazione dei tempi di seek con algoritmi SCAN, C-SCAN e LOOK su trace di richieste I/O reali.\r\nProgrammazione di Sistema (C/POSIX): Implementazione efficiente di primitive di sincronizzazione (semafori, mutex) e risoluzione di problemi classici (Produttore-Consumatore, Lettori-Scrittori) con attenzione alle race condition e al deadlock.','\r',char(13)),'\n',char(10)));
INSERT INTO studymatch_gruppo VALUES(10,'ANTROPOLOGOIA',3,'','');
CREATE TABLE IF NOT EXISTS "studymatch_assegnazione" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "id_esame_id" smallint NOT NULL REFERENCES "studymatch_esame" ("id_esame") DEFERRABLE INITIALLY DEFERRED, "id_gruppo_id" smallint NOT NULL REFERENCES "studymatch_gruppo" ("id_gruppo") DEFERRABLE INITIALLY DEFERRED, "periodo" datetime NOT NULL);
INSERT INTO studymatch_assegnazione VALUES(5,2,5,'2026-08-11T13:52:07.969650+00:00');
INSERT INTO studymatch_assegnazione VALUES(6,1,6,'2026-07-26 13:53:55.002626');
INSERT INTO studymatch_assegnazione VALUES(7,6,7,'2026-08-12 16:09:20.505150');
INSERT INTO studymatch_assegnazione VALUES(8,7,8,'2026-09-11 16:18:37.515201');
INSERT INTO studymatch_assegnazione VALUES(9,8,9,'2026-09-11 16:21:18.380643');
INSERT INTO studymatch_assegnazione VALUES(10,9,10,'2026-08-15 14:28:03.384770');
CREATE TABLE IF NOT EXISTS "studymatch_invio" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "testo" text NOT NULL, "data_invio" datetime NOT NULL, "letta" bool NOT NULL, "destinatario_id" varchar(50) NOT NULL REFERENCES "studymatch_utente" ("utente") DEFERRABLE INITIALLY DEFERRED, "mittente_id" bigint NOT NULL REFERENCES "studymatch_admin" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO studymatch_invio VALUES(3,'Buongiorno come va?','2026-07-12 15:51:15.940885',1,'test_user_7z3q',1);
INSERT INTO studymatch_invio VALUES(4,'Buongiorno come va?','2026-07-12 15:51:15.950006',1,'studente_dev_x92',1);
INSERT INTO studymatch_invio VALUES(5,'Buongiorno come state?','2026-07-12 15:53:11.226131',1,'m.rossi_test01',2);
INSERT INTO studymatch_invio VALUES(6,'Buongiorno come state?','2026-07-12 15:53:11.235402',1,'studente_dev_x92',2);
INSERT INTO studymatch_invio VALUES(8,'Buongiorno, A tutti i partecipanti dico che oggi il gruppo sarà in manuntenzione...','2026-07-12 16:00:14.305938',0,'tutor_demo_user',2);
INSERT INTO studymatch_invio VALUES(9,'Buongiorno, A tutti i partecipanti dico che oggi il gruppo sarà in manuntenzione...','2026-07-12 16:00:14.309451',1,'g.conti_dev',2);
INSERT INTO studymatch_invio VALUES(10,'Buongiorno, A tutti i partecipanti dico che oggi il gruppo sarà in manuntenzione...','2026-07-12 16:00:14.312707',1,'studente_dev_x92',2);
INSERT INTO studymatch_invio VALUES(11,'Buongiorno, A tutti i partecipanti dico che oggi il gruppo sarà in manuntenzione...','2026-07-12 16:00:14.316061',0,'a.ferrari_elec',2);
INSERT INTO studymatch_invio VALUES(12,'Buongiorno, A tutti i partecipanti dico che oggi il gruppo sarà in manuntenzione...','2026-07-12 16:00:14.318841',1,'m.rossi_test01',2);
INSERT INTO studymatch_invio VALUES(13,'Buongiorno faremo una conversazione alle 18: 00','2026-07-16 15:07:22.735190',0,'m.rossi_test01',4);
INSERT INTO studymatch_invio VALUES(14,'Saremo operativi oggi verso le 18:45','2026-07-16 15:25:02.612581',0,'m.rossi_test01',4);
INSERT INTO studymatch_invio VALUES(15,'Buongiorno. invio una NEWSLETTER.','2026-07-16 15:30:31.131733',1,'studente_dev_x92',4);
INSERT INTO studymatch_invio VALUES(16,'Buongiorno a tutti operiamo per chi vuole deve sostenere l''esame fra poco!','2026-07-19 08:49:58.241123',0,'soprano_olong90',1);
INSERT INTO studymatch_invio VALUES(17,'Buongiorno a tutti operiamo per chi vuole deve sostenere l''esame fra poco!','2026-07-19 08:49:58.246156',0,'a.ferrari_elec',1);
INSERT INTO studymatch_invio VALUES(18,'Buongiorno a tutti operiamo per chi vuole deve sostenere l''esame fra poco!','2026-07-19 08:49:58.249134',0,'tutor_demo_user',1);
INSERT INTO studymatch_invio VALUES(19,'Buongiorno a tutti operiamo per chi vuole deve sostenere l''esame fra poco!','2026-07-19 08:49:58.251826',0,'studente_dev_x92',1);
INSERT INTO studymatch_invio VALUES(20,'Buongiorno a tutti operiamo per chi vuole deve sostenere l''esame fra poco!','2026-07-19 08:49:58.254723',0,'s.barbieri_crypto',1);
INSERT INTO studymatch_invio VALUES(21,'Buongiorno a tutti operiamo per chi vuole deve sostenere l''esame fra poco!','2026-07-19 08:49:58.257673',0,'g.conti_dev',1);
INSERT INTO studymatch_invio VALUES(22,'Buongiorno a tutti operiamo per chi vuole deve sostenere l''esame fra poco!','2026-07-19 08:49:58.260505',0,'c.volpi_redteam',1);
INSERT INTO studymatch_invio VALUES(23,'Buongiorno a tutti operiamo per chi vuole deve sostenere l''esame fra poco!','2026-07-19 08:49:58.263847',0,'test_user_7z3q',1);
INSERT INTO studymatch_invio VALUES(24,'Buongiorno a tutti operiamo per chi vuole deve sostenere l''esame fra poco!','2026-07-19 08:49:58.266832',0,'a.neri_netsec',1);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('django_migrations',31);
INSERT INTO sqlite_sequence VALUES('django_content_type',19);
INSERT INTO sqlite_sequence VALUES('auth_permission',76);
INSERT INTO sqlite_sequence VALUES('auth_group',0);
INSERT INTO sqlite_sequence VALUES('auth_user',0);
INSERT INTO sqlite_sequence VALUES('studymatch_admin',5);
INSERT INTO sqlite_sequence VALUES('studymatch_studente',6);
INSERT INTO sqlite_sequence VALUES('studymatch_tutor',5);
INSERT INTO sqlite_sequence VALUES('studymatch_esame',9);
INSERT INTO sqlite_sequence VALUES('studymatch_gestione',13);
INSERT INTO sqlite_sequence VALUES('studymatch_partecipazione',12);
INSERT INTO sqlite_sequence VALUES('studymatch_supporto',8);
INSERT INTO sqlite_sequence VALUES('studymatch_condivisione',3);
INSERT INTO sqlite_sequence VALUES('studymatch_gruppo',10);
INSERT INTO sqlite_sequence VALUES('studymatch_assegnazione',10);
INSERT INTO sqlite_sequence VALUES('studymatch_invio',24);
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");
CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");
CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE UNIQUE INDEX "studymatch_partecipazione_studente_id_id_gruppo_id_1d4ce08a_uniq" ON "studymatch_partecipazione" ("studente_id", "id_gruppo_id");
CREATE INDEX "studymatch_partecipazione_id_gruppo_id_e6f11b2d" ON "studymatch_partecipazione" ("id_gruppo_id");
CREATE INDEX "studymatch_partecipazione_studente_id_c8241c52" ON "studymatch_partecipazione" ("studente_id");
CREATE UNIQUE INDEX "studymatch_svolgimento_studente_id_id_esame_id_24920ad9_uniq" ON "studymatch_svolgimento" ("studente_id", "id_esame_id");
CREATE INDEX "studymatch_svolgimento_id_esame_id_893b340c" ON "studymatch_svolgimento" ("id_esame_id");
CREATE INDEX "studymatch_svolgimento_studente_id_ec3b8eff" ON "studymatch_svolgimento" ("studente_id");
CREATE INDEX "studymatch_admin_admin_id_40d6192c" ON "studymatch_admin" ("admin_id");
CREATE INDEX "studymatch_studente_studente_id_cfc4e5bf" ON "studymatch_studente" ("studente_id");
CREATE INDEX "studymatch_tutor_tutor_id_93217784" ON "studymatch_tutor" ("tutor_id");
CREATE UNIQUE INDEX "studymatch_gestione_admin_id_id_gruppo_id_f8f9dcd2_uniq" ON "studymatch_gestione" ("admin_id", "id_gruppo_id");
CREATE INDEX "studymatch_gestione_admin_id_89f0aebe" ON "studymatch_gestione" ("admin_id");
CREATE INDEX "studymatch_gestione_id_gruppo_id_a8c989e7" ON "studymatch_gestione" ("id_gruppo_id");
CREATE INDEX "studymatch_admin_notifica_id_46bd9428" ON "studymatch_admin" ("notifica_id");
CREATE UNIQUE INDEX "studymatch_condivisione_file_id_id_gruppo_id_14fff5ae_uniq" ON "studymatch_condivisione" ("file_id", "id_gruppo_id");
CREATE INDEX "studymatch_condivisione_file_id_b543d0c4" ON "studymatch_condivisione" ("file_id");
CREATE INDEX "studymatch_condivisione_id_gruppo_id_b96875ac" ON "studymatch_condivisione" ("id_gruppo_id");
CREATE UNIQUE INDEX "studymatch_supporto_tutor_id_id_gruppo_id_bb897892_uniq" ON "studymatch_supporto" ("tutor_id", "id_gruppo_id");
CREATE INDEX "studymatch_supporto_id_gruppo_id_53bf06a9" ON "studymatch_supporto" ("id_gruppo_id");
CREATE INDEX "studymatch_supporto_tutor_id_fd9c265f" ON "studymatch_supporto" ("tutor_id");
CREATE TRIGGER trg_partecipazione_capienza_insert
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
CREATE TRIGGER trg_partecipazione_capienza_update
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
CREATE TRIGGER trg_gruppo_modifica_capienza
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
CREATE TRIGGER trg_studente_specializzazione
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
CREATE TRIGGER trg_tutor_specializzazione
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
CREATE TRIGGER trg_admin_specializzazione
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
CREATE TRIGGER trg_utente_ruolo_specializzazione_update
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
CREATE TRIGGER trg_supporto_limite_tutor_insert
                BEFORE INSERT ON studymatch_supporto
                FOR EACH ROW

                WHEN (
                    SELECT COUNT(*)
                    FROM studymatch_supporto
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                ) >= 4

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Un gruppo non può avere più di 4 tutor'
                    );
                END;
CREATE TRIGGER trg_supporto_limite_tutor_update
                BEFORE UPDATE OF id_gruppo_id
                ON studymatch_supporto
                FOR EACH ROW

                WHEN NEW.id_gruppo_id != OLD.id_gruppo_id
                AND (
                    SELECT COUNT(*)
                    FROM studymatch_supporto
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                ) >= 4

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Un gruppo non può avere più di 4 tutor'
                    );
                END;
CREATE TRIGGER trg_gestione_limite_admin_insert
                BEFORE INSERT ON studymatch_gestione
                FOR EACH ROW

                WHEN (
                    SELECT COUNT(*)
                    FROM studymatch_gestione
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                ) >= 2

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Un gruppo non può avere più di 2 amministratori'
                    );
                END;
CREATE TRIGGER trg_gestione_limite_admin_update
                BEFORE UPDATE OF id_gruppo_id
                ON studymatch_gestione
                FOR EACH ROW

                WHEN NEW.id_gruppo_id != OLD.id_gruppo_id
                AND (
                    SELECT COUNT(*)
                    FROM studymatch_gestione
                    WHERE id_gruppo_id = NEW.id_gruppo_id
                ) >= 2

                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Un gruppo non può avere più di 2 amministratori'
                    );
                END;
CREATE UNIQUE INDEX "studymatch_assegnazione_id_esame_id_id_gruppo_id_742068d0_uniq" ON "studymatch_assegnazione" ("id_esame_id", "id_gruppo_id");
CREATE INDEX "studymatch_assegnazione_id_esame_id_2754bfb1" ON "studymatch_assegnazione" ("id_esame_id");
CREATE INDEX "studymatch_assegnazione_id_gruppo_id_ec5abfa5" ON "studymatch_assegnazione" ("id_gruppo_id");
CREATE INDEX "studymatch_invio_destinatario_id_8e86afe1" ON "studymatch_invio" ("destinatario_id");
CREATE INDEX "studymatch_invio_mittente_id_5b606c3e" ON "studymatch_invio" ("mittente_id");
COMMIT;
