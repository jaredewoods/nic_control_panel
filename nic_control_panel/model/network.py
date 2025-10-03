import ctypes, ipaddress, re, subprocess, sys
from typing import Dict, List
from .types import Interface, NICRuntime, NICStaged

APP_TITLE = "NIC Control Panel (Windows)"

# ---------- subprocess helper ----------
def _run(cmd: str):
    c = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return c.returncode, c.stdout.strip(), c.stderr.strip()

# ---------- elevation ----------
def ensure_admin():
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False
    if not is_admin:
        params = " ".join(f'"{a}"' for a in sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable,
            f'"{sys.argv[0]}" {params}', None, 1)
        sys.exit()

# ---------- validators ----------
def ipv4(s: str) -> bool:
    try:
        ipaddress.IPv4Address(s); return True
    except Exception:
        return False

def same_subnet(ip: str, mask: str, gw: str) -> bool:
    try:
        net = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
        return ipaddress.IPv4Address(gw) in net
    except Exception:
        return False

# ---------- connectivity ----------
def ping(host: str, timeout_ms: int = 250) -> bool:
    code, _, _ = _run(f'ping -n 1 -w {int(timeout_ms)} {host}')
    return code == 0

# ---------- reads ----------
def list_interfaces() -> List[Interface]:
    code, out, err = _run('netsh interface show interface')
    if code != 0: raise RuntimeError(err or out)
    rows: List[Interface] = []
    for line in out.splitlines():
        m = re.match(r'^\s*(Enabled|Disabled)\s+(Connected|Disconnected)\s+\S+\s+(.+?)\s*$', line)
        if m:
            rows.append(Interface(
                name=m.group(3),
                enabled=(m.group(1)=="Enabled"),
                link_status=m.group(2),
            ))
    # augment with description/mac
    meta = get_adapter_meta()
    for it in rows:
        desc, mac = meta.get(it.name, ("", ""))
        it.description, it.mac = desc, mac
    return rows

def read_ip_config(name: str) -> NICRuntime:
    code, out, err = _run(f'netsh interface ip show config name="{name}"')
    if code != 0: raise RuntimeError(err or out)
    data = NICRuntime()
    m = re.search(r'DHCP enabled:\s*(Yes|No)', out, re.I)
    if m: data.dhcp = (m.group(1).lower() == "yes")
    m = re.search(r'IP(v4)? Address.*?:\s*([0-9.]+)', out, re.I)
    if m: data.ip = m.group(2)
    m = re.search(r'Subnet Prefix.*?mask\s*([0-9.]+)\)', out, re.I)
    if m: data.mask = m.group(1)
    else:
        m = re.search(r'Subnet Mask:\s*([0-9.]+)', out, re.I)
        if m: data.mask = m.group(1)
    m = re.search(r'Default Gateway:\s*([0-9.]+)', out, re.I)
    if m: data.gw = m.group(1)

    sb = re.search(r'Statically Configured DNS Servers:(.*?)(?:\n\n|\Z)', out, re.I|re.S)
    db = re.search(r'DNS servers configured through DHCP:(.*?)(?:\n\n|\Z)', out, re.I|re.S)
    if sb:
        data.dns = re.findall(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', sb.group(1)); data.dns_source="static"
    elif db:
        data.dns = re.findall(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', db.group(1)); data.dns_source="dhcp"
    return data

def get_adapter_meta() -> Dict[str, tuple]:
    code, out, _ = _run('getmac /v /fo csv')
    name_to = {}
    if code == 0:
        import csv
        from io import StringIO
        try:
            rdr = csv.DictReader(StringIO(out))
            for r in rdr:
                nm  = (r.get("Connection Name") or "").strip()
                nad = (r.get("Network Adapter") or "").strip()
                mac = (r.get("Physical Address") or "").strip()
                if nm: name_to[nm] = (nad, mac)
        except Exception:
            pass
    return name_to

# ---------- writes ----------
def set_static(name: str, ip: str, mask: str, gw: str=None):
    cmd = f'netsh interface ip set address name="{name}" static {ip} {mask}'
    if gw and gw.strip(): cmd += f' {gw} 1'  # metric 1; consider tuning
    code, out, err = _run(cmd)
    if code != 0: raise RuntimeError(err or out)

def set_dhcp(name: str):
    for c in [f'netsh interface ip set address name="{name}" dhcp',
              f'netsh interface ip set dns name="{name}" dhcp']:
        code, out, err = _run(c)
        if code != 0: raise RuntimeError(err or out)

def set_dns(name: str, dns_list: List[str]):
    if not dns_list:
        code, out, err = _run(f'netsh interface ip set dns name="{name}" dhcp')
        if code != 0: raise RuntimeError(err or out)
        return
    code, out, err = _run(f'netsh interface ip set dns name="{name}" static {dns_list[0]} primary')
    if code != 0: raise RuntimeError(err or out)
    for i, d in enumerate(dns_list[1:], start=2):
        code, out, err = _run(f'netsh interface ip add dns name="{name}" {d} index={i}')
        if code != 0: raise RuntimeError(err or out)

# ---------- controller helpers ----------
def validate_static(staged: NICStaged) -> None:
    if staged.mode != "Static":
        return
    ip, mask, gw = staged.ip, staged.mask, (staged.gw or "").strip() or None
    if not (ipv4(ip or "") and ipv4(mask or "")):
        raise RuntimeError("Invalid IP or Subnet Mask.")
    if gw and not ipv4(gw):
        raise RuntimeError("Invalid Default Gateway.")
    if gw and not same_subnet(ip, mask, gw):
        raise RuntimeError("Gateway not in same subnet.")
