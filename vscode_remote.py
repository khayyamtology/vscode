# pylint: disable=R0801 # similar-lines
from pathlib import Path


def config() -> dict:
    return {
        "files": {
            "/etc/nginx/nginx.conf": {
                "content": Path("stacks/common/cfn_init/files/vscode/nginx.conf").read_text(encoding="utf-8"),
            },
            "/usr/local/bin/vscode_cli_launcher.sh": {
                "content": Path("stacks/common/cfn_init/files/vscode/cli_launcher.sh").read_text(encoding="utf-8"),
                "mode": "000555",
                "owner": "root",
                "group": "root",
            },
        },
        "commands": {
            "01_setup_rules": {
                "command": "echo 'INFO: open ports' && semanage permissive -a httpd_t",
            },
            "02_install_nginx": {
                "command": "echo 'INFO: nginx' && dnf install -y nginx",
            },
            "03_generate_certs": {
                "command": "echo 'INFO: create self-signed certs for vscode+nginx' && openssl req -subj '/CN=localhost' -x509 -newkey rsa:4096 -nodes -keyout /etc/nginx/conf.d/key.pem -out /etc/nginx/conf.d/cert.pem -days 90",
            },
            "04_start_nginx": {
                "command": "echo 'INFO: starting nginx RI setup for VSCode' && systemctl enable nginx && systemctl start nginx",
            },
            "05_import_ms_keys": {
                "command": "echo 'INFO: Importing Microsoft keys' && rpm --import https://packages.microsoft.com/keys/microsoft.asc",
            },
            "06_add_ms_repo": {
                "command": "echo 'INFO: adding Microsoft repo' && sh -c 'echo -e \"[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc\" > /etc/yum.repos.d/vscode.repo'",
            },
            "07_install_vscode": {
                "command": "echo 'INFO: install VS Code' && dnf check && sudo dnf -y install code",
            },
        },
    }
