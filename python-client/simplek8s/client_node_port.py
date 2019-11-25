from kubernetes import client, config


def create_node_port_object():
    metadata = client.V1ObjectMeta(
        name="client-node-port"
    )
    spec = client.V1ServiceSpec(
        type="NodePort",
        ports=[
            client.V1ServicePort(
                port=3050,
                target_port=3000,
                node_port=31515,
            )
        ],
        selector={
            "component": "web"
        }
    )
    node_port = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=metadata,
        spec=spec,
    )
    return node_port


def create_node_port(api_instance, node_port):
    api_response = api_instance.create_namespaced_service(
        namespace="default",
        body=node_port,
    )

    print("Service created. Status='%s'" % str(api_response.status))


def main():
    config.load_kube_config()
    apps_v1 = client.CoreV1Api()

    node_port = create_node_port_object()

    create_node_port(apps_v1, node_port)


if __name__ == '__main__':
    main()
