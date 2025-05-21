import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import sys

def load_config(config_path: str) -> dict:
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[!] Failed to load configuration file:{e}")
        sys.exit(1)

def validate_config(config: dict) -> None:
    
    required_fields = [
        "implant.name",
        "implant.language",
        "network.proxy_addr",
        "network.proxy_port",
        "security.key_part1"  
    ]

    empty_fields = []

    for field in required_fields:
        keys = field.split(".")
        current = config

        try:
            
            for key in keys:
                current = current[key]

            
            if current is None or (isinstance(current, str) and current.strip() == ""):
                empty_fields.append(field)

        except KeyError:
            
            continue

    
    if empty_fields:
        print("The following configuration fields are empty:")
        for field in empty_fields:
            print(f"- {field}")
        exit(1)

    print("Configuration validation succeeded!")

def render_template(template_dir: str, config: dict) -> str:
    """Render template, exit on failure."""
    language = config["implant"]["language"]
    template_name = f"{language}/main.{language}.tmpl"
    
    try:
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        return template.render(**config)
    except TemplateNotFound:
        print(f"[!] Template file not found: {template_name}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Template rendering failed: {e}")
        sys.exit(1)

def save_output(output_path: str, content: str) -> None:
    """Save generated file, exit on failure."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[!] Template rendering failed: {e}")
        sys.exit(1)

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, "configs", "implant.yml")
    TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

    
    config = load_config(CONFIG_PATH)
    
    
    validate_config(config)
    
    
    rendered = render_template(TEMPLATE_DIR, config)
    
    
    output_dir = os.path.join(BASE_DIR, "output")
    output_file = f"{config['implant']['name']}.{config['implant']['language']}"
    output_path = os.path.join(output_dir, output_file)
    save_output(output_path, rendered)
    
    print(f"[+] Implant program has been generated: {output_path}")

if __name__ == "__main__":
    main()