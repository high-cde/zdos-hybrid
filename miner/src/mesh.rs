use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

pub struct MeshNode {
    addr: String,
}

impl MeshNode {
    pub fn new(addr: &str) -> Self {
        Self { addr: addr.to_string() }
    }

    pub fn start_listener(&self) {
        let listener = TcpListener::bind(&self.addr).expect("[Mesh] Errore bind porta TCP");
        println!("[ZComm Mesh] Nodo in ascolto su {}...", self.addr);

        for stream in listener.incoming() {
            match stream {
                Ok(mut stream) => {
                    thread::spawn(move || {
                        let mut buffer = [0; 512];
                        if let Ok(n) = stream.read(&mut buffer) {
                            let msg = String::from_utf8_lossy(&buffer[..n]);
                            println!("[ZComm Mesh] Ricevuto pacchetto: {}", msg);
                            let response = "ZDOS_MESH_ACK_OK";
                            let _ = stream.write_all(response.as_bytes());
                        }
                    });
                }
                Err(e) => {
                    println!("[Mesh] Errore connessione in ingresso: {}", e);
                }
            }
        }
    }

    pub fn broadcast_block(peer_addr: &str, block_data: &str) -> Result<(), Box<dyn std::error::Error>> {
        let mut stream = TcpStream::connect(peer_addr)?;
        stream.write_all(block_data.as_bytes())?;
        let mut response = [0; 128];
        let n = stream.read(&mut response)?;
        println!("[ZComm Mesh] Broadcast ACK ricevuto: {}", String::from_utf8_lossy(&response[..n]));
        Ok(())
    }
}
