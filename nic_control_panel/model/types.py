from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Interface:
    name: str
    enabled: bool
    link_status: str            # e.g., "Connected" / "Disconnected"
    description: str = ""
    mac: str = ""

@dataclass
class NICRuntime:
    dhcp: Optional[bool] = None
    ip: Optional[str] = None
    mask: Optional[str] = None
    gw: Optional[str] = None
    dns: List[str] = field(default_factory=list)
    dns_source: Optional[str] = None   # "static" | "dhcp" | None

@dataclass
class NICStaged:
    name: str
    mode: str                      # "DHCP" | "Static"
    ip: Optional[str] = None
    mask: Optional[str] = None
    gw: Optional[str] = None
    dns: List[str] = field(default_factory=list)
