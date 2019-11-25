from kubernetes import client, config

DEPLOYMENT_NAME = "nginx-deployment"


def create_deployment_object():
    # Configureate Pod template container
    container = client.V1Container(
        name="nginx",
        image="nginx:1.15.4",
        ports=[client.V1ContainerPort(container_port=80)])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=3,
        template=template,
        selector={'matchLabels': {'app': 'nginx'}})
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))


def main():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    deployment = create_deployment_object()

    create_deployment(apps_v1, deployment)


if __name__ == '__main__':
    main()
