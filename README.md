<div align="center">

# Aman Singh

### ML Systems Engineer · LLM Training, Serving & AI Infrastructure

I build LLM systems from training and inference to secure, reliable deployment.

[Portfolio](https://aman-ai-portfolio.netlify.app) · [Résumé](https://asinghresume.netlify.app) · [LinkedIn](https://www.linkedin.com/in/amanyagami) · [Email](mailto:2amansingh2@gmail.com)

</div>

## Currently

**Founding Engineer at Noah Labs**, building Sentinel's async agent runtime for local-first and air-gapped AI in Palo Alto, California.

## Engineering snapshot

| Area | Evidence |
| --- | --- |
| **LLM runtimes** | Model integration, repository context, multi-step tool orchestration, backend services, evaluation, and streaming tool calls |
| **Reliable execution** | Semaphore-bounded concurrency, approval gates, crash recovery, and production debugging |
| **Secure systems** | Rust sandboxing, Windows AppContainer/LPAC confinement, and Linux filesystem isolation |
| **GPU and distributed ML** | H100 training with DDP and FP16/BF16, FSDP checkpointing, vLLM rollout networking, and sub-10 ms A6000 inference |
| **Production engineering** | Amazon systems that supported 1.8× peak client traffic, reduced operating costs by 30%, and cut incidents by 60% |
| **Open-source systems** | SGLang, VERL, Megatron-LM, PyTorch AO, LLVM/MLIR, and arapuca · <!-- OSS-SUMMARY:START -->✅ [5 merged](#open-source-systems-work) · 🟠 [29 pending](#open-source-systems-work) · ⚪ [10 closed](#open-source-systems-work)<!-- OSS-SUMMARY:END --> |

## Open-source systems work

<!-- OSS-STATS:START -->
### Public PR activity

✅ merged · 🟠 pending · ⚪ closed — counts link to matching PRs and refresh automatically.

| Repository | Contribution area | PR status |
|---|---|---|
| [MPSLab-ASU/Seperating_OOD_and_ADV](https://github.com/MPSLab-ASU/Seperating_OOD_and_ADV) | Adversarial/OOD separation framework | [✅ 1 merged](https://github.com/MPSLab-ASU/Seperating_OOD_and_ADV/pull/1) · — · — |
| [NVIDIA/Megatron-LM](https://github.com/NVIDIA/Megatron-LM) | Pipeline-parallel execution and distributed training | — · [🟠 2 pending](https://github.com/search?q=repo%3ANVIDIA/Megatron-LM%20is%3Apr%20author%3Aamanyagami%20is%3Aopen&type=pullrequests) · — |
| [huggingface/trl](https://github.com/huggingface/trl) | Public PR activity | — · [🟠 2 pending](https://github.com/search?q=repo%3Ahuggingface/trl%20is%3Apr%20author%3Aamanyagami%20is%3Aopen&type=pullrequests) · — |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Public PR activity | — · — · [⚪ 3 closed](https://github.com/search?q=repo%3Alangchain-ai/langgraph%20is%3Apr%20author%3Aamanyagami%20is%3Aclosed%20-is%3Amerged&type=pullrequests) |
| [llvm/llvm-project](https://github.com/llvm/llvm-project) | MLIR compiler correctness | [✅ 2 merged](https://github.com/search?q=repo%3Allvm/llvm-project%20is%3Apr%20author%3Aamanyagami%20is%3Amerged&type=pullrequests) · [🟠 4 pending](https://github.com/search?q=repo%3Allvm/llvm-project%20is%3Apr%20author%3Aamanyagami%20is%3Aopen&type=pullrequests) · [⚪ 1 closed](https://github.com/llvm/llvm-project/pull/217513) |
| [ml-explore/mlx-lm](https://github.com/ml-explore/mlx-lm) | Public PR activity | — · — · [⚪ 2 closed](https://github.com/search?q=repo%3Aml-explore/mlx-lm%20is%3Apr%20author%3Aamanyagami%20is%3Aclosed%20-is%3Amerged&type=pullrequests) |
| [noahlabsai/arapuca](https://github.com/noahlabsai/arapuca) | Sandbox isolation on Linux and Windows | — · [🟠 1 pending](https://github.com/noahlabsai/arapuca/pull/1) · — |
| [pytorch/ao](https://github.com/pytorch/ao) | FP8 and quantization implementation work | — · [🟠 17 pending](https://github.com/search?q=repo%3Apytorch/ao%20is%3Apr%20author%3Aamanyagami%20is%3Aopen&type=pullrequests) · — |
| [sergio-correia/arapuca](https://github.com/sergio-correia/arapuca) | Sandbox isolation on Linux and Windows | [✅ 2 merged](https://github.com/search?q=repo%3Asergio-correia/arapuca%20is%3Apr%20author%3Aamanyagami%20is%3Amerged&type=pullrequests) · — · — |
| [sgl-project/sglang](https://github.com/sgl-project/sglang) | KV/radix-cache correctness across runtime backends | — · [🟠 1 pending](https://github.com/sgl-project/sglang/pull/35781) · — |
| [verl-project/verl](https://github.com/verl-project/verl) | FSDP checkpoint integrity and vLLM rollout networking | — · [🟠 2 pending](https://github.com/search?q=repo%3Averl-project/verl%20is%3Apr%20author%3Aamanyagami%20is%3Aopen&type=pullrequests) · [⚪ 4 closed](https://github.com/search?q=repo%3Averl-project/verl%20is%3Apr%20author%3Aamanyagami%20is%3Aclosed%20-is%3Amerged&type=pullrequests) |

<sub>Auto-updated 2026-08-28 03:45 UTC by [update-oss-stats.yml](.github/workflows/update-oss-stats.yml) · includes public PRs authored by amanyagami; excludes personal repositories</sub>
<!-- OSS-STATS:END -->

## Selected work

| Project | What it demonstrates |
| --- | --- |
| [Make Presentation Simple](https://github.com/amanyagami/Make_Presentation_Simple.io) | Serverless multimodal workflow using Lambda, Step Functions, S3, and DynamoDB |
| [Nandi — SLM Research Assistant](https://github.com/amanyagami/SLM-based-QA) | Direct prompting versus RAG across small and large language models |
| [ViT Fine-Tuning Benchmarks](https://github.com/amanyagami/Fine_Tuning_Vision_Transformers_on_Cifar100) | Reproducible vision-model fine-tuning and evaluation on CIFAR-100 |
| [DrDNA](https://github.com/amanyagami/Detecting-Silent-Data-Corruptions-in-Deep-Neural-Networks) | Post-hoc silent-data-corruption detection in deep networks |

## Research

**Viyog: Separating Adversarial and Out-of-Distribution**<br>
Accepted at **ESWEEK CODES 2026**

Research on separating adversarial and out-of-distribution inputs using intermediate-representation geometry, with reproducible PyTorch training and evaluation workflows.

## Education

- **M.S. in Computer Engineering** — Arizona State University, 2024–2026
- **B.Tech in Electrical and Electronics Engineering** — National Institute of Technology Karnataka, 2018–2022

## Technical toolkit

**Languages:** Python · C++ · Rust · Go · Java<br>
**ML systems:** PyTorch · CUDA · DDP/FSDP · Megatron-LM · FP16/BF16 · quantization · evaluation<br>
**LLM and inference:** SGLang · vLLM · Transformers · RAG · agentic systems · LoRA/QLoRA<br>
**Infrastructure:** Linux · Kubernetes · Docker · AWS · Google Cloud · CI/CD · Spark

## Connect

For ML systems, AI infrastructure, or research engineering opportunities: [email me](mailto:2amansingh2@gmail.com) or connect on [LinkedIn](https://www.linkedin.com/in/amanyagami).
