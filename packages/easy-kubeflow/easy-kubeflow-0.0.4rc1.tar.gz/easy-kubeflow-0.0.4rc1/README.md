# easy-kubeflow

python sdk for kubeflow platform

## docker

examples for use of docker

### initial

init docker client

Similar to cmd line ``docker login``

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

pull images from service.stonewise.cn:5000/ or harbor or harbor proxy (recommend)

Similar to cmd line ``docker pull xxx``

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
### push images

push images to service.stonewise.cn:5000/ or harbor (recommend)

Similar to cmd line ``docker push xxx``

```python
docker.push_images(repository="service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount", 
                   tag="0.0.3")

  0%|          | 0/793 [00:00<?, ?it/s]2022-03-23 06:52:54.661 [INFO] The push refers to repository [service.stonewise.cn:5000/notebook-server-manager/gpu-hot-mount]
  0%|          | 1/793 [00:00<01:20,  9.83it/s]2022-03-23 06:52:54.764 [INFO] Preparing
  0%|          | 2/793 [00:00<01:21,  9.76it/s]2022-03-23 06:52:54.867 [INFO] Waiting
  3%|▎         | 20/793 [00:00<00:09, 85.39it/s]2022-03-23 06:52:54.970 [INFO] Pushing
  4%|▍         | 31/793 [00:00<00:08, 94.05it/s]2022-03-23 06:52:55.072 [INFO] Pushed
2022-03-23 06:52:55.173 [INFO] Pushing
  5%|▌         | 41/793 [00:00<00:10, 70.32it/s]2022-03-23 06:52:55.276 [INFO] Pushed
2022-03-23 06:52:55.377 [INFO] Pushing
  6%|▌         | 49/793 [00:00<00:13, 56.90it/s]2022-03-23 06:52:55.480 [INFO] Pushed
  8%|▊         | 60/793 [00:00<00:10, 68.78it/s]2022-03-23 06:52:55.583 [INFO] Pushing
2022-03-23 06:52:55.684 [INFO] Pushed
2022-03-23 06:52:55.786 [INFO] Pushing
  9%|▊         | 68/793 [00:01<00:15, 47.38it/s]2022-03-23 06:52:55.889 [INFO] Pushed
 10%|█         | 80/793 [00:01<00:11, 60.79it/s]2022-03-23 06:52:55.993 [INFO] Pushing
2022-03-23 06:52:56.095 [INFO] Pushed
2022-03-23 06:52:56.196 [INFO] Pushing
 11%|█         | 88/793 [00:01<00:15, 45.07it/s]2022-03-23 06:52:56.300 [INFO] Pushed
 50%|████▉     | 393/793 [00:01<00:00, 564.44it/s]2022-03-23 06:52:56.403 [INFO] Pushing
2022-03-23 06:52:56.504 [INFO] Pushed
2022-03-23 06:52:56.605 [INFO] Pushing
2022-03-23 06:52:56.707 [INFO] Pushed
2022-03-23 06:52:56.809 [INFO] Pushing
2022-03-23 06:52:56.910 [INFO] Pushed
2022-03-23 06:52:57.012 [INFO] Pushing
 62%|██████▏   | 488/793 [00:02<00:01, 289.57it/s]2022-03-23 06:52:57.115 [INFO] Pushed
2022-03-23 06:52:57.216 [INFO] Pushing
 70%|███████   | 558/793 [00:02<00:00, 300.54it/s]2022-03-23 06:52:57.320 [INFO] Pushed
 80%|███████▉  | 632/793 [00:02<00:00, 354.68it/s]2022-03-23 06:52:57.423 [INFO] Pushing
 88%|████████▊ | 695/793 [00:02<00:00, 394.87it/s]2022-03-23 06:52:57.526 [INFO] Pushed
2022-03-23 06:52:57.627 [INFO] Pushing
 96%|█████████▌| 758/793 [00:03<00:00, 368.36it/s]2022-03-23 06:52:57.730 [INFO] Pushed
2022-03-23 06:52:57.831 [INFO] 0.0.3: digest: sha256:189270b1726e6764ebbcdfa72f1ba80fa8bc3945712afadc1adadfd3dfb741b4 size: 4079
2022-03-23 06:52:57.933 [INFO] {}
100%|██████████| 793/793 [00:03<00:00, 235.06it/s]
2022-03-23 06:52:58.036 [INFO] Push image successfully !
```

### build images

build images for harbor or service.stonewise.cn:5000/

Similar to cmd line ``docker build -f Dockerfile -t xxx ./``

```python
docker.build_images(path="/home/jovyan/image",
                    dockerfile="Dockerfile",
                    repository="service.stonewise.cn:5000/standalone-training",tag="0.0.1")

  0%|          | 0/14 [00:00<?, ?it/s]2022-03-23 07:35:22.763 [INFO] Step 1/3 : FROM harbor-qzm.stonewise.cn/proxy_cache/kubeflow/tensorflow:1.14.0-py3.6-cpu
  7%|▋         | 1/14 [00:00<00:01,  9.88it/s]2022-03-23 07:35:22.866 [INFO] 
 14%|█▍        | 2/14 [00:00<00:01,  9.75it/s]2022-03-23 07:35:22.970 [INFO]  ---> 3519b2e83423
 21%|██▏       | 3/14 [00:00<00:01,  9.73it/s]2022-03-23 07:35:23.073 [INFO] Step 2/3 : ADD main.py .
 29%|██▊       | 4/14 [00:00<00:01,  9.71it/s]2022-03-23 07:35:23.176 [INFO] 
 36%|███▌      | 5/14 [00:00<00:00,  9.71it/s]2022-03-23 07:35:23.279 [INFO]  ---> 755d86598819
 43%|████▎     | 6/14 [00:00<00:00,  9.71it/s]2022-03-23 07:35:23.382 [INFO] Step 3/3 : ENTRYPOINT ["python3", "main.py"]
 50%|█████     | 7/14 [00:00<00:00,  9.70it/s]2022-03-23 07:35:23.485 [INFO] 
 57%|█████▋    | 8/14 [00:00<00:00,  9.71it/s]2022-03-23 07:35:23.588 [INFO]  ---> Running in 0438ef9bc950
 64%|██████▍   | 9/14 [00:00<00:00,  9.71it/s]2022-03-23 07:35:23.691 [INFO] Removing intermediate container 0438ef9bc950
 71%|███████▏  | 10/14 [00:01<00:00,  9.71it/s]2022-03-23 07:35:23.794 [INFO]  ---> 9a41289aed98
 79%|███████▊  | 11/14 [00:01<00:00,  9.70it/s]2022-03-23 07:35:23.897 [INFO] {'ID': 'sha256:9a41289aed98e3e715fd91a21625c621dd697e49d632e2e06d3564bfc77c5e88'}
 86%|████████▌ | 12/14 [00:01<00:00,  9.70it/s]2022-03-23 07:35:24.000 [INFO] Successfully built 9a41289aed98
 93%|█████████▎| 13/14 [00:01<00:00,  9.70it/s]2022-03-23 07:35:24.103 [INFO] Successfully tagged service.stonewise.cn:5000/standalone-training:0.0.1
100%|██████████| 14/14 [00:01<00:00,  9.70it/s]
2022-03-23 07:35:24.208 [INFO] Build image successfully !

docker.push_images(repository="service.stonewise.cn:5000/standalone-training", tag="0.0.1")

  0%|          | 0/525 [00:00<?, ?it/s]2022-03-23 07:37:37.084 [INFO] The push refers to repository [service.stonewise.cn:5000/standalone-training]
  0%|          | 1/525 [00:00<00:53,  9.88it/s]2022-03-23 07:37:37.186 [INFO] Preparing
  0%|          | 2/525 [00:00<00:53,  9.81it/s]2022-03-23 07:37:37.289 [INFO] Waiting
  2%|▏         | 11/525 [00:00<00:11, 45.49it/s]2022-03-23 07:37:37.392 [INFO] Pushing
  3%|▎         | 16/525 [00:00<00:10, 46.73it/s]2022-03-23 07:37:37.495 [INFO] Mounted from notebook-server-manager/gpu-hot-mount
2022-03-23 07:37:37.596 [INFO] Pushing
2022-03-23 07:37:37.698 [INFO] Pushed
  4%|▍         | 21/525 [00:00<00:18, 27.66it/s]2022-03-23 07:37:37.800 [INFO] Pushing
2022-03-23 07:37:37.902 [INFO] Mounted from notebook-server-manager/gpu-hot-mount
  5%|▍         | 25/525 [00:00<00:20, 24.64it/s]2022-03-23 07:37:38.005 [INFO] Pushing
2022-03-23 07:37:38.106 [INFO] Mounted from notebook-server-manager/gpu-hot-mount
2022-03-23 07:37:38.207 [INFO] Pushing
  6%|▌         | 29/525 [00:01<00:25, 19.51it/s]2022-03-23 07:37:38.310 [INFO] Mounted from notebook-server-manager/gpu-hot-mount
2022-03-23 07:37:38.412 [INFO] Pushing
  6%|▌         | 32/525 [00:01<00:27, 18.07it/s]2022-03-23 07:37:38.516 [INFO] Pushed
100%|█████████▉| 523/525 [00:01<00:00, 854.64it/s]2022-03-23 07:37:38.620 [INFO] 0.0.1: digest: sha256:0fe6eaa12c2e4409f2b20f089dca83e8f0b4480b60405dcbb102a00185b2070c size: 2215
2022-03-23 07:37:38.721 [INFO] {}
100%|██████████| 525/525 [00:01<00:00, 301.85it/s]
2022-03-23 07:37:38.825 [INFO] Push image successfully !
```