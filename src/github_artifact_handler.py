import os
import requests

GITHUB_API = "https://api.github.com"

def list_artifacts(repo: str, token: str):
    url = f"{GITHUB_API}/repos/{repo}/actions/artifacts"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("artifacts", [])


def download_artifact(repo: str, token: str, artifact_id: int, output_path: str):
    url = f"{GITHUB_API}/repos/{repo}/actions/artifacts/{artifact_id}/zip"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()

    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"artifact_{artifact_id}.zip")

    with open(output_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✅ Downloaded artifact {artifact_id} to {output_file}")
    return output_file


def delete_artifact(repo: str, token: str, artifact_id: int):
    url = f"{GITHUB_API}/repos/{repo}/actions/artifacts/{artifact_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"🗑️ Artifact {artifact_id} deleted successfully.")
    else:
        print(f"❌ Failed to delete artifact {artifact_id}: {response.status_code} {response.text}")


def download_all_artifacts(repo: str, token: str, output_path: str = "downloads"):
    artifacts = list_artifacts(repo, token)
    for artifact in artifacts:
        artifact_id = artifact["id"]
        name = artifact["name"]
        print(f"⬇️ Baixando artefato: {name} (ID: {artifact_id})")
        try:
            download_artifact(repo, token, artifact_id, output_path)
            delete_artifact(repo, token, artifact_id)
        except Exception as e:
            print(f"⚠️ Erro ao processar artefato {artifact_id}: {e}")
