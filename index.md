Simulation testing has been widely adopted by leading companies to ensure the safety of autonomous driving systems (ADSs). A number of scenario-based testing approaches have been developed to generate diverse driving scenarios for simulation testing, and demonstrated to be capable of finding safety violations. However, there is no automated way to diagnose whether these violations are caused by the ADS under test and which category these violations belong to. As a result, great effort is required to manually diagnose violations.

To bridge this gap, we propose DiaVio to automatically diagnose safety violations in simulation testing by leveraging large language models (LLMs). It is built on top of a new domain specific language (DSL) of crash to align real-world accident reports described in natural language and violation scenarios in simulation testing. DiaVio fine-tunes a base LLM with real-world accident reports to learn diagnosis capability, and uses the fine-tuned LLM to diagnose violation scenarios in simulation testing. Our evaluation has demonstrated the effectiveness and efficiency of DiaVio in violation diagnosis.

The paper has been submitted to ISSTA 2024.

## Overview

![](/img/overview.png)

## The Syntax of Crash DSL

We propose a DSL to describe crashes. The DSL serves as an intermediate representation to align crashes in accident reports in natural language and crashes in violation scenarios in simulation testing. The syntax of our proposed Crash DSL is illustrated as follows.

![](/img/DSL.pdf)

## Accident Reports --- Violation Reports --- Model Output

Here we will introduce the format of the accident reports, the style of the violation reports and the results of the model diagnosis.

### Accident Reports

### Violation Reports

Based on the above accident report, we convert its format according to the syntax of the DSL (aligned with the violation report generated during the simulation testing).

### Model Output

The output of our fine-tuned model diagnosis of the above report are shown below.

## Samples

By running DiaVio with AV-Fuzzer and DriveFuzz, we diagnose cases caused by NPC Vehicles and Ego Vehicle respectively. Here are some examples of our findings.



## The prototype of DiaVio and documents are available [here](https://github.com/DiaVio/diavio).

## The LoRA models and datasets are available [here](https://huggingface.co/DiaVio).