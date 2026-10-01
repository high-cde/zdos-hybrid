#!/usr/bin/env bash
set -e

echo "======================================================="
echo " ZDOS // EVOLUTION DEPLOYMENT & ZLANG IDE PIPELINE     "
echo "======================================================="

# 1. Installazione prerequisiti corretti per Ubuntu/Debian
echo "[*] Controllo e installazione requisiti di sistema..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y \
        build-essential \
        curl \
        git \
        make \
        gcc \
        cpio \
        gzip \
        coreutils \
        xorriso \
        grub-common \
        grub-pc-bin \
        mtools \
        qemu-system-x86 \
        qemu-utils \
        e2fsprogs \
        python3 \
        python3-pip \
        pkg-config \
        libssl-dev
else
    echo "[!] Gestore pacchetti APT non rilevato."
fi

# 2. Configurazione percorsi e workspace
ZDOS_ROOT="$HOME/zdos-organism"
ZLANG_ROOT="$ZDOS_ROOT/Zlang"
mkdir -p "$ZDOS_ROOT"
cd "$ZDOS_ROOT"

echo "[*] Workspace principale: $ZDOS_ROOT"

# 3. Sincronizzazione Zlang
if [ ! -d "$ZLANG_ROOT" ]; then
    echo "[*] Clonazione Zlang da GitHub..."
    git clone https://github.com/high-cde/Zlang.git "$ZLANG_ROOT"
else
    echo "[*] Aggiornamento repository Zlang esistente..."
    cd "$ZLANG_ROOT" && git pull origin main || true
    cd "$ZDOS_ROOT"
fi

# 4. Compilazione Zlang & ZLB2
echo "[*] Compilazione del compilatore Zlang e del runtime ZLB2..."
if [ -f "$ZLANG_ROOT/Cargo.toml" ]; then
    cd "$ZLANG_ROOT"
    cargo build --release
    cd "$ZDOS_ROOT"
fi

# 5. Pipeline Evidence Chain
EVIDENCE_SCRIPT="$ZDOS_ROOT/scripts/evolve-zlang-evidence.sh"
if [ -f "$EVIDENCE_SCRIPT" ]; then
    ZLANG_ROOT="$ZLANG_ROOT" bash "$EVIDENCE_SCRIPT" || true
fi

echo "======================================================="
echo " [SUCCESSO] ZDOS EVOLUTION PIPELINE COMPLETATA!        "
echo "======================================================="
