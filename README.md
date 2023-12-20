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
    - Python3

## Installation & Run
