# easy-kubeflow

python sdk for kubeflow platform

## docker

examples for use of docker

### initial

init docker client
```python
from easy_kubeflow import EasyDocker
docker = EasyDocker()

2022-03-22 01:39:02.933 [INFO] Connected to host docker successfully !
```
### show images

show images in container's host node.

Similar to cmd line ``docker images | grep xxx``. when name none, show all images

```python
docker.show_images(grep="liuweibin")

REPOSITORY + TAG	IMAGE ID	CREATED	SIZE
harbor.stonewise.cn/kubeflow/liuweibin/notebook-image:base	f621486595fe	2022-03-17T02:02:18.143	8.1 GB
harbor.stonewise.cn/kubeflow/liuweibin/notebook-image:test	8491b7b97d72	2022-01-21T10:13:34.857	8.1 GB
```

### pull images

pull images from harbor or harbor proxy (recommend)

```python
docker.pull_images(repository="harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount", 
                   tag="0.0.3")

  0%|          | 0/3 [00:00<?, ?it/s]2022-03-22 01:53:12.543 [INFO] Pulling from proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount
 33%|███▎      | 1/3 [00:00<00:00,  9.84it/s]2022-03-22 01:53:12.646 [INFO] Digest: sha256:189270b1726e6764ebbcdfa72f1ba80fa8bc3945712afadc1adadfd3dfb741b4
 67%|██████▋   | 2/3 [00:00<00:00,  9.75it/s]2022-03-22 01:53:12.749 [INFO] Status: Downloaded newer image for harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount:0.0.3
100%|██████████| 3/3 [00:00<00:00,  9.69it/s]
2022-03-22 01:53:12.854 [INFO] Pull image successfully !
```

### tag images

tag images in container's host node.

```python
docker.tag_images(original_repository="harbor-qzm.stonewise.cn/proxy_cache/kubeflow/notebook-server-manager/gpu-hot-mount", 
                  original_tag="0.0.3",
                  target_repository="service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount", 
                  target_tag="0.0.3"
                 )

2022-03-22 02:03:55.017 [INFO] Tag repository successfully !

docker.show_images(grep="service.stonewise.cn")

REPOSITORY + TAG	IMAGE ID	CREATED	SIZE
service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount:0.0.3	d3838c66fc1e	2022-03-14T02:19:02.010	1.0 GB
```

