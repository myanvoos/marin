"""

Usage:
1. If you have a model you want to download from huggingface, add the repo name and config in MODEL_NAME_TO_CONFIG.
2. Run download_model_step(MODEL_NAME_TO_CONFIG[model_name]) to download the model.
3. Use get_model_local_path(model_name) to get the local path of the model.

Example:
```
model_name = "meta-llama/Llama-3.1-8B-Instruct"
model_config = MODEL_NAME_TO_CONFIG[model_name]
download_step = download_model_step(model_config)
executor_main([download_step])

local_path = get_model_local_path(model_name)
```
"""

import os
from dataclasses import dataclass

from marin.download.huggingface.download import DownloadConfig
from marin.download.huggingface.download_hf import download_hf
from marin.execution.executor import ExecutorStep, this_output_path, versioned
from marin.utils import get_directory_friendly_name


@dataclass(frozen=True)
class ModelConfig:
    hf_repo_id: str
    hf_revision: str


# We utilize GCSFuse because our disk space is limited on TPUs.
# This means that for certain large models (e.g. Llama 70B), we will not be able
# to fit the models on local disk. We use GCSFuse to mount the GCS bucket to the local filesystem
# to be able to download and use these large models.
LOCAL_PREFIX = "/opt"
GCS_FUSE_MOUNT_PATH = "gcsfuse_mount/models"


def download_model_step(model_config: ModelConfig) -> ExecutorStep:
    model_name = get_directory_friendly_name(model_config.hf_repo_id)
    model_revision = get_directory_friendly_name(model_config.hf_revision)
    download_step = ExecutorStep(
        name=f"{GCS_FUSE_MOUNT_PATH}/{model_name}--{model_revision}",
        fn=download_hf,
        config=DownloadConfig(
            hf_dataset_id=model_config.hf_repo_id,
            revision=versioned(model_config.hf_revision),
            gcs_output_path=this_output_path(),
            wait_for_completion=True,
            hf_repo_type_prefix="",
        ),
        # must override because it because if we don't then it will end in a hash
        # if it ends in a hash, then we cannot determine the local path
        override_output_path=f"{GCS_FUSE_MOUNT_PATH}/{model_name}--{model_revision}",
    )

    return download_step


def get_model_local_path(step: ExecutorStep) -> str:
    model_repo_name = step.name[len(GCS_FUSE_MOUNT_PATH) + 1 :]
    return os.path.join(LOCAL_PREFIX, GCS_FUSE_MOUNT_PATH, model_repo_name)


smollm2_1_7b_instruct = download_model_step(
    ModelConfig(
        hf_repo_id="HuggingFaceTB/SmolLM2-1.7B-Instruct",
        hf_revision="450ff1f",
    )
)

# Note(Will): I don't think we actually support Qwen models in Levanter?
qwen2_5_7b_instruct = download_model_step(
    ModelConfig(
        hf_repo_id="Qwen/Qwen2.5-7B-Instruct",
        hf_revision="a09a354",
    )
)

qwen2_5_72b_instruct = download_model_step(
    ModelConfig(
        hf_repo_id="Qwen/Qwen2.5-72B-Instruct",
        hf_revision="495f393",
    )
)

llama_3_3_70b_instruct = download_model_step(
    ModelConfig(
        hf_repo_id="meta-llama/Llama-3.3-70B-Instruct",
        hf_revision="6f6073b",
    )
)

llama_3_1_8b_instruct = download_model_step(
    ModelConfig(
        hf_repo_id="meta-llama/Llama-3.1-8B-Instruct",
        hf_revision="0e9e39f",
    )
)

llama_3_1_8b = download_model_step(
    ModelConfig(
        hf_repo_id="meta-llama/Llama-3.1-8B",
        hf_revision="d04e592",
    )
)

tulu_3_1_8b_sft = download_model_step(
    ModelConfig(
        hf_repo_id="allenai/Llama-3.1-Tulu-3-8B-SFT",
        hf_revision="f2a0b46",
    )
)

tulu_3_1_8b_instruct = download_model_step(
    ModelConfig(
        hf_repo_id="allenai/Llama-3.1-Tulu-3.1-8B",
        hf_revision="46239c2",
    )
)

olmo_2_sft_8b = download_model_step(
    ModelConfig(
        hf_repo_id="allenai/OLMo-2-1124-7B-SFT",
        hf_revision="1de02c0",
    )
)

olmo_2_base_8b = download_model_step(
    ModelConfig(
        hf_repo_id="allenai/OLMo-2-1124-7B",
        hf_revision="7df9a82",
    )
)

amber_base_7b = download_model_step(
    ModelConfig(
        hf_repo_id="LLM360/Amber",
        hf_revision="83c188f",
    )
)

map_neo_7b = download_model_step(
    ModelConfig(
        hf_repo_id="m-a-p/neo_7b",
        hf_revision="81bad32",
    )
)
