from kubernetes import client, config


def create_pod_object():
    container = client.V1Container(
        name="client",
        image="rishikant42/multi-client",
        ports=[
            client.V1ContainerPort(container_port=3000)
        ]
    )
    spec = client.V1PodSpec(
        containers=[container]
    )
    pod = client.V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=client.V1ObjectMeta(
            name="client-pod",
            labels={
                "component": "web"
            }
        ),
        spec=spec
    )
    return pod


def create_pod(api_instance, pod):
    api_response = api_instance.create_namespaced_pod(
        namespace="default",
        body=pod
    )
    print("Pod create. Status='%s'" % str(api_response.status))


def main():
    config.load_kube_config()
    apps_v1 = client.CoreV1Api()

    pod = create_pod_object()

    create_pod(apps_v1, pod)


if __name__ == '__main__':
    main()
