import socket
import time
from pathlib import Path
import shutil

home_directory = Path.home()
socket_path = "./windows/windows-monitor.socket"


def sendkey_sequence(
    sock: socket.socket,
    keys: list[str | list[str]],
    delay: float = 0.1,
):
    """
    Accepts ["ret", "ctrl-alt-del", ["c", "m", "d", "dot", "e", "x", "e"]]
    """
    for key in keys:
        if type(key) == str:
            cmd = f"sendkey {key}"
            sock.sendall((cmd + "\n").encode())
            time.sleep(delay)
        else:
            time.sleep(delay)
            # TODO type error, not supposed to happen here with key being list[str]
            sendkey_sequence(sock, key)
            time.sleep(delay)


def send_word_keys(words: str) -> list[str]:
    """
    Generate ["c", "m", "d", "dot", "e", "x", "e", "spc", "f", "ret"] from "cmd.exe f\n"
    """
    keys: list[str] = []
    # https://en.wikibooks.org/wiki/QEMU/Monitor#sendkey_keys
    map = {
        ",": "comma",
        ".": "dot",
        "/": "slash",
        "\\": "backslash",
        "*": "asterisk",
        " ": "spc",
        "-": "minus",
        "=": "equal",
        "\t": "tab",
        "\n": "ret",
    }
    for k in list(words):
        if k in map:
            k = map[k]
        keys.append(k)
    print(keys)  # debug
    return keys


def source_pwsh_script(sock: socket.socket, name: str, vm_ip: str):
    sendkey_sequence(
        sock,
        [
            send_word_keys(rf" . \\{vm_ip}\qemu\{name}"),
            "ret",
        ],
        delay=0,
    )
    time.sleep(1.5)
    sendkey_sequence(sock, ["r", "ret"])


def setup_sshd_qemu(vm_ip: str = "10.0.2.4"):
    """
    Setup sshd and start it on guest, automated
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(socket_path)

    f = home_directory / "Public" / "winusb-nix"
    try:
        shutil.rmtree(f)
    except:
        pass
    finally:
        f.mkdir(parents=True, exist_ok=True)
    d = Path.cwd() / ".." / "scripts" / "steps"
    d = d.resolve().absolute()

    scripts: list[str] = []
    for s in sorted(d.iterdir()):
        print(f"{s} -> {f}/{s.name}")
        scripts.append(rf"winusb-nix\{s.name}")
        _ = shutil.copy(s, f)

    try:
        # setup powershell
        sendkey_sequence(
            sock,
            [
                "ctrl-esc",
                send_word_keys("powershell.exe \n"),
                "ret",
            ],
        )
        time.sleep(5)
        sendkey_sequence(
            sock,
            [
                send_word_keys(
                    " set-executionpolicy -executionpolicy unrestricted -scope process -force\n"
                ),
            ],
        )

        # TODO allow steps installation
        # as of now combining them because individual sleeps are undertminable
        source_pwsh_script(sock, r"winusb-nix\setup.ps1", vm_ip)

        # TODO write progress or state to smb share
        # Monitor that from here and proceed with next step, i.e. ansible setup

        # sendkey_sequence(["ctrl-esc", send_word_keys("explorer.exe\n")])
        # time.sleep(1.5)
        # sendkey_sequence(["ctrl-l", send_word_keys(rf"\\{vm_ip}\qemu"), "ret"])
    except:
        pass
    finally:
        sock.close()


def setup_ansible_connection(
    user: str = "Quickemu",
    passwd: str = "quickemu",
    host: str = "localhost",
    port: str = "22220",
):
    """
    Initialise and wait for sshd connection from windows guest
    Some ssh command wrapping

    Initial conncection via ssh Quickemu@localhost -p 22220
    """
    conn_test = f"""sshpass -p {passwd} \
      ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      {user}@{host} -p {port} -t cmd.exe
    """
    print(conn_test)


def main():
    setup_sshd_qemu()
    conn = setup_ansible_connection()
    # run_ansible_setup(conn)


if __name__ == "__main__":
    main()
