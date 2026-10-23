use sha2::{Sha256, Digest};
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Transaction {
    pub sender: String,
    pub recipient: String,
    pub amount: u64,
    pub nonce: u64,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Block {
    pub index: u64,
    pub previous_hash: String,
    pub timestamp: u64,
    pub transactions: Vec<Transaction>,
    pub nonce: u64,
    pub hash: String,
    pub state_root: String,
}

impl Block {
    pub fn calculate_hash(index: u64, previous_hash: &str, timestamp: u64, txs: &[Transaction], nonce: u64) -> String {
        // Usiamo {:?} per tutti i campi non primitivi o composti
        let data = format!("{:?}{:?}{:?}{:?}{:?}", index, previous_hash, timestamp, txs, nonce);
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        format!("{:x}", hasher.finalize())
    }
}
