import os
from git import Repo
from google.cloud import firestore

# Firestore 초기화
db = firestore.Client()

# Git repository 경로 설정
repo_base_path = "/tmp/repos"

def clone_or_pull_repo(repo_url):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(repo_base_path, repo_name)

    # 레포지토리 경로가 없으면 클론, 있으면 pull
    if not os.path.exists(repo_path):
        repo = Repo.clone_from(repo_url, repo_path)
    else:
        repo = Repo(repo_path)
        repo.remotes.origin.pull()

    return repo

def get_latest_commit_sha(repo):
    return repo.head.object.hexsha

def check_for_changes(repo_url, previous_sha):
    repo = clone_or_pull_repo(repo_url)
    latest_sha = get_latest_commit_sha(repo)
    print(f"Previous SHA: {previous_sha}")
    print(f"Latest SHA: {latest_sha}")

    if previous_sha != latest_sha:
        print("Changes detected!")
        # 변경된 파일 목록 가져오기
        diff = repo.head.commit.diff(previous_sha)
        changed_files = [item.a_path for item in diff]
        print(f"Changed files: {changed_files}")

        # Firestore에 최신 SHA 업데이트
        repo_doc = db.collection('repos').where('url', '==', repo_url).limit(1).get()[0]
        repo_doc.reference.update({"latest_sha": latest_sha})

    return latest_sha


def main(request):
    # Firebase Firestore에서 Git repository 주소 받기 (예시로 첫번째 문서 사용)
    repos_ref = db.collection('repos')
    docs = repos_ref.stream()

    for doc in docs:
        repo_url = doc.to_dict().get("url")
        if repo_url:
            print(f"Processing repo: {repo_url}")
            sha = check_for_changes(repo_url)
            # 여기서 sha 또는 변경 사항을 처리하는 로직을 추가하면 됩니다.
            # 예를 들어, Firestore에 업데이트 된 SHA를 저장할 수 있습니다.
            repos_ref.document(doc.id).update({"latest_sha": sha})

    return "Function executed successfully"
