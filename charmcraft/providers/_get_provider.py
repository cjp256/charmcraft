# Copyright 2021 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For further info, check https://github.com/canonical/charmcraft

"""Build environment provider support for charmcraft."""

import logging
import os
import sys

from charmcraft import snap
from charmcraft.cmdbase import CommandError
from charmcraft.env import is_charmcraft_running_from_snap

from ._lxd import LXDProvider
from ._multipass import MultipassProvider

logger = logging.getLogger(__name__)


def _get_platform_default_provider() -> str:
    if sys.platform == "linux":
        return "lxd"

    return "multipass"


def get_provider():
    """Get the configured or appropriate provider for the host OS.

    If platform is not Linux, use Multipass.

    If platform is Linux:
    (1) use provider specified with CHARMCRAFT_PROVIDER,
    (2) use provider specified with snap configuration,
    (3) default to LXD.

    :return: Provider instance.
    """
    provider = os.getenv("CHARMCRAFT_PROVIDER")
    if provider is None and is_charmcraft_running_from_snap():
        snap_config = snap.get_snap_configuration()
        provider = snap_config.provider if snap_config else None

    if provider is None:
        provider = _get_platform_default_provider()

    if provider == "lxd":
        return LXDProvider()
    elif provider == "multipass":
        return MultipassProvider()

    raise CommandError(f"Unsupported provider specified {provider!r}.")
