from kubernetes import client, config

def create_deployment_object():
    api_version = 'apps/v1'
    kind = 'Deployment'
    metadata = client.V1ObjectMeta(
        name='nginx-deployment',
    )
    spec = client.V1DeploymentSpec(
        replicas=2,
        selector=client.V1LabelSelector(
            match_expressions=[
                client.V1LabelSelectorRequirement(
                    key='tier',
                    operator='In',
                    values=['frontend']
                ),
            ],
            match_labels={
                'app': 'nginx-app',
            }
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={
                    'app': 'nginx-app',
                    'tier': 'frontend',
                }
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name='nginx-container',
                        image='nginx',
                        ports=[
                            client.V1ContainerPort(
                                container_port=80
                            )
                        ]
                    ),
                ],
            )
        )
    )
    deployment_object = client.V1Deployment(
        api_version=api_version,
        kind=kind,
        metadata=metadata,
        spec=spec,
    )
    return deployment_object


def create_deployment(api_instance, body):
    namespace = 'default'

    api_instance.create_namespaced_deployment(
        namespace,
        body,
    )
    print("\nDONE\n")


def main():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    deployment_objects = create_deployment_object()
    create_deployment(apps_v1, deployment_objects)

main()
