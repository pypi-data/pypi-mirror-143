# -*- coding: utf-8 -*-

from __future__ import annotations

import enum
import inspect
import os
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Optional, Union

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from ignite.handlers.checkpoint import Checkpoint
from transformers.optimization import get_linear_schedule_with_warmup


class ModeKeys(str, enum.Enum):
    TRAIN = "train"
    EVAL = "eval"
    PREDICT = "predict"


class PhaseMixin(object):
    mode = ModeKeys.TRAIN

    def train(self) -> None:
        self.mode = ModeKeys.TRAIN

    def eval(self) -> None:
        self.mode = ModeKeys.EVAL

    def predict(self) -> None:
        self.mode = ModeKeys.PREDICT

    def is_train(self) -> bool:
        return self.mode == ModeKeys.TRAIN


def cuda(enable: bool) -> bool:
    return enable and torch.cuda.is_available()


def device(
    device_str: str = "", return_string: bool = True
) -> Union[str, torch.device]:
    if (
        not device_str
        or device_str.startswith("cuda")
        and not torch.cuda.is_available()
    ):
        device_str = "cpu"

    return device_str if return_string else torch.device(device_str)


def split_tensors(
    tensors: Iterable[torch.Tensor], chunk_size: int, dim: int = 0
) -> list[tuple[torch.Tensor, ...]]:
    sizes = [t.size() for t in tensors]
    if not sizes:
        raise ValueError("At least one tensor must be given.")

    for prev, this in zip(sizes, sizes[1:]):
        if prev[dim] != this[dim]:
            raise ValueError(
                f"Size of dimension `dim` = {dim}"  # type: ignore
                " must be same for all input tensors, "
                f"got: {list(map(tuple, sizes))}."
            )

    splits = list(zip(*(torch.split(x, chunk_size, dim=dim) for x in tensors)))

    return splits


def split_apply(
    f: Callable,
    inputs: Iterable[torch.Tensor],
    chunk_size: int,
    *args,
    dim: int = 0,
    **kwargs,
) -> Union[torch.Tensor, tuple[torch.Tensor, ...]]:
    chunks = split_tensors(inputs, chunk_size=chunk_size, dim=dim)
    outputs = [f(*chunk, *args, **kwargs) for chunk in chunks]

    if all(isinstance(t, torch.Tensor) for t in outputs):
        return torch.cat(outputs, dim=dim)

    outputs = list(zip(*outputs))
    tuple_outputs = tuple(torch.cat(x, dim=dim) for x in outputs)

    return tuple_outputs


def check_tensors_dimension(tensors: Iterable[torch.Tensor], dim: int):
    if any(not isinstance(x, torch.Tensor) or x.ndim != dim for x in tensors):
        raise ValueError(f"`tensors` must be {dim}d tensors.")


def pad_stack_1d(
    tensors: Sequence[torch.Tensor],
    max_length: Optional[int] = None,
    return_lengths: bool = False,
) -> Union[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
    # NOTE: Works for 1d tensors with size 0.

    check_tensors_dimension(tensors, 1)

    if max_length is None:
        length = torch.tensor([len(x) for x in tensors], dtype=torch.int64)
        max_length = max(length)
    else:
        if return_lengths:
            raise ValueError(
                "`return_lengths` must be False when `max_length` is given"
            )

    tensor = torch.stack([F.pad(x, [0, max_length - len(x)]) for x in tensors])

    if return_lengths:
        return tensor, length

    return tensor


def pad_stack_2d(
    tensors: Sequence[torch.Tensor], max_rows: int, max_columns: int
) -> torch.Tensor:
    # NOTE: Works for 2d tensors with size 0.

    check_tensors_dimension(tensors, 2)

    # https://discuss.pytorch.org/t/padding-zero-size-tensors/118777
    if max_rows == 0:
        return tensors[0].new_zeros(len(tensors), max_rows, max_columns)

    return torch.stack(
        [
            torch.nn.functional.pad(
                x, [0, max_columns - x.size(1), 0, max_rows - x.size(0)]
            )
            for x in tensors
        ]
    )


def get_default_arguments(f: Callable) -> dict:
    return {
        key: value.default
        for key, value in inspect.signature(f).parameters.items()
        if value.default is not value.empty
    }


def load_checkpoint(
    to_load: Union[Mapping, nn.Module], checkpoint: Union[str, os.PathLike]
) -> None:
    if isinstance(to_load, nn.Module):
        to_load = {"model": to_load}

    ckpt = torch.load(checkpoint, map_location="cpu")
    Checkpoint.load_objects(to_load=to_load, checkpoint=ckpt)


def plm_path(path: Union[str, os.PathLike]) -> str:
    root = os.getenv("PRETRAINED_MODEL_DIR")
    if root:
        return os.path.join(root, path)

    return str(path)


def get_pretrained_optimizer_and_scheduler(
    model: nn.Module,
    lr: float,
    weight_decay: float,
    warmup_steps: int,
    num_training_steps: Union[int, float],
    optimizer_kwargs: Optional[dict] = None,
    scheduler_kwargs: Optional[dict] = None,
) -> tuple[optim.Optimizer, optim.lr_scheduler.LambdaLR]:
    if lr <= 0:
        raise ValueError("`lr` must be positive.")

    if warmup_steps <= 0:
        raise ValueError("`warmup_steps` must be positive")

    if isinstance(warmup_steps, float):
        warmup_steps = int(warmup_steps * num_training_steps)

    if not optimizer_kwargs:
        optimizer_kwargs = {}

    if not scheduler_kwargs:
        scheduler_kwargs = {}

    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if not any(nd in n for nd in no_decay)
            ],
            "weight_decay": weight_decay,
        },
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.0,
        },
    ]
    optimizer = optim.AdamW(optimizer_grouped_parameters, lr=lr, **optimizer_kwargs)

    lr_scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=num_training_steps,
        **scheduler_kwargs,
    )

    return (optimizer, lr_scheduler)
