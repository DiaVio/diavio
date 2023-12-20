# DiaVio
Simulation testing has been widely adopted by leading companies to ensure the safety of autonomous driving systems (ADSs). A number of scenario-based testing approaches have been developed to generate diverse driving scenarios for simulation testing, and demonstrated to be capable of finding safety violations. However, there is no automated way to diagnose whether these violations are caused by the ADS under test and which category these violations belong to. As a result, great effort is required to manually diagnose violations.

To bridge this gap, we propose DiaVio to automatically diagnose safety violations in simulation testing by leveraging large language models (LLMs). It is built on top of a new domain specific language (DSL) of crash to align real-world accident reports described in natural language and violation scenarios in simulation testing. DiaVio fine-tunes a base LLM with real-world accident reports to learn diagnosis capability, and uses the fine-tuned LLM to diagnose violation scenarios in simulation testing. Our evaluation has demonstrated the effectiveness and efficiency of DiaVio in violation diagnosis.

We bridge DiaVio with two state-of-the-art open source scenario-based testing approaches, i.e., AV-Fuzzer and DriveFuzz. Specifically, we set up AV-Fuzzer with the Apollo 8.0 ADS and the SORA-SVL simulator, and set up DriveFuzz with the Behavior Agent ADS and the Carla simulator.
## Experiment Environment

### The following environment was used to fine-tune and use the LoRA models（recommended）:

- Hardware
    - CPU: Intel Core 8358P CPU
    - GPU: 8 NVIDIA A800 GPUs
    - RAM: 1TB
- OS & SW
    - Ubuntu 20.04.6 
    - Python 3.10.13
    - You can use and fine-tune the models through [text-generation-webui](https://github.com/oobabooga/text-generation-webui).

### The following environment was used to generate violation reports (described in DSL) in simulation testing:

- Hardware
    - CPU: Intel Core i9-12900K CPU
    - GPU: 1 NVIDIA GeForce RTX 3090 GPU
    - RAM:  64GB
- OS & SW
    - Ubuntu 18.04.6 (strictly required)
    - Python3.6

## Installation & Run
### Setting up docker and nvidia driver

1. Install `docker-ce`
* Remove existing installation, add GPG key, and install `docker-ce`
```sh
$ sudo apt remove docker docker-engine docker.io
$ sudo apt update
$ sudo apt install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo apt-key fingerprint 0EBFCD88
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
$ sudo apt update
$ sudo apt install docker-ce
```

* Check installation. The following should print a message starting with
  "Hello from Docker!"
```sh
$ sudo docker run hello-world
```

2. Set up permissions
* Create group `docker` and add yourself to it
```sh
$ sudo groupadd docker
$ sudo usermod -aG docker ${USER}
```

* Log out and log back in
```sh
$ sudo su - ${USER}
```

* Try running docker without root permission this time
```sh
$ docker run hello-world
```

3. Make sure you have nvidia driver on Host
* Search for available drivers
```sh
$ sudo add-apt-repository ppa:graphics-drivers
$ sudo apt update
$ ubuntu-drivers devices
```

* Install one of the compatible drivers. `nvidia-driver-415` worked for me.
```sh
$ sudo apt install nvidia-driver-415
$ sudo reboot now
$ nvidia-smi
```

4. Install `nvidia-docker2`
* Install
```sh
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
$ curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
$ curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

$ sudo apt update
$ sudo apt install nvidia-docker2
$ sudo systemctl restart docker
```

* Test the installation
```sh
$ docker run --runtime=nvidia --rm nvidia/cuda:10.0-base nvidia-smi
```
### AV-Fuzzer
#### 1. install LGSVL
LGSVL simulator can be installed from https://github.com/lgsvl/simulator .We are using the latest version,2021.3.\
LGSVL has made the difficult decision to suspend active development of SVL Simulator, as of January 1, 2022. The cloud had stopped running on June 30, 2022.Therefore, we use SORA-SVL to build our own server as a replacement.SORA-SVL can be installed from https://github.com/YuqiHuai/SORA-SVL
#### 2. install Apollo8.0
clone source code
```sh
$ git clone https://github.com/ApolloAuto/apollo.git
```
pull docker image and enter the container(This step may take a long time)
```sh
$ sudo bash ./docker/scripts/dev_start.sh
$ sudo bash ./docker/scripts/dev_into.sh
```
build Apollo
```sh
sudo ./apollo.sh build
```
start dreamviewer
```sh
sudo bash scripts/bootstrap.sh
```
After completion, open localhost:8888 and you can see the Dreamviewer Interface.\
bridge Apollo with LGSVL
```sh
bash scripts/bridge.sh
``` 
#### 3. run AV-Fuzzer-diavio
Install necessary Python packages using pip
```sh
pip3 install -r requirements.txt
```
edit config/\_\_init__.py,modify SIMULATOR_HOST,SIMULATOR_PORT,BRIDGE_HOST and BRIDGE_PORT(If both Apollo and LGSVL are installed locally, no modifications are required) 
\
\
start AV-Fuzzer-diavio
```sh
python3 drive_experiment.py
``` 

### drivefuzz-diavio
#### 1. Install Carla 0.9.10.1 docker
Choose either of the two methods to install Carla.
* Pull docker image
```sh
$ docker pull carlasim/carla:0.9.10.1
```

* Quick-running Carla
Carla can be run using a wrapper script `run_carla.sh`.

To run carla simulator, execute the script:
```sh
$ ./run_carla.sh
```
It will run carla simulator container, and name it carla-${USER} .

To stop the container, do:
```sh
$ docker rm -f carla-${USER}
```

#### 2. Install Carla 0.9.10.1 Releases
```sh
wget https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.10.1.tar.gz
mkdir carla_0.9.10.1
tar -zxvf CARLA_0.9.10.1.tar.gz -C ./carla_0.9.10.1/
```
run Carla
```sh
cd carla_0.9.10.1
./CarlaUE4.sh -quality-level=Low -windowed -ResX=640 -ResY=480
```

#### 3. run drivefuzz-diavio
Initialize the runtime environment
```sh
sudo ./init.sh
```
Before running drivefuzz-diavio each time, it is necessary to delete or move the output file from the last run
```sh
rm -rf out-artifact
```
start drivefuzz-diavio
```sh
./fuzzer.py -o out-artifact -s seed-artifact -c 5 -m 5 -t behavior --timeout 60 --town 1 --strategy all
```