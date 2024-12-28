fn main() {
    tonic_build::configure()
        .build_client(false)
        .build_server(true)
        .compile_protos(&["../proto/api.proto"], &["../proto/"])
        .unwrap_or_else(|e| {
            panic!("Error compining .proto: {e}");
        });
}
