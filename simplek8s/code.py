from kubernetes import client, config, watch


def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    w = watch.Watch()
    stream = w.stream(
        v1.list_namespaced_pod, namespace='default',
        label_selector="component=web"
    )
    for event in stream:
        event_obj = event.get('object')
        if event_obj.status.container_statuses:
            print(f"Containter ready: {event_obj.status.container_statuses[0].ready}")
        else:
            print("Container not ready")
        print(f"obj status phase: {event_obj.status.phase}")

        conds = event_obj.status.conditions or []
        condition_map = {
            x.type: x.status for x in conds
        }
        print(condition_map)
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
        if event_obj.status.conditions:
            for cond in event_obj.status.conditions:
                print(f"type: {cond.type}, status: {cond.status}")
        else:
            print("No cond yet")

        print("\n\n\n")
        # w.stop()
    return "Finished pod stream."


if __name__ == '__main__':
    x = main()
    print('x=', x)
