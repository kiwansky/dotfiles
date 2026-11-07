"""kyi-ws hardware: Intel CPU + NVIDIA GPU.

Replaces hardware-configuration.nix of kyi-ws:
  - hardware.cpu.intel.updateMicrocode  -> intel-ucode
  - hardware.nvidia (open = true)       -> nvidia-open + nvidia-utils
  - hardware.nvidia.modesetting.enable  -> modprobe.d options
  - boot.kernelModules (set by the NixOS nvidia module) -> modules-load.d
  - hardware.graphics.enable32Bit       -> lib32-nvidia-utils (multilib)

nvidia-open is prebuilt for the stock `linux` kernel used in the base
module. Filesystems/initrd are handled by the Arch installation itself.
"""

from decman import File, Module
from decman.plugins import pacman

from modules import files_path


class DesktopHardware(Module):

    def __init__(self):
        super().__init__(name="hardware-kyi-ws")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {
            "intel-ucode",
            "nvidia-open",
            "nvidia-utils",
            "lib32-nvidia-utils",
            "egl-wayland",
        }

    def files(self) -> dict[str, File]:
        return {
            "/etc/modprobe.d/nvidia-modeset.conf": File(
                source_file=files_path("modprobe", "nvidia-modeset.conf")
            ),
            # Load the NVIDIA modules in systemd-modules-load (sysinit.target)
            # instead of leaving it to udev. greetd starts after sysinit.target,
            # so the NVIDIA DRM device exists before the greeter's niri starts.
            # Without this, niri bound to the firmware framebuffer (simpledrm),
            # which nvidia-drm removed about two seconds later; the screen then
            # stayed frozen on the boot messages. Same role as
            # boot.kernelModules on NixOS.
            "/etc/modules-load.d/nvidia.conf": File(
                content="nvidia\nnvidia_modeset\nnvidia_uvm\nnvidia_drm\n"
            ),
        }
