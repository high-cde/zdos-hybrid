use serde_json::json;
use zdos_core::zvm_executor::exec_zlang_in_core;
use zdos_cortex::bytecode_mutator::mutate_bytecode;
use zdos_zlang::{parser::Parser, compiler::compile};
use zdos_zvm::vm::ZVM;

#[tokio::main]
async fn main() {
    println!("[ZDOS] organism boot");

    let src = "let x = 10 let y = x + 32";

    let core_exec = exec_zlang_in_core(src);
    println!("[CORE][EXEC] {core_exec}");

    let mut parser = Parser::new(src);
    let program = parser.parse().unwrap();
    let mut bytecode = compile(&program);

    mutate_bytecode(&mut bytecode);

    let mut vm = ZVM::new();
    let mutated = vm.run(&bytecode);

    println!("[CORTEX][MUTATED BYTECODE RESULT] {mutated}");
}
