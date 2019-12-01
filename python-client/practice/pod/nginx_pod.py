from kubernetes import client, config


def create_pod_objects():
    api_version = 'v1'
    kind = 'Pod'
    metadata = client.V1ObjectMeta(
        name='nginx-pod',
        labels={
            'app': 'nginx',
            'tier': 'dev',
        },
    )
    spec = client.V1PodSpec(
        containers=[
            client.V1Container(
                name='nginx',
                image='nginx',
            ),
        ],
    )
    pod_object = client.V1Pod(
        api_version=api_version,
        kind=kind,
        metadata=metadata,
        spec=spec,
    )
    return pod_object


def create_pod(api_instance, body):
    namespace = 'default'
    api_instance.create_namespaced_pod(
        namespace,
        body,
    )
    print("\nDONE\n")


def main():
    config.load_kube_config()
    apps_v1 = client.CoreV1Api()
    pod_object = create_pod_objects()
    create_pod(apps_v1, pod_object)


main()
