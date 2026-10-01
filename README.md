![ZDOS Hybrid — Security Workstation](https://capsule-render.vercel.app/api?type=waving&color=0:0A0118,45:06043E,100:15E0ED&height=210&section=header&text=ZDOS%20HYBRID&fontSize=68&fontColor=EAF6FF&animation=fadeIn&fontAlignY=38&desc=Security%20Workstation%20%C2%B7%20Parrot%20Edition&descAlignY=60&descSize=18)

![ZDOS Hybrid](https://img.shields.io/badge/ZDOS_HYBRID-Parrot_Edition-15E0ED?style=for-the-badge&logo=linux&logoColor=black)
![Parrot OS](https://img.shields.io/badge/identit%C3%A0-Parrot_OS_%C2%ABEcho%C2%BB-00D3F2?style=for-the-badge&logo=parrotsecurity&logoColor=black)
![Rust](https://img.shields.io/badge/Rust-stable-000000?style=for-the-badge&logo=rust)
![ZLang](https://img.shields.io/badge/ZLang-ZLB2_runtime-0A0118?style=for-the-badge&logo=gnubash&logoColor=00FFF0)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Licenza](https://img.shields.io/badge/licenza-MIT-3DDC97?style=for-the-badge)
![Analisi](https://img.shields.io/badge/analisi-tecnica_disponibile-8799B5?style=for-the-badge&logo=readthedocs&logoColor=white)

# ZDOS Hybrid — Security Workstation

**ZDOS Hybrid** è l'evoluzione ibrida dell'ecosistema ZDOS. Nasce dal runtime
bio-computazionale Rust di `zdos-organism` e vi sovrappone un livello
**workstation di sicurezza**: interfacce grafiche Tkinter, una webapp
gestionale, memoria persistente con ledger di attestazioni e script di
ancoraggio desktop.

> **Identità visiva.** L'interfaccia adotta la palette di **Parrot OS 7
> «Echo»** (KDE Plasma 6, temi Flat Remix + Sweet Mars): fondo notte
> `#0A0118`, indaco profondo `#06043E`, ciano di marca `#15E0ED` e neon
> `#00FFF0` per gli elementi attivi.

---

## 🚀 Avvio rapido

```bash
git clone https://github.com/high-cde/zdos-hybrid.git
cd zdos-hybrid

# 1. verifica dei prerequisiti dell'interfaccia
python3 zdos_zk_launch.py --check

# 2. apertura della workstation (Glass Engine · Parrot Edition)
python3 zdos_zk_launch.py

# 3. stato dell'ecosistema
./zdos-status.sh --deep
```

| Comando | Effetto |
|---|---|
| `python3 zdos_zk_launch.py` | avvia il Glass Engine e, se presente, il Node Pulse ZComm |
| `python3 zdos_zk_launch.py --check` | verifica prerequisiti e percorsi senza aprire finestre |
| `python3 zdos_zk_launch.py --no-node` | apre solo l'interfaccia |
| `ZDOS_ROOT=/percorso python3 zdos_zk_launch.py` | forza la radice del progetto |
| `bash zdos-autobuild.sh` | rigenera webapp, design system e interfaccia |
| `cargo test --workspace --all-targets --all-features` | gate di qualità del runtime Rust |

Il launcher risolve la radice in questo ordine: `--root` → `ZDOS_ROOT` →
`~/zdos-organism` → directory dello script. **Nessun percorso assoluto
hard-coded.**

---

## 🎨 Identità visiva · Parrot OS «Echo»

| Ruolo | Token | Valore |
|---|---|---|
| Fondo applicazione | `bg_deep` | `#04010F` |
| Fondo di marca | `bg` | `#0A0118` |
| Pannelli | `panel` / `panel_alt` | `#0F0A1E` / `#131038` |
| Barre e header | `surface` | `#06043E` |
| Accento di marca | `cyan` | `#15E0ED` |
| Neon / voce attiva | `cyan_hi` | `#00FFF0` |
| Secondario | `violet` | `#7C3AED` |
| Testo primario / attenuato | `text` / `text_muted` | `#EAF6FF` / `#8799B5` |

![Glass Engine · Parrot Edition](docs/theme/preview/glass-engine-parrot-edition.png)

*Glass Engine con la palette Parrot: barra di identità ciano, superfici
indaco profondo, tipografia `Ubuntu` + `JetBrains Mono`.*

Documentazione completa del design system: **[docs/theme/PARROT-OS-IDENTITY.md](docs/theme/PARROT-OS-IDENTITY.md)**.
Token machine-readable: **[assets/theme/parrot-tokens.json](assets/theme/parrot-tokens.json)**.

---

## 🧠 Architettura

### Runtime bio-computazionale (Rust)

| Crate | Responsabilità |
|---|---|
| `organism-bin` | CLI, ciclo vitale, sensori di sistema, stato locale |
| `cortex` | decision engine, feedback omeostatico, evoluzione, bridge LLM |
| `zlang` | parser, AST e compiler verso bytecode |
| `zvm` | bytecode, opcode, stack e macchina virtuale con errori tipizzati |
| `core` | primitive condivise ed executor |
| `memzdos` | identità e stato persistente |

```text
SENSORS → NEURO SIGNALS → BIO FEEDBACK → FITNESS
        → MUTATION → OPTIMIZATION → CORTEX DECISION → STATE

source ZLang → Parser → AST → Compiler → BytecodeProgram → ZVM → JSON
```

Il feedback omeostatico dell'organismo (`programs/organism/tick.zlang`) è
eseguito dalla ZVM con ABI numerico, capability allowlist e fallback
deterministico in Rust — vedi [docs/ORGANISM_ZLANG.md](docs/ORGANISM_ZLANG.md).

### Layer ibrido (workstation)

| Componente | File |
|---|---|
| Launcher `zk` | `zdos_zk_launch.py` |
| Glass Engine (GUI) | `zdos_omni_os.py` |
| Widget desktop e dashboard | `z_kali_ui.py`, `z_kali_sovereign.py`, `zdos_master_dashboard.py` |
| Core UI glass | `interface/glass/core_ui.py` |
| Management Hub web | `webapp/` |
| Memoria e attestazioni | `src/neural/z_kali_cortex.py`, `zdos_bridge.py`, `var/evidence.jsonl` |
| Design system | `parrot_theme.py`, `assets/theme/` |
| Generator ambiente | `zdos-autobuild.sh`, `zdos-status.sh`, `zdos-evolution-deploy.sh` |

---

## ✅ Stato verificato

Distinguiamo sempre fra ciò che è **verificato eseguendo** e ciò che è
**dichiarato**. Ultima verifica: **2026-10-02**, branch
`feat/zdos-hybrid-security-20261001-230859`.

| Superficie | Stato | Prova |
|---|---|---|
| Identità visiva Parrot OS | **VERIFIED** | `tools/apply-parrot-theme.py --check` senza colori fuori palette |
| Interfaccia Glass Engine | **VERIFIED** | eseguita sotto Xvfb, anteprima in `docs/theme/preview/` |
| Launcher `zk` | **VERIFIED** | `python3 zdos_zk_launch.py --check` |
| Generatore ↔ artefatti | **VERIFIED** | `tools/sync-autobuild-heredocs.py --check` |
| Workspace Rust | **BLOCCATO** | `cargo test` non compila: vedi [docs/ANALISI-ZDOS-HYBRID.md](docs/ANALISI-ZDOS-HYBRID.md) |
| CI (format, Clippy, test) | **INATTIVA** | il workflow si attiva su push a `main`, che non esiste nel repository |
| Node Pulse / Microcosmo | **ASSENTE** | `zdos-microcosm-beta/` e `Zlang/` contengono 0 file tracciati |
| Endpoint LLM | **CONFIGURABILE** | `ZDOS_LLM_URL`; mock locale in `llm-mock.py` |

> **Nota di trasparenza.** Il workspace Rust **non compila** in questo branch:
> `cortex/src/policy.rs` chiama `runtime::execute` (rinominata
> `execute_with_vars`), mentre `core` e `organism-bin` non dichiarano alcune
> dipendenze usate (`zdos_zlang`, `tokio`). La diagnosi completa, con i comandi
> di riproduzione, è in **[docs/ANALISI-ZDOS-HYBRID.md](docs/ANALISI-ZDOS-HYBRID.md)**.

---

## 🛠️ Qualità e manutenzione

```bash
# runtime Rust
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test  --workspace --all-targets --all-features

# identità visiva e coerenza dei generatori
python3 tools/apply-parrot-theme.py --check
python3 tools/sync-autobuild-heredocs.py --check
python3 parrot_theme.py
```

| Strumento | Scopo |
|---|---|
| `tools/apply-parrot-theme.py` | converte e verifica la palette Parrot nei file UI (modalità `--check`) |
| `tools/sync-autobuild-heredocs.py` | mantiene allineati i file generati e i blocchi heredoc dell'autobuild |
| `parrot_theme.py` | design system: palette, tipografia, banner e token esportabili |

---

## 📁 Struttura del repository

```text
organism-bin/        → ciclo vitale e CLI
cortex/              → decision engine, feedback, evoluzione
zlang/ zvm/          → linguaggio interno e macchina virtuale
core/ memzdos/       → primitive condivise e stato persistente
programs/organism/   → programmi ZLang canonici
docs/                → wiki, deployment, identità visiva, analisi
assets/theme/        → token del design system
webapp/              → Management Hub (app.x-zdos.it)
parrot_theme.py      → design system condiviso
zdos_zk_launch.py    → launcher della workstation
zdos-autobuild.sh    → generatore dell'ambiente ibrido
```

---

## 🔐 Perimetro d'uso

Il progetto è un **laboratorio personale e difensivo**: strumenti, automazioni e
interfacce vanno usati su sistemi propri o con autorizzazione esplicita. Il
profilo ZLang applica *default-deny* su shell, rete e credenziali; il bridge
HTTP locale della GUI è pensato per la sola macchina di sviluppo. Vedi
[SECURITY.md](SECURITY.md).

---

## 📚 Documentazione

- **[Analisi tecnica del repository](docs/ANALISI-ZDOS-HYBRID.md)** — stato verificato, rischi e correzioni consigliate.
- **[Identità visiva Parrot OS](docs/theme/PARROT-OS-IDENTITY.md)** — palette, tipografia, applicazione.
- **[Overview tecnica](docs/OVERVIEW.md)** — contesto e contratto operativo.
- **[Architettura](docs/wiki/Architecture.md)** — confini dei crate e flusso dei segnali.
- **[Guida operativa](docs/wiki/Operations.md)** — installazione, CLI e troubleshooting.
- **[Deployment](docs/DEPLOYMENT.md)** — staging, systemd e rollback.
- **[Ecosystem Status](docs/ECOSYSTEM-STATUS.md)** — ruolo e stato nell'ecosistema ZDOS.
- **[Changelog](CHANGELOG.md)** — cronologia delle modifiche.

---

## 📝 Licenza

MIT License. «Parrot» e il logo Parrot Security sono marchi dei rispettivi
titolari: in questo progetto la palette è usata come riferimento estetico e non
implica alcuna affiliazione.

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:15E0ED,55:06043E,100:0A0118&height=130&section=footer)