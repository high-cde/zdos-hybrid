# Changelog ZDOS Hybrid

Tutte le modifiche rilevanti del progetto sono registrate in questo documento. Le versioni seguono una convenzione semantica finché il runtime resta in fase di consolidamento.

## [Unreleased]

### Identità visiva Parrot OS «Echo»

- sostituita la palette Kali-teal con l'identità Parrot OS 7 su GUI, webapp,
  dashboard, widget e launcher;
- introdotto il design system condiviso `parrot_theme.py` con token in
  `assets/theme/parrot-tokens.json` e documentazione in
  `docs/theme/PARROT-OS-IDENTITY.md`;
- aggiunti `tools/apply-parrot-theme.py` (conversione tracciata e `--check`) e
  `tools/sync-autobuild-heredocs.py` (allineamento generatore/artefatti);
- launcher `zk`: banner Parrot, risoluzione della radice senza percorsi
  assoluti, flag `--check` e `--no-node`;
- `zdos-autobuild.sh`: heredoc finale terminato e generazione di
  `parrot_theme.py`.

### Documentazione

- `README.md` riscritto con identità `zdos-hybrid`, istruzioni di avvio del
  layer ibrido e stato verificabile;
- aggiunto `docs/ANALISI-ZDOS-HYBRID.md` con la diagnosi della build, il
  perimetro della CI e i rilievi di igiene del repository.

Questa sezione raccoglie il lavoro successivo alla prima release foundation: telemetria strutturata, configurazione del servizio systemd, test di integrazione del cortex e documentazione del runtime ZLang.

### Forgiatura Organism in ZLang

- aggiunto il programma canonico `programs/organism/tick.zlang`;
- collegato il feedback Rust al file ZLang versionato tramite `include_str!`;
- documentati ABI numerico, capability allowlist e fallback local-only in `docs/ORGANISM_ZLANG.md`;
- riallineato lo stato ecosistema alla struttura ZDOS/Zlang/Organism senza riferimenti a componenti esterni rimossi.

## [0.1.0-foundation] — 2026-08-25

La prima release foundation rende il workspace Rust riproducibile e introduce un percorso end-to-end verificato tra ZLang, compiler e ZVM. La CLI supporta `--help`, `--version`, `--eval` e `--once`; il loop dell’organismo usa `ZDOS_LLM_URL` e `ZDOS_STATE_DIR` invece di percorsi hard-coded.

La macchina virtuale ora segnala in modo tipizzato stack underflow, divisione per zero, programma senza risultato e superamento del limite di istruzioni. Sono stati aggiunti test unitari per stack, aritmetica, runtime ZLang e gestione degli errori.

Il repository include `rust-toolchain.toml`, workflow CI per format, Clippy, test e smoke test CLI, oltre a regole `.gitignore` per escludere artefatti di build e stato locale.

## Riferimenti

- [README](README.md)
- [Overview tecnica](docs/OVERVIEW.md)
- [Roadmap](docs/wiki/Roadmap.md)
- [Security policy](SECURITY.md)
