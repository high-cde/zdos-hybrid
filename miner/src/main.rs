mod ledger;
mod mesh;

use ledger::{Block, Transaction};
use mesh::MeshNode;
use std::time::{SystemTime, UNIX_EPOCH};
use std::thread;
use std::time::Duration;

fn main() {
    println!("==================================================");
    println!("   ZDOS SOVEREIGN HYBRID MINER & MESH NET v2.1");
    println!("==================================================");

    // Avviamo il listener di rete mesh in un thread separato
    thread::spawn(|| {
        let node = MeshNode::new("127.0.0.1:8333");
        node.start_listener();
    });

    // Simuliamo una transazione .zbag
    let tx = Transaction {
        sender: "zdos_wallet_highkali_13".to_string(),
        recipient: "zdos_validator_node_01".to_string(),
        amount: 5000,
        nonce: 1,
    };

    let index = 1;
    let previous_hash = "0000000000000000000000000000000000000000000000000000000000000000".to_string();
    let timestamp = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs();
    let txs = vec![tx];
    
    let target_difficulty = "0000";
    let mut nonce: u64 = 0;

    println!("[*] Avvio Proof-of-Work per il Blocco #{} con sincronizzazione Mesh...", index);

    loop {
        let hash = Block::calculate_hash(index, &previous_hash, timestamp, &txs, nonce);
        if hash.starts_with(target_difficulty) {
            let block = Block {
                index,
                previous_hash,
                timestamp,
                transactions: txs,
                nonce,
                hash: hash.clone(),
                state_root: "0x0100_vram_state_trie_root".to_string(),
            };

            println!("\n[+] BLOCCO #{} MINATO E VALIDATO CON SUCCESSO! 🎉", block.index);
            println!("    Hash:       {}", block.hash);
            println!("    Nonce:      {}", block.nonce);
            println!("    State Root: {}", block.state_root);

            // Simuliamo il broadcast sulla rete Mesh verso un peer locale
            thread::sleep(Duration::from_millis(200));
            let payload = format!("BLOCK_BROADCAST:{}", block.hash);
            if let Err(_) = MeshNode::broadcast_block("127.0.0.1:8333", &payload) {
                println!("[ZComm Mesh] Nessun altro nodo attivo sulla porta 8333 (modalità standalone attiva).");
            }
            break;
        }
        nonce += 1;
    }
}
