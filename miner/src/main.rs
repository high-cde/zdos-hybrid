mod ledger;

use ledger::{Block, Transaction};
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    println!("==================================================");
    println!("   ZDOS SOVEREIGN HYBRID MINER & LEDGER v2");
    println!("==================================================");

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

    println!("[*] Avvio Proof-of-Work per il Blocco #{} con transazione .zbag...", index);

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

            println!("\n[+] BLOCCO #{} VALIDATO E MINATO CON SUCCESSO! 🎉", block.index);
            println!("    Hash:       {}", block.hash);
            println!("    Nonce:      {}", block.nonce);
            println!("    Transazioni incluse: {}", block.transactions.len());
            println!("    State Root: {}", block.state_root);
            break;
        }
        nonce += 1;
    }
}
