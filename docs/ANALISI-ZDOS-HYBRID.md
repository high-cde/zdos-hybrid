# ZDOS Hybrid · Analisi tecnica del repository

| Campo | Valore |
|---|---|
| Repository | `high-cde/zdos-hybrid` (public) |
| Branch predefinito analizzato | `feat/zdos-hybrid-security-20261001-230859` |
| Commit di riferimento | `c46d1a4` — *feat(zk-launch): add absolute path launcher for zk command and background node orchestration* |
| Data analisi | 2026-10-02 |
| Metodo | ispezione del codice, `git log`, confronto generatori/artefatti, build e test reali del workspace Rust su toolchain stabile, esecuzione della GUI sotto Xvfb |

Questa analisi distingue sempre fra **ciò che è stato verificato eseguendo** e
ciò che è soltanto **dichiarato** dalla documentazione del repository.

---

## 1. Sintesi esecutiva

ZDOS Hybrid è un **clone evoluto di `zdos-organism`** (runtime bio-computazionale
Rust) sovrapposto a un **layer ibrido "security workstation"**: interfacce Tkinter,
una webapp gestionale, script di ancoraggio desktop e riferimenti a un modulo
Android/Expo (`zdos-microcosm-beta`) e al compilatore `Zlang`.

Lo stato reale è **"foundation + prototipo ibrido"**, con tre problemi bloccanti
che la documentazione attuale non riporta:

1. **Il workspace Rust non compila** in questo branch: `clippy` e `test`
   falliscono con sei errori distribuiti su tre crate (`cortex`, `core`,
   `organism-bin`): un'API rinominata e dipendenze non dichiarate nei
   `Cargo.toml` (§3).
2. **La CI non può accorgersene**: i workflow si attivano su push a `main`, ma
   `main` **non esiste**: l'unico branch è quello di feature. I quality gate
   dichiarati dal README non sono mai stati eseguiti.
3. **Il layer ibrido fa riferimento a moduli assenti**: `Zlang/` e
   `zdos-microcosm-beta/` sono presenti come directory ma contengono **0 file
   tracciati da git**. Il launcher `zk` li richiama comunque.

A questi si aggiungono difetti di igiene (percorsi `/home/ruby` hard-coded,
virtualenv e artefatti di macchina committati, drift fra generatore e artefatto)
dettagliati nella sezione 6.

---

## 2. Cos'è il repository

`git log` mostra una storia lineare con due anime:

| Fase | Commit rappresentativi | Contenuto |
|---|---|---|
| Organismo Rust | `c7508c3`, `d477feb`, `b5cefae`, `b1e546d` | workspace Cargo, ZLang/ZVM, BioFeedback, CI e wiki |
| Migrazione ibrida | `ac33cc3`, `c46d1a4` | strumenti Python/Shell, GUI, webapp, launcher `zk`, audit di migrazione |

Il README e la documentazione continuano però a descrivere il repository come
`high-cde/zdos-organism`:

| Superficie | Identità dichiarata |
|---|---|
| `README.md` (titolo) | «ZDOS Organism — Bio-Computational Adaptive System» |
| `docs/OVERVIEW.md`, `docs/wiki/*` | identità `high-cde/zdos-organism` |
| `SECURITY.md` | «riguarda il repository `high-cde/zdos-organism`» |
| `zdos-status.sh`, `zdos-brain.sh`, `zdos-v20.sh` | radice `$HOME/zdos-organism` |
| `zdos_zk_launch.py`, `zdos-os.desktop` | radice `/home/ruby/zdos-organism` |

Le conseguenze pratiche sono due: la documentazione non descrive il layer ibrido
(che è la ragione d'essere di `zdos-hybrid`), e i percorsi assoluti della
macchina di origine rompono l'avvio su qualunque altro utente o host.

---

## 3. Stato verificato (eseguito il 2026-10-02)

Comandi eseguiti nella root del repository, toolchain Rust stabile:

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-targets --all-features
cargo run -q -p organism-bin -- --eval "+ 2 3"
ZDOS_STATE_DIR=/tmp/zdosvar cargo run -q -p organism-bin -- --once
```

| Gate | Esito reale | Dettaglio |
|---|---|---|
| `cargo fmt --check` | **FAIL** | 10 file con diff di formattazione (es. `organism-bin/src/main.rs`, `zlang/src/compiler.rs`, `zlang/src/runtime.rs`) |
| `cargo clippy` | **FAIL (101)** | errore di compilazione, non un warning |
| `cargo test` | **FAIL (101)** | stessa causa radice |
| `--eval "+ 2 3"` | **FAIL** | la CLI non viene compilata |
| `--once` | **FAIL** | la CLI non viene compilata |

### Causa radice (inventario completo)

Il workspace è rotto in **tre crate**, per due cause distinte: un'API rinominata
e dipendenze non dichiarate nei `Cargo.toml`.

| Crate · posizione | Errore | Causa |
|---|---|---|
| `cortex/src/policy.rs:23` | `E0425` — `cannot find function execute in module runtime` | `zlang::runtime` espone ora `execute_with_vars(code, vars)` |
| `core/src/zvm_executor.rs:2` | `E0433` — `cannot find module or crate zdos_zlang` | `core/Cargo.toml` non dichiara `zdos-zlang` |
| `organism-bin/src/main.rs:2,3,5` | `E0433` ×3 — `zdos_core`, `zdos_cortex`, `zdos_zvm` non risolti | `organism-bin/Cargo.toml` dichiara solo `cortex` e `zdos-zlang`: mancano `zdos-core` e `zdos-zvm`, e l'import `zdos_cortex` non corrisponde alla dipendenza `cortex` |
| `organism-bin/src/main.rs:7,8` | `E0433` + `E0752` — `tokio` non risolto, `main` non può essere `async` | manca la dipendenza `tokio` (feature `macros`/`rt`) |
| `organism-bin/src/main.rs:1` | warning — import `serde_json::json` non usato | pulizia |

Verifica del concatenamento: applicando in un worktree la **sola** correzione di
`policy.rs` (`execute` → `execute_with_vars`) il compilatore non si riprende;
emergono gli errori `E0433` di `core` e `organism-bin` elencati sopra. Non è
quindi un difetto di una riga: le dipendenze vanno riallineate nei `Cargo.toml`
dei crate interessati.

> Il README attuale afferma: *«Il repository è ora compilabile con Rust stabile
> e la CI verifica automaticamente formattazione, Clippy, test e smoke test
> CLI»*. Su questo branch l'affermazione **non è riproducibile**. Il README è
> stato riscritto per riflettere lo stato verificato.

### Perché la CI non intercetta il problema

`.github/workflows/ci.yml` dichiara `on: push: branches: [main]` e
`pull_request`. In questo repository **`main` non esiste**: l'unico branch
remoto è `feat/zdos-hybrid-security-20261001-230859`, verificato con
`git ls-remote --heads origin` e `gh api repos/high-cde/zdos-hybrid/branches`.
I workflow non si sono quindi **mai** attivati: i gate di qualità esistono sulla
carta, non nel percorso reale della migrazione.

---

## 4. Architettura

### 4.1 Runtime Rust (workspace Cargo)

| Crate | Ruolo |
|---|---|
| `organism-bin` | CLI, ciclo vitale, sensori, stato locale (`--eval`, `--once`, daemon) |
| `cortex` | decision engine, feedback omeostatico, evoluzione, bridge LLM |
| `zlang` | parser, AST, compiler verso bytecode |
| `zvm` | bytecode, opcode, stack e macchina virtuale con errori tipizzati |
| `core` | primitive condivise e executor |
| `memzdos` | identità e stato persistente |

Percorso dati dichiarato e coerente con il codice:

```text
SENSORS → NEURO SIGNALS → BIO FEEDBACK → FITNESS
        → MUTATION → OPTIMIZATION → CORTEX DECISION → STATE

source ZLang → Parser → AST → Compiler → BytecodeProgram → ZVM → JSON
```

Il programma canonico del feedback omeostatico è versionato in
`programs/organism/tick.zlang`, con ABI e capability allowlist documentate in
`docs/ORGANISM_ZLANG.md` (shell, rete e credenziali negate: profilo local-only).

### 4.2 Layer ibrido ("security workstation")

| Componente | File | Natura |
|---|---|---|
| Launcher `zk` | `zdos_zk_launch.py` | avvio GUI + Node Pulse in background |
| Glass Engine (GUI principale) | `zdos_omni_os.py` | Tkinter, fullscreen; bridge HTTP su `0.0.0.0:8888` |
| Widget desktop | `z_kali_ui.py`, `z_kali_sovereign.py` | Tkinter, finestra ancorata in basso a destra |
| Dashboard/moduli | `zdos_master_dashboard.py`, `z_kali_megadrive.py`, `z_kali_ruby_city.py` | Tkinter, scenari canvas |
| Core UI glass | `interface/glass/core_ui.py` | stub di stile/descrizione |
| Webapp gestionale | `webapp/index.html`, `webapp/assets/*` | HTML/CSS/JS statico |
| Memoria e attestazioni | `src/neural/z_kali_cortex.py`, `zdos_bridge.py` | stato JSON + ledger append-only (`var/evidence.jsonl`) |
| Pulizia adattiva | `z_kali_cleaner.py` | rimozione cache (`target/debug/incremental`, `__pycache__`, `./var/tmp`) |
| Generator/autobuild | `zdos-autobuild.sh`, `autobuild-*.sh` | ricreano file di progetto in `$HOME/zdos-organism` |
| Ambiente LLM locale | `zdos-llm/`, `llm-mock.py` | virtualenv committato + mock Flask su porta 8080 |
| App mobile | `zdos-microcosm-beta/` | **riferita ma assente** (vedi §6) |

### 4.3 Moduli assenti ma referenziati

```bash
git ls-files | grep -cE '^(Zlang|zdos-microcosm-beta)/'   # → 0
```

Le due directory esistono come contenitori vuoti. Conseguenze:

* `zdos_zk_launch.py` cerca `zdos-microcosm-beta/node/zdos-node.ts` e, se
  presente, avvia `npx tsx`: nel repository attuale il Node Pulse non parte mai.
* `zdos-evolution-deploy.sh` presume di trovare `Zlang/Cargo.toml` e
  `scripts/evolve-zlang-evidence.sh`: entrambi assenti.
* L'audit `.zdos-migration-audit/20261001-230859/report.txt` elenca decine di
  file (`zdos-node.ts`, `package.json`, `lib/zdos-zcomm.ts`, …) mai entrati nel
  commit.

---

## 5. Avvio: comandi reali e limiti

| Comando | Cosa fa oggi |
|---|---|
| `bash zdos-autobuild.sh` | genera webapp, `parrot_theme.py` e una GUI Tkinter **in `$HOME/zdos-organism`** |
| `python3 zdos_zk_launch.py` | risolve la radice, avvia Node Pulse (se esiste) e apre il Glass Engine |
| `./zdos-status.sh --deep` | report ASCII + `cargo build` (fallisce finché la build è rotta) |
| `bash zdos-brain.sh` | autobuild + status + `cargo run -p organism-bin` |

Problemi rilevati nel percorso di avvio:

* percorsi assoluti `/home/ruby/zdos-organism` in `zdos_zk_launch.py` e
  `zdos-os.desktop`: su un utente diverso il launcher non trova l'interfaccia;
* `zdos-autobuild.sh` scrive in `$HOME/zdos-organism` mentre il repository può
  essere clonato altrove (es. `~/zdos-hybrid`): due radici diverse convivono;
* il blocco heredoc finale di `zdos-autobuild.sh` **non era terminato**
  (`here-document delimited by end-of-file`): lo script funzionava per effetto
  collaterale dell'EOF del file. Corretto in questo intervento.

---

## 6. Rilievi, con severità

| # | Rilievo | Severità | Evidenza |
|---|---|---:|---|
| 1 | Workspace non compilabile: 3 crate, sei errori (`E0425`, 4×`E0433`, `E0752`) | **Alta** | `cargo check --workspace --all-targets` |
| 2 | CI mai eseguita: trigger su `main`, ma **`main` non esiste** | **Alta** | `git ls-remote --heads`, `gh api …/branches` |
| 3 | Moduli referenziati ma assenti (`Zlang/`, `zdos-microcosm-beta/`) | **Alta** | 0 file tracciati |
| 4 | Percorsi assoluti `/home/ruby/...` | Media | `zdos_zk_launch.py`, `zdos-os.desktop` |
| 5 | Artefatti di macchina committati: virtualenv `zdos-llm/` (11 MB, Flask/Click/Jinja2), file `time` (261 KB, PostScript ImageMagick), `var/` con stato e ledger | Media | `du -sh`, `file time` |
| 6 | Drift generatore/artefatto: `zdos-autobuild.sh` rigenera una GUI **diversa e più vecchia** di `zdos_omni_os.py` | Media | diff dei blocchi heredoc |
| 7 | Identità documentale incoerente (`zdos-organism` vs `zdos-hybrid`) | Media | README, `docs/*`, `SECURITY.md` |
| 8 | Bridge HTTP su `0.0.0.0:8888` con `Access-Control-Allow-Origin: *` che espone metriche, host locale e indirizzo token a qualunque client della rete | Media | `zdos_omni_os.py` |
| 9 | Cripto residua: polling DexScreener su `TOKEN_ADDRESS`, nonostante il commit `refactor: remove crypto and blockchain integrations` | Bassa | `zdos_omni_os.py` |
| 10 | Finestra «Terminale Root» simulata accanto a pulsanti che eseguono comandi reali (`subprocess`) | Bassa | `zdos_master_dashboard.py` |
| 11 | `zdos-evolution-deploy.sh` esegue `apt-get install` di pacchetti di sistema (inclusi `qemu-*`, `xorriso`) senza conferma | Bassa | script |
| 12 | `z_kali_cleaner.py` rimuove ricorsivamente directory (`target/debug/incremental`, `var/tmp`, `__pycache__`) | Bassa (raggio limitato) | script |
| 13 | Nomenclatura incoerente con l'edizione dichiarata: file e agenti `z_kali_*`, `Z-KALI` accanto a «Parrot Edition» | Bassa | nomi file/etichette |
| 14 | README senza istruzioni per il layer ibrido e senza stato verificabile onesto | Media | riscritto in questo intervento |

Nessuno di questi punti riguarda l'uso duale o l'abuso di sistemi terzi: il
perimetro dichiarato (laboratorio personale, ambienti autorizzati, default-deny)
resta coerente con `SECURITY.md`.

---

## 7. Correzioni consigliate, in ordine di impatto

1. **Ripristinare la build** — correggere `cortex/src/policy.rs`
   (`execute_with_vars`) e riallineare le dipendenze: `zdos-zlang` in `core`;
   `zdos-core`, `zdos-zvm` e `tokio` (feature `macros`/`rt`) in `organism-bin`,
   uniformando l'import di `cortex`. Criterio di completamento:
   `cargo test --workspace --all-targets` verde.
2. **Rendere reale la CI** — creare `main` a partire dal branch corrente oppure
   ampliare il trigger a `push` su tutti i branch; bloccare i merge su
   `fmt`/`clippy`/`test` verdi.
3. **Riportare `Zlang/` e `zdos-microcosm-beta/` nel repository** oppure
   degradare il launcher: se i moduli non ci sono, il comando deve dirlo con
   chiarezza invece di tentare un avvio impossibile.
4. **Eliminare i percorsi assoluti** — usare `ZDOS_ROOT`/`$HOME` (già fatto nel
   launcher in questo intervento) e correggere `zdos-os.desktop`.
5. **Ripulire gli artefatti** — rimuovere `zdos-llm/` (ricreabile con
   `python3 -m venv`), il file `time`, lo stato in `var/` e l'audit di
   migrazione; aggiungerli a `.gitignore`.
6. **Chiudere il bridge** — limitare l'ascolto a `127.0.0.1`, richiedere un
   token di sessione e rimuovere `Access-Control-Allow-Origin: *`.
7. **Allineare l'identità** — `README`/`docs`/`SECURITY` devono parlare di
   `zdos-hybrid` e descrivere esplicitamente il layer ibrido.
8. **Scegliere una sola radice di progetto** (`~/zdos-organism` *oppure* la
   directory del clone) e documentarla.

---

## 8. Interventi applicati in questo lavoro

| Ambito | Modifica |
|---|---|
| Identità visiva | palette Parrot OS applicata a GUI, webapp, dashboard, widget e launcher (`parrot_theme.py`, `assets/theme/parrot-tokens.json`, `docs/theme/PARROT-OS-IDENTITY.md`) |
| Tooling | `tools/apply-parrot-theme.py` (conversione tracciata, modalità `--check`), `tools/sync-autobuild-heredocs.py` (allineamento generatore/artefatti) |
| Launcher `zk` | banner Parrot, risoluzione radice senza percorsi assoluti, flag `--check`/`--no-node`, messaggi d'errore espliciti |
| Autobuild | heredoc finale terminato, generazione di `parrot_theme.py`, branding coerente |
| Documentazione | questo rapporto, il design system e il `README.md` riscritto con stato verificabile |

Gli interventi **non** modificano la logica del runtime Rust: il difetto di
compilazione resta aperto finché non vengono applicate le correzioni del punto 1.

---

## Appendice · Riproduzione

```bash
git clone https://github.com/high-cde/zdos-hybrid.git && cd zdos-hybrid

# qualità del runtime Rust
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test  --workspace --all-targets --all-features

# identità visiva
python3 tools/apply-parrot-theme.py --check
python3 tools/sync-autobuild-heredocs.py --check
python3 zdos_zk_launch.py --check
python3 parrot_theme.py
```
