#!/bin/bash
echo "[*] Preparazione immagine disco avviabile ZDOS..."
dd if=/dev/zero of=zdos_boot.img bs=1M count=64
mkfs.ext4 zdos_boot.img

# Montaggio temporaneo per popolare il filesystem radice con i binari compilati
mkdir -p /mnt/zdos_root
mount -o loop zdos_boot.img /mnt/zdos_root

mkdir -p /mnt/zdos_root/sbin /mnt/zdos_root/etc /mnt/zdos_root/root
cp -r target/release/* /mnt/zdos_root/root/

# Creazione di un init minimale per l'avvio del sistema operativo
cat << 'INIT' > /mnt/zdos_root/init
#!/bin/sh
echo "=================================================="
echo "      ZDOS // REAL OPERATING SYSTEM BOOTED       "
echo "      Cortex Engine & ZLang Runtime Active        "
echo "=================================================="
export PATH=/root
exec /bin/sh
INIT
chmod +x /mnt/zdos_root/init

umount /mnt/zdos_root
echo "[*] Immagine disco ZDOS pronta."
