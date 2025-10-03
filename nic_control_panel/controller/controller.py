from typing import List
from model.types import Interface, NICRuntime, NICStaged
from model import network as net

class AppController:
    """Bridges View ↔ Model. View calls these; model performs system I/O."""
    def __init__(self):
        pass

    # ---- Reads ----
    def list_interfaces(self) -> List[Interface]:
        return net.list_interfaces()

    def read_runtime(self, iface_name: str) -> NICRuntime:
        return net.read_ip_config(iface_name)

    def connectivity_color(self, link_status: str) -> str:
        if link_status != "Connected":
            return "#e53935"  # red
        # quick reachability to public DNS — single check to avoid UI stalls
        return "#2e7d32" if (net.ping("1.1.1.1") or net.ping("8.8.8.8")) else "#f6c945"

    # ---- Writes ----
    def apply(self, staged: NICStaged) -> None:
        # IMPORTANT: do not silently convert DHCP DNS into a static override
        if staged.mode == "DHCP":
            net.set_dhcp(staged.name)
            return
        # Static path
        net.validate_static(staged)
        net.set_static(staged.name, staged.ip, staged.mask, staged.gw or None)
        net.set_dns(staged.name, staged.dns)
