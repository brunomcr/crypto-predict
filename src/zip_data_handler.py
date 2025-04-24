import os
import zipfile
import shutil


class ZipDataHandler:
    def __init__(self, downloads_dir="downloads", target_dir="data/bronze", tmp_dir="tmp_extract"):
        self.downloads_dir = downloads_dir
        self.target_dir = target_dir
        self.tmp_dir = tmp_dir

    def process_all(self):
        if not os.path.isdir(self.downloads_dir):
            print(f"⚠️ Diretório {self.downloads_dir} não encontrado.")
            return

        zip_files = [f for f in os.listdir(self.downloads_dir) if f.endswith(".zip")]
        if not zip_files:
            print("📭 Nenhum arquivo .zip encontrado para processar.")
            return

        for zip_file in zip_files:
            zip_path = os.path.join(self.downloads_dir, zip_file)
            print(f"\n🔧 Processando: {zip_file}")

            try:
                self.extract(zip_path)
                self.move()
            except Exception as e:
                print(f"❌ Erro ao processar {zip_file}: {e}")
            finally:
                self.clean(zip_path, self.tmp_dir)

    def extract(self, zip_path):
        if not zipfile.is_zipfile(zip_path):
            raise ValueError(f"{zip_path} não é um .zip válido.")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.tmp_dir)
            print(f"📦 Extraído para: {self.tmp_dir}")

    def move(self):
        os.makedirs(self.target_dir, exist_ok=True)
        moved = 0
        for root, _, files in os.walk(self.tmp_dir):
            for file in files:
                if file.endswith(".json"):
                    src = os.path.join(root, file)
                    dst = os.path.join(self.target_dir, file)
                    shutil.move(src, dst)
                    print(f"✅ JSON movido: {dst}")
                    moved += 1
        if moved == 0:
            print("⚠️ Nenhum JSON encontrado.")
        else:
            print(f"🟢 Total de arquivos JSON movidos: {moved}")

    def clean(self, *paths):
        for path in paths:
            if os.path.isdir(path):
                shutil.rmtree(path)
                print(f"🗑️ Diretório removido: {path}")
            elif os.path.isfile(path):
                os.remove(path)
                print(f"🗑️ Arquivo removido: {path}")
            else:
                print(f"⚠️ {path} não existe ou já foi removido.")
