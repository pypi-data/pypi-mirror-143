//! Integration tests

#[cfg(test)]
mod integ_tests {
    mod client_tests;
    mod heartbeat_tests;
    mod polling_tests;
    mod queries_tests;
    mod workflow_tests;

    use std::str::FromStr;
    use temporal_client::WorkflowService;
    use temporal_sdk_core::{
        init_worker_from_upgradeable_client, telemetry_init, ClientTlsConfig, ServerGatewayApis,
        ServerGatewayOptionsBuilder, TlsConfig,
    };
    use temporal_sdk_core_api::{worker::WorkerConfigBuilder, CoreTelemetry};
    use temporal_sdk_core_protos::temporal::api::workflowservice::v1::ListNamespacesRequest;
    use temporal_sdk_core_test_utils::{
        get_integ_server_options, get_integ_telem_options, NAMESPACE,
    };
    use url::Url;

    // Create a worker like a bridge would (unwraps aside)
    #[tokio::test]
    #[ignore] // Really a compile time check more than anything
    async fn lang_bridge_example() {
        let opts = get_integ_server_options();
        let telem_d = telemetry_init(&get_integ_telem_options()).unwrap();
        let mut retrying_client = opts
            .connect_no_namespace(telem_d.get_metric_meter())
            .await
            .unwrap();

        let _worker = init_worker_from_upgradeable_client(
            WorkerConfigBuilder::default()
                .namespace("default")
                .task_queue("Wheee!")
                .build()
                .unwrap(),
            // clone the client if you intend to use it later. Strip off the retry wrapper since
            // worker will assert its own
            retrying_client.clone().into_inner(),
        );

        // Do things with worker or client
        let _ = retrying_client
            .list_namespaces(ListNamespacesRequest::default())
            .await;
    }

    // TODO: Currently ignored because starting up the docker image with TLS requires some hoop
    //  jumping. We should upgrade CI to be able to do that but this was manually run against
    //  https://github.com/temporalio/customization-samples/tree/master/tls/tls-simple
    #[tokio::test]
    #[ignore]
    async fn tls_test() {
        // Load certs/keys
        let root = tokio::fs::read(
            "/home/sushi/dev/temporal/customization-samples/tls/tls-simple/certs/ca.cert",
        )
        .await
        .unwrap();
        let client_cert = tokio::fs::read(
            "/home/sushi/dev/temporal/customization-samples/tls/tls-simple/certs/client.pem",
        )
        .await
        .unwrap();
        let client_private_key = tokio::fs::read(
            "/home/sushi/dev/temporal/customization-samples/tls/tls-simple/certs/client.key",
        )
        .await
        .unwrap();
        let sgo = ServerGatewayOptionsBuilder::default()
            .target_url(Url::from_str("https://localhost:7233").unwrap())
            .worker_binary_id("binident".to_string())
            .tls_cfg(TlsConfig {
                server_root_ca_cert: Some(root),
                domain: Some("tls-sample".to_string()),
                client_tls_config: Some(ClientTlsConfig {
                    client_cert,
                    client_private_key,
                }),
            })
            .build()
            .unwrap();
        let con = sgo.connect(NAMESPACE.to_string(), None).await.unwrap();
        con.list_namespaces().await.unwrap();
    }
}
