import os


class TortoiseConfig:
    @staticmethod
    def _discover_model_modules(root_path="server", debug=False):
        model_modules = []

        if debug:
            print(f"🔍 Scanning for `models.py` in root: {root_path}")

        for dirpath, _, filenames in os.walk(root_path):
            if debug:
                pass
                # print(f"📂 Checking directory: {dirpath}")

            if "models.py" in filenames:
                full_path = os.path.join(dirpath, "models.py")
                module_path = os.path.relpath(full_path).replace(os.sep, ".").removesuffix(".py")
                model_modules.append(module_path)

                if debug:
                    print(f"✅ Found model: {full_path} -> module: {module_path}")
            elif debug:
                pass
                # print("❌ No models.py found here.")

        if not model_modules:
            pass
            # raise Exception(f"❗ No models.py found in path '{root_path}'")

        if debug:
            print(f"📦 Discovered model modules: {model_modules}")

        return model_modules

    @staticmethod
    def config(username: str = None, password: str = None, host: str = None, db_name: str = None, port: int = 5432, debug=False):
        if not all([username, password, host, db_name]):
            raise Exception("username, password, host, and db_name cannot be None")

        if debug:
            print("🚀 Building Tortoise ORM config with the following DB info:")
            print(f"   Username: {username}")
            print(f"   Host: {host}")
            print(f"   Port: {port}")
            print(f"   DB Name: {db_name}")

        model_modules = TortoiseConfig._discover_model_modules(debug=debug)

        config = {
            "connections": {
                "default": f"postgres://{username}:{password}@{host}:{port}/{db_name}"
            },
            "apps": {
                "models": {
                    "models": model_modules,
                    "default_connection": "default",
                },
            },
        }

        if debug:
            pass
            # print("🔧 Final Tortoise ORM Configuration:")
            # from pprint import pprint
            # pprint(config)

        return config
